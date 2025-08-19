# gerador_playlist/live_finder.py

import os
import sys
from datetime import datetime, timedelta

import pytz
import yt_dlp
from yt_dlp import utils as yt_dlp_utils

# --- CONFIGURAÇÕES ---
INPUT_FILE = 'links.txt'
VIDEOS_A_VERIFICAR = 50
FALLBACK_VIDEO_URL = "https://www.youtube.com/watch?v=9pudYN0rJnk"


def write_fallback_stream(channel_name: str, channel_id: str, category: str, m3u8_lines: list):
    """Adiciona um stream de fallback à lista de linhas M3U8."""
    print(f"INFO: Nenhuma live ativa para '{channel_name}'. Usando fallback.")
    # ALTERADO: group-title agora é "Streams"
    m3u8_lines.append(
        f'#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{channel_name} (Offline)" group-title="Streams",{channel_name} (Offline)')
    m3u8_lines.append(FALLBACK_VIDEO_URL)


def process_youtube_channel(url: str, name: str, channel_id: str, category: str, m3u8_lines: list):
    """Processa um canal do YouTube e adiciona as lives encontradas à lista."""
    exclusion_filter = yt_dlp_utils.match_filter_func("live_status != 'is_upcoming' & live_status != 'was_live'")
    ydl_opts = {'quiet': True, 'no_warnings': True, 'match_filter': exclusion_filter, 'playlistend': VIDEOS_A_VERIFICAR}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            live_videos = [v for v in playlist_info.get('entries', []) if v and v.get('is_live')]

            if not live_videos:
                write_fallback_stream(name, channel_id, category, m3u8_lines)
                return

            for index, video_info in enumerate(live_videos, 1):
                display_name = f"{name} {index}" if len(live_videos) > 1 else name
                manifest_url = next((f['url'] for f in reversed(video_info.get('formats', [])) if
                                     f.get('protocol') == 'm3u8_native' and f.get('vcodec') != 'none'), None)
                if manifest_url:
                    # ALTERADO: group-title agora é "Streams"
                    m3u8_lines.append(
                        f'#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{display_name}" group-title="Streams",{display_name}')
                    m3u8_lines.append(manifest_url)
    except Exception as e:
        print(f"DEBUG: Erro ao processar canal '{name}': {e}")
        write_fallback_stream(name, channel_id, category, m3u8_lines)


def process_single_stream(url: str, name: str, channel_id: str, category: str, m3u8_lines: list):
    """Processa streams únicos (Twitch/Kick)."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            if info.get('is_live'):
                manifest_url = next((f['url'] for f in reversed(info.get('formats', [])) if
                                     f.get('protocol') == 'm3u8_native' and f.get('vcodec') != 'none'), None)
                if manifest_url:
                    # ALTERADO: group-title agora é "Streams"
                    m3u8_lines.append(
                        f'#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{name}" group-title="Streams",{name}')
                    m3u8_lines.append(manifest_url)
                else:
                    write_fallback_stream(name, channel_id, category, m3u8_lines)
            else:
                write_fallback_stream(name, channel_id, category, m3u8_lines)
    except Exception:
        write_fallback_stream(name, channel_id, category, m3u8_lines)


def gerar_m3u8_dinamico():
    """Função principal que lê links.txt e retorna o conteúdo M3U8 como string."""
    m3u8_lines = []
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            channel_name, channel_id, category = '', '', ''
            for line in f:
                line = line.strip()
                if not line or line.startswith('##'): continue
                if line.startswith('https:'):
                    if not all([channel_name, channel_id, category]): continue

                    if 'youtube.com' in line:
                        url = line.split('/live')[0].rstrip('/') + '/streams'
                        process_youtube_channel(url, channel_name, channel_id, category, m3u8_lines)
                    elif 'twitch.tv' in line or 'kick.com' in line:
                        process_single_stream(line, channel_name, channel_id, category, m3u8_lines)
                else:
                    parts = line.split('||')
                    if len(parts) == 3:
                        channel_name, channel_id, category = parts[0].strip(), parts[1].strip(), parts[
                            2].strip().title()

    except FileNotFoundError:
        print(f"AVISO: Arquivo '{INPUT_FILE}' não encontrado. Pulando a busca por lives dinâmicas.")
        return ""

    return "\n".join(m3u8_lines)