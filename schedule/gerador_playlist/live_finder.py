# gerador_playlist/live_finder.py

import os
import sys
from datetime import datetime, timedelta

import pytz
import yt_dlp
from yt_dlp import utils as yt_dlp_utils

# Importa a lista de canais estáticos do arquivo de configuração
from .config import STATIC_CHANNELS

# --- CONFIGURAÇÕES ---
VIDEOS_A_VERIFICAR = 100

def process_youtube_channel(url: str, name: str, channel_id: str, category: str, m3u8_lines: list):
    """Processa um canal do YouTube com lógica aprimorada para priorizar o manifesto mestre (suporte a 4K)."""

    # Usando o seu filtro original e mais confiável para pegar apenas lives ativas
    exclusion_filter = yt_dlp_utils.match_filter_func("is_live & live_status != 'is_upcoming' & live_status != 'was_live' & live_status = 'is_live'")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'playlistend': VIDEOS_A_VERIFICAR,
        'ignoreerrors': False,  # Alterado para False para que a exceção seja lançada
        'match_filter': exclusion_filter
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False, process=True)

            live_videos = [e for e in playlist_info.get('entries', []) if e is not None]

            if not live_videos:
                print(f"INFO: Nenhuma live ativa para '{name}'.")
                return

            for index, video_info in enumerate(live_videos, 1):
                display_name = f"{name} {index}" if len(live_videos) > 1 else name

                for index, video_info in enumerate(live_videos, 1):
                    live_title = video_info.get('title', 'Live Stream')

                    if 'rerun' not in live_title.lower():
                        current_tvg_id = f"{channel_id.split('.')[0]}{index}.{channel_id.split('.')[-1]}" if len(live_videos) > 1 else channel_id

                        manifest_url = None

                        top_level_manifest = video_info.get('manifest_url')
                        if top_level_manifest and top_level_manifest.endswith('.m3u8'):
                            manifest_url = top_level_manifest
                            print(f"INFO: Stream '{display_name}' selecionada")

                        if manifest_url:
                            m3u8_lines.append(f'#EXTINF:-1 tvg-id="{current_tvg_id}" tvg-name="{display_name}" group-title="Streams",{display_name}')
                            m3u8_lines.append(manifest_url)
                        else:
                            print(f"AVISO: Nenhum stream M3U8 válido encontrado para '{display_name}'.")

                    else:
                        print(f"Ignorando, pois é um rerun: '{display_name}'")

    except yt_dlp.utils.DownloadError as e:
        # Trata o erro específico de lives agendadas, que não são capturadas pelo filtro
        if 'This live event will begin' in str(e):
            print(f"INFO: Ignorando live agendada para o canal '{name}'.")
        else:
            print(f"DEBUG: Erro de download ao processar o canal '{name}': {e}")
    except Exception as e:
        print(f"DEBUG: Erro ao processar canal '{name}': {e}")


def process_single_stream(url: str, name: str, channel_id: str, category: str, m3u8_lines: list):
    """Processa streams únicos (Twitch/Kick), que já usam a lógica correta."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            if info.get('is_live'):
                m3u8_formats = [
                    f for f in info.get('formats', [])
                    if f.get('protocol') in ('m3u8', 'm3u8_native') and f.get('vcodec') != 'none' and f.get(
                        'acodec') != 'none'
                ]
                if m3u8_formats:
                    m3u8_formats.sort(key=lambda f: f.get('height', 0), reverse=True)
                    manifest_url = m3u8_formats[0]['url']
                    print(
                        f"INFO: Stream '{name}' encontrada. Melhor qualidade com áudio: {m3u8_formats[0].get('height')}p")
                    m3u8_lines.append(
                        f'#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{name}" group-title="Streams",{name}')
                    m3u8_lines.append(manifest_url)
                else:
                    print(f"INFO: Nenhuma stream com áudio encontrada para '{name}'.")
            else:
                print(f"INFO: Stream '{name}' não está ao vivo.")
    except Exception as e:
        print(f"DEBUG: Erro ao processar stream '{name}': {e}")


def gerar_m3u8_dinamico():
    """Função principal que itera sobre os canais estáticos e retorna o conteúdo M3U8 como string."""
    m3u8_lines = []
    print("INFO: Iniciando a busca por lives dinâmicas a partir da configuração.")

    for channel in STATIC_CHANNELS:
        name = channel.get("name")
        channel_id = channel.get("id")
        platform = channel.get("platform")
        url = channel.get("url")
        category = "Live"  # A categoria é fixa para "Streams" no M3U8

        if not all([name, channel_id, platform, url]):
            print(f"AVISO: Entrada de canal incompleta na configuração, pulando: {channel}")
            continue

        print(f"INFO: Processando canal '{name}' da plataforma '{platform}'.")

        if platform == 'youtube':
            # A URL do YouTube precisa terminar em /streams para o yt-dlp encontrar os vídeos
            streams_url = url.split('/live')[0].rstrip('/') + '/streams'
            process_youtube_channel(streams_url, name, channel_id, category, m3u8_lines)
        elif platform in ['twitch', 'kick']:
            process_single_stream(url, name, channel_id, category, m3u8_lines)
        else:
            print(f"AVISO: Plataforma '{platform}' não suportada para o canal '{name}'.")

    if not m3u8_lines:
        print("AVISO: Nenhuma live dinâmica foi encontrada ou processada.")

    return "\n".join(m3u8_lines)
