import json
import logging
import re
import reflex as rx
from urllib.parse import quote, urlparse
from curl_cffi import AsyncSession
from typing import List, Optional
from .utils import encrypt, decrypt, urlsafe_base64, decode_bundle
from rxconfig import config

# --- Configuração do Logging ---
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
        self.logger = logging.getLogger("StepDaddy")
        self.logger.info("Inicializando instância StepDaddy...")

        socks5 = config.socks5
        if socks5 != "":
            self._session = AsyncSession(proxy="socks5://" + socks5)
            self.logger.info(f"Usando proxy SOCKS5: {socks5}")
        else:
            self._session = AsyncSession()
            self.logger.info("Nenhum proxy SOCKS5 configurado.")

        self._base_urls = [
            "https://daddylivestream.com",
            "https://thedaddy.top",
            "https://thedaddy.sx"
        ]

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
            referer = self._base_urls[0]

        headers = {
            "Referer": referer,
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
        }
        if origin:
            headers["Origin"] = origin
        return headers

    async def load_channels(self):
        for base_url in self._base_urls:
            try:
                print(f"> Carregando canais de: {base_url}")
                response = await self._session.get(f"{base_url}/24-7-channels.php",
                                                   headers={"user-agent": "Mozilla/5.0..."})
                response.raise_for_status()

                channels_data = re.compile("href=\"(.*)\" target(.*)<strong>(.*)</strong>").findall(response.text)
                if not channels_data:
                    print(f"> Nenhum canal encontrado em {base_url}")
                    continue

                channels = []
                processed_ids = set()
                for channel_data in channels_data:
                    channel = self._get_channel(channel_data)
                    if channel and channel.id not in processed_ids:
                        channels.append(channel)
                        processed_ids.add(channel.id)

                if not channels:
                    print(f"> Nenhum canal válido encontrado em {base_url}, tentando próxima URL.")
                    continue

                print(f"> {len(channels)} canais carregados com sucesso de: {base_url}")
                self.channels = sorted(channels, key=lambda channel: (channel.name.startswith("18"), channel.name))
                return

            except Exception as e:
                print(f"> Falha ao carregar de {base_url}: {e}")

        print("! Erro: Não foi possível carregar os canais de nenhuma das URLs fornecidas.")
        self.channels = []

    def _get_channel(self, channel_data) -> Optional[Channel]:
        link_parts = channel_data[0].split('-')
        if len(link_parts) < 2:
            return None

        channel_id = link_parts[1].replace('.php', '')
        channel_name = channel_data[2]
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
        return Channel(id=channel_id, name=channel_name, tags=meta.get("tags", []), logo=logo)

    async def _get_source(self, channel_id: str):
        self.logger.info(f"Tentando obter URL de origem para o canal ID: {channel_id}")
        prefixes = ["cast", "watch", "casting"]

        for base_url in self._base_urls:
            self.logger.info(f"Tentando com a base: {base_url}")
            for prefix in prefixes:
                url = f"{base_url}/{prefix}/stream-{channel_id}.php"
                if len(channel_id) > 3:
                    url = f"{base_url}/{prefix}/bet.php?id=bet{channel_id}"

                try:
                    self.logger.debug(f"Tentando URL: {url}")
                    response = await self._session.post(url, headers=self._headers())
                    matches = re.compile("iframe src=\"(.*)\" width").findall(response.text)

                    if matches:
                        source_url = matches[0]
                        self.logger.info(f"URL de origem encontrada com sucesso: {source_url}")
                        return await self._session.post(source_url, headers=self._headers(url)), source_url
                except Exception as e:
                    self.logger.debug(f"Falha ao tentar {url}: {e}. Continuando...")
                    continue

        self.logger.error(
            f"Falha ao encontrar a URL de origem para o canal {channel_id} após tentar todas as bases e prefixos.")
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
            self.logger.debug(f"Chave do servidor encontrada: {server_key}")

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
        self.logger.debug(f"Buscando chave da URL descriptografada: {decrypted_url}")

        headers = self._headers(f"https://{decrypted_host}/", decrypted_host)
        self.logger.debug(f"Usando cabeçalhos para a solicitação da chave: {headers}")

        response = await self._session.get(decrypted_url, headers=headers, timeout=60)
        if response.status_code != 200:
            self.logger.error(f"Falha ao obter a chave. Status: {response.status_code}, URL: {decrypted_url}")
            raise Exception(f"Failed to get key")

        self.logger.debug("Chave buscada com sucesso.")
        return response.content

    @staticmethod
    def content_url(path: str):
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
        for base_url in self._base_urls:
            try:
                print(f"> Carregando schedule de: {base_url}")
                response = await self._session.get(f"{base_url}/schedule/schedule-generated.php", headers=self._headers(referer=base_url))
                response.raise_for_status()
                print(f"> Schedule carregado com sucesso de: {base_url}")
                return response.json()
            except Exception as e:
                print(f"> Falha ao carregar schedule de {base_url}: {e}")

        raise Exception("! Erro: Falha ao carregar o schedule de todas as URLs disponíveis.")