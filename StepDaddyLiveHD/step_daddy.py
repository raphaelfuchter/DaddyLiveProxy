import json
import re
import os
import reflex as rx
from urllib.parse import quote, urlparse
from curl_cffi import AsyncSession
from typing import List, Dict
from .utils import encrypt, decrypt, urlsafe_base64, decode_bundle
from rxconfig import config
import logging

# Silencia os logs de INFO da biblioteca subjacente de HTTP
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING) # Adicionado por segurança, caso httpx também seja usado

# Configuração básica do logging para exibir mensagens de nível DEBUG
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Channel(rx.Base):
    id: str
    name: str
    tags: List[str]
    logo: str


class StepDaddy:
    def __init__(self):
        socks5 = config.socks5
        if socks5 != "":
            self._session = AsyncSession(proxy="socks5://" + socks5)
        else:
            self._session = AsyncSession()

        self.channels = []
        with open("StepDaddyLiveHD/meta.json", "r") as f:
            self._meta = json.load(f)
        self._cache = {}

    def _headers(self, referer: str = None, origin: str = None):
        settings = self._load_settings()
        base_url = settings["base_url"]

        if referer is None:
            referer = base_url
        headers = {
            "Referer": referer,
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
        }
        if origin:
            headers["Origin"] = origin
        return headers

    async def load_channels(self):
        channels = []
        settings = self._load_settings()
        base_url = settings["base_url"]

        try:
            response = await self._session.get(f"{base_url}/24-7-channels.php", headers=self._headers())
            response.raise_for_status()
            channels_data = re.compile("href=\"(.*)\" target(.*)<strong>(.*)</strong>").findall(response.text)
            channels = []
            processed_ids = set()
            for channel_data in channels_data:
                channel = self._get_channel(channel_data)
                if channel and channel.id not in processed_ids:
                    channels.append(channel)
                    processed_ids.add(channel.id)
        finally:
            self.channels = sorted(channels, key=lambda channel: (channel.name.startswith("18"), channel.name))

    def _get_channel(self, channel_data) -> Channel:
        channel_id = channel_data[0].split('-')[1].replace('.php', '')
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

    @staticmethod
    def _load_settings() -> Dict[str, str]:
        """Carrega as configurações do arquivo settings.json."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(current_dir, "settings.json")

        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)

                return {
                    "base_url": settings.get("base_url"),
                    "prefix": settings.get("prefix")
                }
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError("Falha ao encontrar ou ler o arquivo settings.json")

    # Not generic
    async def stream(self, channel_id: str):
        logging.info(f"Iniciando método stream para o channel_id: {channel_id}")

        if self._cache.get("channel_id") == channel_id:
            logging.info(f"Usando server_url e source_url do cache para o canal {channel_id}")
            server_url = self._cache["server_url"]
            source_url = self._cache["source_url"]
        else:
            self._cache.clear()
            settings = self._load_settings()
            base_url = settings["base_url"]
            user_prefix = settings["prefix"]
            logging.info(f"Configurações carregadas: base_url='{base_url}', prefix='{user_prefix}'")

            key = "CHANNEL_KEY"
            prefix = user_prefix
            logging.debug(f"Tentando com o prefixo: '{prefix}'")
            url = f"{base_url}/{prefix}/stream-{channel_id}.php"
            if len(channel_id) > 3:
                url = f"{base_url}/stream/bet.php?id=bet{channel_id}"

            logging.debug(f"Construindo URL de requisição: {url}")
            response = await self._session.post(url, headers=self._headers())
            logging.info(f"Resposta recebida de {url} com status: {response.status_code}")

            matches = re.compile('''iframe src=\\"(.*)\\" width''').findall(response.text)
            if not matches:
                logging.debug("Nenhum iframe encontrado na resposta.")
                logging.error("Falha ao encontrar uma source_url válida para o canal.")
                raise ValueError("Failed to find source URL for channel")

            source_url = matches[0]
            logging.debug(f"Iframe encontrado com source_url: {source_url}")
            source_response = await self._session.post(source_url, headers=self._headers(url))
            logging.info(f"Resposta recebida do source_url com status: {source_response.status_code}")

            if key not in source_response.text:
                logging.debug(f"'{key}' não encontrada na resposta do source_url.")
                logging.error("Falha ao encontrar uma source_url válida para o canal.")
                raise ValueError("Failed to find source URL for channel")

            logging.debug(f"'{key}' encontrada na resposta.")

            channel_key = re.compile(rf'''const\s+{re.escape(key)}\s*=\s*\"(.*?)\";''').findall(source_response.text)[-1]
            logging.debug(f"Channel key extraída: {channel_key}")

            bundle = re.compile(r'''const\s+XJZ\s*=\s*\"(.*?)\";''').findall(source_response.text)[-1]
            logging.debug(f"Bundle encontrado: {bundle[:30]}...")  # Loga apenas o início do bundle

            data = decode_bundle(bundle)
            auth_ts = data.get("b_ts", "")
            auth_sig = data.get("b_sig", "")
            auth_rnd = data.get("b_rnd", "")
            auth_url = data.get("b_host", "")
            logging.debug(
                f"Dados do bundle decodificados: auth_ts='{auth_ts}', auth_sig='{auth_sig}', auth_rnd='{auth_rnd}', auth_url='{auth_url}'")

            auth_request_url = f"{auth_url}auth.php?channel_id={channel_key}&ts={auth_ts}&rnd={auth_rnd}&sig={auth_sig}"
            logging.debug(f"URL de autenticação: {auth_request_url}")

            auth_response = await self._session.get(auth_request_url, headers=self._headers(source_url))
            logging.debug(f"Resposta da autenticação recebida com status: {auth_response.status_code}")

            if auth_response.status_code != 200:
                logging.error("Falha ao obter resposta da autenticação.")
                raise ValueError("Failed to get auth response")

            key_url = urlparse(source_url)
            key_url = f"{key_url.scheme}://{key_url.netloc}/server_lookup.php?channel_id={channel_key}"
            logging.debug(f"URL para lookup do servidor: {key_url}")

            key_response = await self._session.get(key_url, headers=self._headers(source_url))
            logging.debug(f"Resposta do lookup do servidor recebida com status: {key_response.status_code}")

            server_key = key_response.json().get("server_key")
            logging.debug(f"Server key obtida: {server_key}")

            if not server_key:
                logging.error("Nenhuma server_key encontrada na resposta.")
                raise ValueError("No server key found in response")

            if server_key == "top1/cdn":
                server_url = f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8"
            else:
                server_url = f"https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8"
            logging.debug(f"URL do m3u8 final: {server_url}")

            self._cache["channel_id"] = channel_id
            self._cache["server_url"] = server_url
            self._cache["source_url"] = source_url

        m3u8 = await self._session.get(server_url, headers=self._headers(quote(str(source_url))))
        logging.debug(f"m3u8 obtido com status: {m3u8.status_code}")

        m3u8_data = ""
        for line in m3u8.text.split("\n"):
            if line.startswith("#EXT-X-KEY:"):
                original_url = re.search(r'''URI=\"(.*?)\"''', line).group(1)
                new_url = f"{config.api_url}/key/{encrypt(original_url)}/{encrypt(urlparse(source_url).netloc)}"
                line = line.replace(original_url, new_url)
                logging.debug(f"Linha de chave #EXT-X-KEY modificada para: {line}")

            elif line.startswith("http") and config.proxy_content:
                original_line = line
                line = f"{config.api_url}/content/{encrypt(line)}"
                logging.debug(f"Linha de conteúdo '{original_line}' modificada para proxy: {line}")

            m3u8_data += line + "\n"

        logging.info("Processamento do m3u8 finalizado. Retornando dados.")
        return m3u8_data

    async def key(self, url: str, host: str):
        url = decrypt(url)
        host = decrypt(host)
        response = await self._session.get(url, headers=self._headers(f"{host}/", host), timeout=60)
        if response.status_code != 200:
            raise Exception(f"Failed to get key")
        return response.content

    @staticmethod
    def content_url(path: str):
        return decrypt(path)

    def playlist(self):
        data = "#EXTM3U\n"
        for channel in self.channels:
            entry = f''' tvg-logo=\"{channel.logo}\",{channel.name}''' if channel.logo else f",{channel.name}"
            data += f"#EXTINF:-1{entry}\n{config.api_url}/stream/{channel.id}.m3u8\n"
        return data

    async def schedule(self):
        settings = self._load_settings()
        base_url = settings["base_url"]

        response = await self._session.get(f"{base_url}/schedule/schedule-generated.php", headers=self._headers())
        return response.json()
