import json
import re
import reflex as rx
from urllib.parse import quote, urlparse
from curl_cffi import AsyncSession
from typing import List, Optional
import base64
from .utils import encrypt, decrypt, urlsafe_base64
from rxconfig import config


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
            self._session = AsyncSession(timeout=60, allow_redirects=True)

        self._base_urls = [
            "https://thedaddy.sx",
            "https://thedaddy.top",
            "https://daddylivestream.com"
        ]

        self.channels = []
        with open("StepDaddyLiveHD/meta.json", "r") as f:
            self._meta = json.load(f)

    def _headers(self, referer: str = None, origin: str = None):
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

    async def stream(self, channel_id: str):
        response = None
        url = "N/A"

        print(f"\n[INFO] Iniciando busca de stream para o canal ID: {channel_id}")

        for base_url in self._base_urls:
            print(f"[INFO] Usando base: {base_url}")
            prefixes = ["stream", "cast", "watch", "player", "casting"]
            for prefix in prefixes:
                try:
                    if len(channel_id) > 3:
                        url = f"{base_url}/{prefix}/bet.php?id=bet{channel_id}"
                    else:
                        url = f"{base_url}/{prefix}/stream-{channel_id}.php"

                    print(f"  > Tentando URL: {url}")
                    response = await self._session.post(url, headers=self._headers(referer=base_url))
                    response.raise_for_status()

                    matches = re.compile("iframe.*?src=\"(https?://.*?)\"").findall(response.text)
                    if not matches:
                        continue

                    source_url = matches[0].strip()
                    if not source_url.startswith("http"):
                        continue

                    print(f"  > Iframe encontrado: {source_url}")
                    source_response = await self._session.get(source_url, headers=self._headers(referer=url))
                    source_response.raise_for_status()

                    channel_key_match = re.search(r'const CHANNEL_KEY = "([^"]+)"', source_response.text)
                    if not channel_key_match:
                        print("    ! Erro: 'CHANNEL_KEY' não encontrada no script do player.")
                        continue
                    channel_key = channel_key_match.group(1)

                    bundle_match = re.search(r'const BUNDLE = "([^"]+)"', source_response.text)
                    if not bundle_match:
                        print("    ! Erro: 'BUNDLE' não encontrado no script do player.")
                        continue
                    bundle = bundle_match.group(1)

                    try:
                        decoded_json_str = base64.b64decode(bundle).decode('utf-8')
                        parts_encoded = json.loads(decoded_json_str)
                        parts = {k: base64.b64decode(v).decode('utf-8') for k, v in parts_encoded.items()}
                    except Exception as e:
                        print(f"    ! Erro: Falha ao decodificar o BUNDLE: {e}")
                        continue

                    auth_request_url = (
                        f"{parts['b_host']}{parts['b_script']}"
                        f"?channel_id={quote(channel_key)}"
                        f"&ts={quote(parts['b_ts'])}"
                        f"&rnd={quote(parts['b_rnd'])}"
                        f"&sig={quote(parts['b_sig'])}"
                    )

                    print(f"    > URL de autorização: {auth_request_url[:80]}...")
                    auth_response = await self._session.get(auth_request_url, headers=self._headers(referer=source_url))
                    auth_response.raise_for_status()
                    print(f"    > Autorização OK (Status: {auth_response.status_code})")

                    parsed_source_url = urlparse(source_url)
                    key_url = f"{parsed_source_url.scheme}://{parsed_source_url.netloc}/server_lookup.php?channel_id={channel_key}"
                    print(f"    > Buscando servidor: {key_url}")
                    key_response = await self._session.get(key_url, headers=self._headers(referer=source_url))
                    key_response.raise_for_status()

                    server_key = key_response.json().get("server_key")
                    if not server_key:
                        raise ValueError("Chave 'server_key' não encontrada na resposta JSON.")
                    print(f"    > Chave do servidor: {server_key}")

                    if server_key == "top1/cdn":
                        server_url = f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8"
                    else:
                        server_url = f"https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8"
                    print(f"    > URL do M3U8: {server_url}")

                    m3u8 = await self._session.get(server_url, headers=self._headers(referer=quote(str(source_url))))
                    m3u8.raise_for_status()

                    m3u8_data = ""
                    for line in m3u8.text.split("\n"):
                        if line.startswith("#EXT-X-KEY:"):
                            original_url = re.search(r'URI="(.*?)"', line).group(1)
                            line = line.replace(original_url,
                                                f"{config.api_url}/key/{encrypt(original_url)}/{encrypt(urlparse(source_url).netloc)}")
                        elif line.startswith("http") and config.proxy_content:
                            line = f"{config.api_url}/content/{encrypt(line)}"
                        m3u8_data += line + "\n"

                    print(f"[SUCESSO] Stream para o canal {channel_id} obtido de {base_url}")
                    return m3u8_data

                except Exception as e:
                    print(f"\n  [ERRO] Falha na tentativa com a base_url '{base_url}' e prefixo '{prefix}'.")
                    print(f"    > Última URL: {url}")
                    print(f"    > Detalhe: {e}")
                    print("  [INFO] Tentando próxima combinação...\n")

            print(f"  ! Nenhum stream funcional encontrado para os prefixos em {base_url}")

        raise Exception(f"Erro: Falha ao obter o stream para o canal {channel_id} de todas as URLs disponíveis.")

    async def key(self, url: str, host: str):
        url = decrypt(url)
        host = decrypt(host)
        response = await self._session.get(url, headers=self._headers(referer=f"{host}/", origin=host), timeout=60)
        if response.status_code != 200:
            raise Exception(f"Failed to get key")
        return response.content

    @staticmethod
    def content_url(path: str):
        return decrypt(path)

    def playlist(self):
        data = "#EXTM3U\n"
        for channel in self.channels:
            entry = f" tvg-logo=\"{channel.logo}\",{channel.name}" if channel.logo else f",{channel.name}"
            data += f"#EXTINF:-1{entry}\n{config.api_url}/stream/{channel.id}.m3u8\n"
        return data

    async def schedule(self):
        for base_url in self._base_urls:
            try:
                print(f"> Carregando schedule de: {base_url}")
                response = await self._session.get(f"{base_url}/schedule/schedule-generated.php",
                                                   headers=self._headers(referer=base_url))
                response.raise_for_status()
                print(f"> Schedule carregado com sucesso de: {base_url}")
                return response.json()
            except Exception as e:
                print(f"> Falha ao carregar schedule de {base_url}: {e}")

        raise Exception("! Erro: Falha ao carregar o schedule de todas as URLs disponíveis.")
