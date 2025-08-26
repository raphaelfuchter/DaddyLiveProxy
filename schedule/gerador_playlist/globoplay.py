import requests
import os
import re
from .config import GLOBOPLAY_CHANNELS, SERVER_IP, SERVER_PORT

GLOBOPLAY_BEARER = os.getenv("GLOBOPLAY_BEARER")

# --- CONFIGURAÇÃO DA REQUISIÇÃO ---
playback_api_url = "https://playback.video.globo.com/v4/video-session"
playback_api_headers = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.8',
    'authorization': f'Bearer {GLOBOPLAY_BEARER}',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://globoplay.globo.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://globoplay.globo.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}
payload_base = {
    "player_type": "desktop",
    "quality": "max",
    "content_protection": "widevine",
    "tz": "-03:00",
    "capabilities": {"low_latency": True, "smart_mosaic": True, "dvr": True},
    "consumption": "streaming",
    "metadata": {"name": "web", "device": {"type": "desktop", "os": {}}},
    "version": 2
}

def _sanitize_name(name):
    """Converte o nome do canal para um ID seguro para URL."""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def get_globoplay_stream_url(channel_id):
    """Busca a URL de stream real de um canal Globoplay pelo seu ID."""
    if not GLOBOPLAY_BEARER:
        print("❌ ERRO: GLOBOPLAY_BEARER não está configurado.")
        return None

    video_id = None
    for channel in GLOBOPLAY_CHANNELS:
        if _sanitize_name(channel['name']) == channel_id:
            video_id = channel['video_id']
            break

    if not video_id:
        print(f"❌ Canal com ID '{channel_id}' não encontrado.")
        return None

    current_payload = payload_base.copy()
    current_payload['video_id'] = video_id

    try:
        print(f"Buscando URL real para o canal ID: {channel_id}...")
        response = requests.post(playback_api_url, headers=playback_api_headers, json=current_payload)
        response.raise_for_status()
        playback_data = response.json()
        stream_url = playback_data['sources'][0]['url']
        print(f"✅ URL encontrada para {channel_id}.")
        return stream_url
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição para o canal ID {channel_id}: {e}")
    except (KeyError, IndexError):
        print(f"❌ Erro ao processar a resposta da API para o canal ID {channel_id}.")
    
    return None

def gerar_conteudo_globoplay():
    """Gera o conteúdo M3U para os canais Globoplay com URLs de proxy."""
    m3u_content = ""
    
    if not GLOBOPLAY_BEARER:
        print("\nAVISO: GLOBOPLAY_BEARER não definida. Pulando canais Globoplay.")
        return ""

    print("\nGerando URLs de proxy para canais Globoplay...")
    for channel in GLOBOPLAY_CHANNELS:
        channel_id = _sanitize_name(channel['name'])
        proxy_url = f"http://{SERVER_IP}:{SERVER_PORT}/stream/{channel_id}.m3u8"
        
        m3u_content += f'#EXTINF:-1 tvg-id="{channel["tvg_id"]}" tvg-name="{channel["name"]}" tvg-logo="{channel["tvg_logo"]}" group-title="{channel["group_title"]}",{channel["name"]}\n'
        m3u_content += proxy_url + "\n\n"

    if m3u_content:
        print(f"✅ {len(GLOBOPLAY_CHANNELS)} URLs de proxy para Globoplay geradas.")
    
    return m3u_content
