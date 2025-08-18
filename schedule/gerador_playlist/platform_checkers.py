# gerador_playlist/platform_checkers.py

import re
from typing import Union
import requests
from bs4 import BeautifulSoup

def _format_youtube_title(title: str) -> str:
    if not title: return "Evento Ao Vivo"
    cleaned_title = re.sub(r'ao vivo:?\s*\|?\s*', '', title, flags=re.IGNORECASE).strip()
    return cleaned_title.title()

def get_youtube_live_title(channel_url: str) -> Union[str, None]:
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.5"}
        response = requests.get(channel_url, headers=headers, timeout=10)
        response.raise_for_status()
        if '"isLiveNow":true' in response.text:
            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.find('meta', property='og:title')
            if title_tag and title_tag.get('content'):
                return _format_youtube_title(title_tag.get('content'))
            return "Ao Vivo"
    except requests.exceptions.RequestException as e:
        print(f"  - AVISO: Falha ao verificar YouTube ({channel_url}). Erro: {e}")
    return None

def get_kick_live_title(channel_url: str) -> Union[str, None]:
    try:
        slug = channel_url.split('/')[-1]
        api_url = f"https://kick.com/api/v2/channels/{slug}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('livestream'):
            return data['livestream'].get('session_title', 'Ao Vivo')
    except requests.exceptions.RequestException as e:
        print(f"  - AVISO: Falha ao verificar Kick ({channel_url}). Erro: {e}")
    return None

def get_twitch_live_title(channel_url: str) -> Union[str, None]:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(channel_url, headers=headers, timeout=10)
        response.raise_for_status()
        if 'isLiveBroadcast' in response.text:
            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.select_one('h1[data-a-target="stream-title"], h2[data-a-target="stream-title"]')
            if title_tag:
                return title_tag.text
            return "Ao Vivo"
    except requests.exceptions.RequestException as e:
        print(f"  - AVISO: Falha ao verificar Twitch ({channel_url}). Erro: {e}")
    return None

# Mapeia a plataforma ao seu respectivo verificador
PLATFORM_CHECKERS = {
    'youtube': get_youtube_live_title,
    'kick': get_kick_live_title,
    'twitch': get_twitch_live_title,
}