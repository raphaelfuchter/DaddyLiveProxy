import json
import logging
import re
import reflex as rx
from urllib.parse import quote, urlparse
from curl_cffi import AsyncSession
from typing import List
from .utils import encrypt, decrypt, urlsafe_base64, decode_bundle
from rxconfig import config

# --- Configuração do Logging ---
# Configura o logger para exibir mensagens no console com um formato claro.
# Mude level=logging.INFO para level=logging.DEBUG para ver mensagens mais detalhadas.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# -----------------------------


class Channel(rx.Base):
    id: str
    name: str
    tags: List[str]
    logo: str


class StepDaddy:
    def __init__(self):
        # Cria um logger específico para esta classe
        self.logger = logging.getLogger("StepDaddy")
        self.logger.info("Inicializando instância StepDaddy...")

        socks5 = config.socks5
        if socks5 != "":
            self._session = AsyncSession(proxy="socks5://" + socks5)
            self.logger.info(f"Usando proxy SOCKS5: {socks5}")
        else:
            self._session = AsyncSession()
            self.logger.info("Nenhum proxy SOCKS5 configurado.")

        self._base_url = "https://thedaddy.top"
        self.channels = []
        try:
            with open("StepDaddyLiveHD/meta.json", "r") as f:
                self._meta = json.load(f)
            self.logger.info("Metadados de meta.json carregados com sucesso.")
        except FileNotFoundError:
            self.logger.error("meta.json não encontrado! Os metadados dos canais estarão ausentes.")
            self._meta = {}
        except json.JSONDecodeError:
            self.logger.error("Falha ao analisar meta.json. Pode estar corrompido.")
            self._meta = {}

    def _headers(self, referer: str = None, origin: str = None):
        if referer is None:
            referer = self._base_url
        headers = {
            "Referer": referer,
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
        }
        if origin:
            headers["Origin"] = origin
        return headers

    async def load_channels(self):
        self.logger.info("Iniciando o carregamento de canais...")
        channels = []
        url = f"{self._base_url}/24-7-channels.php"
        try:
            self.logger.debug(f"Buscando canais de {url}")
            response = await self._session.get(url, headers=self._headers())
            response.raise_for_status()  # Lança um erro para status HTTP 4xx/5xx

            channels_block = re.compile("<center><h1(.+?)tab-2", re.MULTILINE | re.DOTALL).findall(str(response.text))
            if not channels_block:
                self.logger.error("Não foi possível encontrar o bloco principal de canais na página.")
                return

            channels_data = re.compile("href=\"(.*)\" target(.*)<strong>(.*)</strong>").findall(channels_block[0])
            self.logger.info(f"Encontrados {len(channels_data)} canais em potencial.")

            for channel_data in channels_data:
                channels.append(self._get_channel(channel_data))

        except Exception as e:
            self.logger.error(f"Falha ao carregar canais de {url}.", exc_info=True)
        finally:
            self.channels = sorted(channels, key=lambda channel: (channel.name.startswith("18"), channel.name))
            self.logger.info(f"Carregamento finalizado. Total de canais carregados e ordenados: {len(self.channels)}")

    def _get_channel(self, channel_data) -> Channel:
        channel_id = channel_data[0].split('-')[1].replace('.php', '')
        channel_name = channel_data[2]

        # Lógica para nomes especiais de canais
        if channel_id == "666":
            channel_name = "Nick Music"
        if channel_id == "609":
            channel_name = "Yas TV UAE"
        if channel_data[2] == "#0 Spain":
            channel_name = "Movistar Plus+"
        elif channel_data[2] == "#Vamos Spain":
            channel_name = "Vamos Spain"

        clean_channel_name = re.sub(r"\s*\(.*?\)", "", channel_name)
        meta = self._meta.get(clean_channel_name, {})
        logo = meta.get("logo", "/missing.png")
        if logo.startswith("http"):
            logo = f"{config.api_url}/logo/{urlsafe_base64(logo)}"

        self.logger.debug(f"Canal processado: ID={channel_id}, Nome='{channel_name}'")
        return Channel(id=channel_id, name=channel_name, tags=meta.get("tags", []), logo=logo)

    async def _get_source(self, channel_id: str):
        self.logger.info(f"Tentando obter URL de origem para o canal ID: {channel_id}")
        prefixes = ["cast", "watch", "stream"]
        for prefix in prefixes:
            url = f"{self._base_url}/{prefix}/stream-{channel_id}.php"
            if len(channel_id) > 3:
                url = f"{self._base_url}/{prefix}/bet.php?id=bet{channel_id}"

            self.logger.debug(f"Tentando URL: {url}")
            response = await self._session.post(url, headers=self._headers())
            matches = re.compile("iframe src=\"(.*)\" width").findall(response.text)

            if matches:
                source_url = matches[0]
                self.logger.info(f"URL de origem encontrada com sucesso: {source_url}")
                return await self._session.post(source_url, headers=self._headers(url)), source_url

        self.logger.error(f"Falha ao encontrar a URL de origem para o canal {channel_id} após tentar todos os prefixos.")
        raise ValueError("Failed to find source URL for channel")

    async def stream(self, channel_id: str):
        self.logger.info(f"Iniciando processo de stream para o canal ID: {channel_id}")
        try:
            source_response, source_url = await self._get_source(channel_id)

            channel_key = re.compile(r"const\s+CHANNEL_KEY\s*=\s*\"(.*?)\";").findall(source_response.text)[-1]
            bundle = re.compile(r"const\s+XJZ\s*=\s*\"(.*?)\";").findall(source_response.text)[-1]
            self.logger.debug(f"Extraído CHANNEL_KEY: {channel_key} de {source_url}")

            data = decode_bundle(bundle)
            auth_ts = data.get("b_ts", "")
            auth_sig = data.get("b_sig", "")
            auth_rnd = data.get("b_rnd", "")
            auth_url = data.get("b_host", "")

            auth_request_url = f"{auth_url}auth.php?channel_id={channel_key}&ts={auth_ts}&rnd={auth_rnd}&sig={auth_sig}"
            self.logger.debug(f"Solicitando autenticação de: {auth_request_url}")
            auth_response = await self._session.get(auth_request_url, headers=self._headers(source_url))
            if auth_response.status_code != 200:
                self.logger.error(f"Falha ao obter resposta de autenticação. Status: {auth_response.status_code}")
                raise ValueError("Failed to get auth response")

            key_url = urlparse(source_url)
            key_url = f"{key_url.scheme}://{key_url.netloc}/server_lookup.php?channel_id={channel_key}"
            self.logger.debug(f"Procurando chave do servidor em: {key_url}")
            key_response = await self._session.get(key_url, headers=self._headers(source_url))

            server_key = key_response.json().get("server_key")
            if not server_key:
                self.logger.error("Nenhuma chave de servidor encontrada na resposta de server_lookup.php")
                raise ValueError("No server key found in response")
            self.logger.info(f"Chave do servidor encontrada: {server_key}")

            if server_key == "top1/cdn":
                server_url = f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8"
            else:
                server_url = f"https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8"

            self.logger.debug(f"Buscando playlist m3u8 de: {server_url}")
            m3u8 = await self._session.get(server_url, headers=self._headers(quote(str(source_url))))

            m3u8_data = ""
            for line in m3u8.text.split("\n"):
                if line.startswith("#EXT-X-KEY:"):
                    original_url = re.search(r'URI="(.*?)"', line).group(1)
                    line = line.replace(original_url,
                                        f"{config.api_url}/key/{encrypt(original_url)}/{encrypt(urlparse(source_url).netloc)}")
                elif line.startswith("http") and config.proxy_content:
                    line = f"{config.api_url}/content/{encrypt(line)}"
                m3u8_data += line + "\n"

            self.logger.info(f"Playlist m3u8 gerada com sucesso para o canal {channel_id}")
            return m3u8_data
        except Exception as e:
            self.logger.error(f"Ocorreu um erro durante o processo de stream para o canal {channel_id}.", exc_info=True)
            raise

    async def key(self, url: str, host: str):
        decrypted_url = decrypt(url)
        decrypted_host = decrypt(host)
        self.logger.info(f"Buscando chave da URL descriptografada: {decrypted_url}")

        headers = self._headers(f"https://{decrypted_host}/", decrypted_host)
        self.logger.debug(f"Usando cabeçalhos para a solicitação da chave: {headers}")

        response = await self._session.get(decrypted_url, headers=headers, timeout=60)
        if response.status_code != 200:
            self.logger.error(f"Falha ao obter a chave. Status: {response.status_code}, URL: {decrypted_url}")
            raise Exception(f"Failed to get key")

        self.logger.info("Chave buscada com sucesso.")
        return response.content

    @staticmethod
    def content_url(path: str):
        # Logging aqui pode expor URLs de conteúdo, então é melhor evitar a menos que seja para depuração intensa.
        # logging.getLogger("StepDaddy").debug(f"Decrypting content path: {path}")
        return decrypt(path)

    def playlist(self):
        self.logger.info("Gerando playlist M3U principal...")
        if not self.channels:
            self.logger.warning("Gerando playlist, mas a lista de canais está vazia.")

        data = "#EXTM3U\n"
        for channel in self.channels:
            entry = f" tvg-logo=\"{channel.logo}\",{channel.name}" if channel.logo else f",{channel.name}"
            data += f"#EXTINF:-1{entry}\n{config.api_url}/stream/{channel.id}.m3u8\n"

        self.logger.info(f"Playlist gerada para {len(self.channels)} canais.")
        return data

    async def schedule(self):
        self.logger.info("Buscando a programação...")
        url = f"{self._base_url}/schedule/schedule-generated.php"
        try:
            response = await self._session.get(url, headers=self._headers())
            response.raise_for_status()
            self.logger.info("Programação buscada com sucesso.")
            return response.json()
        except Exception as e:
            self.logger.error(f"Falha ao buscar a programação de {url}.", exc_info=True)
            return {}  # Retorna um dicionário vazio em caso de erro