import json
import re
import reflex as rx
from urllib.parse import quote, urlparse
from curl_cffi import AsyncSession
from typing import List
from .utils import encrypt, decrypt, urlsafe_base64, extract_and_decode_var
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
        
        # Lista de URLs base ---
        self._base_urls = [
            "https://thedaddy.sx",         
            "https://dlhd.click"
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
        channels = []
        for base_url in self._base_urls:
            try:
                print(f"Tentando carregar canais de: {base_url}")
                response = await self._session.get(f"{base_url}/24-7-channels.php", headers={"user-agent": "Mozilla/5.0..."})
                response.raise_for_status()
                
                channels_block = re.compile("<center><h1(.+?)tab-2", re.MULTILINE | re.DOTALL).findall(str(response.text))
                if not channels_block:
                    continue
                
                channels_data = re.compile("href=\"(.*)\" target(.*)<strong>(.*)</strong>").findall(channels_block[0])
                for channel_data in channels_data:
                    channels.append(self._get_channel(channel_data))
                
                print(f"Canais carregados com sucesso de: {base_url}")
                self.channels = sorted(channels, key=lambda channel: (channel.name.startswith("18"), channel.name))
                return
            
            except Exception as e:
                print(f"Falha ao carregar de {base_url}: {e} - Tentando próxima URL...")
        
        print("Erro: Não foi possível carregar os canais de nenhuma das URLs fornecidas.")
        self.channels = []

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

    async def stream(self, channel_id: str):
        response = None  # Inicializa a variável para garantir que ela exista no bloco except
        url = "N/A"      # Inicializa a URL para o log de erro
        
        print(f"[LOG] Iniciando busca de stream para o canal ID: {channel_id}")
        
        for base_url in self._base_urls:
            try:
                print(f"\n[LOG] Usando base_url: {base_url}")
                
                prefixes = ["stream", "cast", "watch", "player", "casting"]
                for prefix in prefixes:
                    print(f"  [LOG] Tentando prefixo: '{prefix}'")
                    
                    if len(channel_id) > 3:
                        url = f"{base_url}/{prefix}/bet.php?id=bet{channel_id}"
                    else:
                        url = f"{base_url}/{prefix}/stream-{channel_id}.php"
                    
                    print(f"    [LOG] Construindo URL da página: {url}")
                    print(f"    [LOG] Fazendo requisição POST para a página...")
                    response = await self._session.post(url, headers=self._headers(referer=base_url))
                    response.raise_for_status()

                    print(f"    [LOG] Procurando pelo iframe na resposta...")
                    matches = re.compile("iframe.*?src=\"(.*?)\"").findall(response.text)
                    
                    if not matches:
                        print(f"    [AVISO] Padrão do iframe não encontrado em {url}. Tentando próximo prefixo.")
                        continue

                    source_url = matches[0]
                    print(f"    [LOG] Iframe encontrado! source_url: {source_url}")
                    
                    print(f"      > [DEBUG] Acessando source_url: {source_url}")
                    print(f"      > [DEBUG] Enviando referer: {url}")
                    source_response = await self._session.get(source_url, headers=self._headers(referer=url))
                    source_response.raise_for_status()

                    print(f"    [LOG] Extraindo channelKey...")
                    channel_key_match = re.compile(r"var\s+channelKey\s*=\s*\"(.*?)\";").findall(source_response.text)
                    if not channel_key_match:
                        print("    [ERRO] Não foi possível encontrar 'channelKey' no script do player.")
                        continue
                    channel_key = channel_key_match[-1]
                    print(f"      > channelKey: {channel_key}")

                    print(f"    [LOG] Extraindo variáveis de autenticação...")
                    auth_ts = extract_and_decode_var("__c", source_response.text)
                    auth_sig = extract_and_decode_var("__e", source_response.text)
                    auth_path = extract_and_decode_var("__b", source_response.text)
                    auth_rnd = extract_and_decode_var("__d", source_response.text)
                    auth_url = extract_and_decode_var("__a", source_response.text)
                    print(f"      > auth_url: {auth_url}, auth_path: {auth_path}, auth_ts: {auth_ts}...") # Log resumido

                    auth_request_url = f"{auth_url}{auth_path}?channel_id={channel_key}&ts={auth_ts}&rnd={auth_rnd}&sig={auth_sig}"
                    print(f"    [LOG] Construindo URL de autorização: {auth_request_url}")
                    print(f"    [LOG] Fazendo requisição de autorização...")
                    auth_response = await self._session.get(auth_request_url, headers=self._headers(referer=source_url))
                    auth_response.raise_for_status()
                    print(f"      > Autorização OK (Status: {auth_response.status_code})")

                    parsed_source_url = urlparse(source_url)
                    key_url = f"{parsed_source_url.scheme}://{parsed_source_url.netloc}/server_lookup.php?channel_id={channel_key}"
                    print(f"    [LOG] Construindo URL de busca do servidor: {key_url}")
                    print(f"    [LOG] Fazendo requisição de busca do servidor...")
                    key_response = await self._session.get(key_url, headers=self._headers(referer=source_url))
                    key_response.raise_for_status()
                    
                    server_key = key_response.json().get("server_key")
                    if not server_key:
                        raise ValueError("Chave 'server_key' não encontrada na resposta JSON.")
                    print(f"    [LOG] Chave do servidor encontrada: {server_key}")
                    
                    if server_key == "top1/cdn":
                        server_url = f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8"
                    else:
                        server_url = f"https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8"
                    print(f"    [LOG] Construindo URL final do M3U8: {server_url}")
                    
                    print(f"    [LOG] Baixando playlist M3U8...")
                    m3u8 = await self._session.get(server_url, headers=self._headers(referer=quote(str(source_url))))
                    m3u8.raise_for_status()
                    
                    print(f"    [LOG] Processando playlist M3U8 para ajustar URLs da chave...")
                    m3u8_data = ""
                    for line in m3u8.text.split("\n"):
                        if line.startswith("#EXT-X-KEY:"):
                            original_url = re.search(r'URI="(.*?)"', line).group(1)
                            line = line.replace(original_url, f"{config.api_url}/key/{encrypt(original_url)}/{encrypt(urlparse(source_url).netloc)}")
                        elif line.startswith("http") and config.proxy_content:
                            line = f"{config.api_url}/content/{encrypt(line)}"
                        m3u8_data += line + "\n"
                    
                    print(f"\n[SUCESSO] Stream obtido e processado com sucesso de: {base_url}")
                    return m3u8_data
                    
                raise ValueError(f"Não foi possível encontrar um source_url válido para os prefixos testados em {base_url}")

            except Exception as e:
                print(f"\n  [ERRO] Ocorreu uma falha durante a tentativa com a base_url '{base_url}'.")
                print(f"  [ERRO] A última URL tentada foi: {url}")
                print(f"  [ERRO] Detalhe da exceção: {e}")
                print("  [INFO] Tentando próxima base_url...\n")
        
        raise Exception("Erro: Falha ao obter o stream de todas as URLs disponíveis.")

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
                print(f"Tentando carregar schedule de: {base_url}")
                response = await self._session.get(f"{base_url}/schedule/schedule-generated.php", headers=self._headers(referer=base_url))
                response.raise_for_status()
                print(f"Schedule carregado com sucesso de: {base_url}")
                return response.json()
            except Exception as e:
                print(f"Falha ao carregar schedule de {base_url}: {e} - Tentando próxima URL...")
        
        raise Exception("Erro: Falha ao carregar o schedule de todas as URLs disponíveis.")