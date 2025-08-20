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
VIDEOS_A_VERIFICAR = 35
FALLBACK_VIDEO_URL = "https://www.youtube.com/watch?v=9pudYN0rJnk"


def write_fallback_stream(channel_name: str, channel_id: str, category: str, m3u8_lines: list):
    """Adiciona um stream de fallback à lista de linhas M3U8."""
    print(f"INFO: Nenhuma live ativa para '{channel_name}'. Usando fallback.")
    m3u8_lines.append(
        f'#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{channel_name} (Offline)" group-title="Streams",{channel_name} (Offline)')
    m3u8_lines.append(FALLBACK_VIDEO_URL)


def process_youtube_channel(url: str, name: str, channel_id: str, category: str, m3u8_lines: list):
    """Processa um canal do YouTube com a lógica de filtragem original e seleção flexível em Python."""

    # Usando o seu filtro original e mais confiável para pegar apenas lives ativas
    exclusion_filter = yt_dlp_utils.match_filter_func("live_status != 'is_upcoming' & live_status != 'was_live'")

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'playlistend': VIDEOS_A_VERIFICAR,
        'ignoreerrors': True,
        'match_filter': exclusion_filter  # Filtro para pegar apenas o que está ao vivo agora
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False, process=True)

            live_videos = [e for e in playlist_info.get('entries', []) if e is not None]

            if not live_videos:
                write_fallback_stream(name, channel_id, category, m3u8_lines)
                return

            for index, video_info in enumerate(live_videos, 1):
                # Lógica para o nome de exibição e ID da TVG
                display_name = f"{name} {index}" if len(live_videos) > 1 else name
                # NOVA LÓGICA: Adiciona o número ao ID se houver mais de uma live
                current_tvg_id = f"{channel_id.split('.')[0]}{index}.{channel_id.split('.')[-1]}" if len(live_videos) > 1 else channel_id

                formats = video_info.get('formats', [])
                manifest_url = None

                # --- LÓGICA DE SELEÇÃO FINAL EM DUAS ETAPAS ---

                # 1. Tenta encontrar os melhores formatos com ÁUDIO E VÍDEO
                combined_formats = [
                    f for f in formats
                    if f.get('protocol') in ('m3u8', 'm3u8_native') and f.get('vcodec') != 'none' and f.get(
                        'acodec') != 'none'
                ]

                if combined_formats:
                    # Se encontrou, ordena por resolução e pega o melhor
                    combined_formats.sort(key=lambda f: f.get('height', 0), reverse=True)
                    best_format = combined_formats[0]
                    manifest_url = best_format['url']
                    print(
                        f"INFO: Stream '{display_name}' selecionada. Qualidade: {best_format.get('resolution', 'N/A')} (Áudio: True)")
                else:
                    # 2. Se não encontrou NENHUM com áudio e vídeo, pega o melhor com APENAS VÍDEO como fallback
                    video_only_formats = [
                        f for f in formats
                        if f.get('protocol') in ('m3u8', 'm3u8_native') and f.get('vcodec') != 'none'
                    ]
                    if video_only_formats:
                        video_only_formats.sort(key=lambda f: f.get('height', 0), reverse=True)
                        best_format = video_only_formats[0]
                        manifest_url = best_format['url']
                        print(
                            f"AVISO: Nenhuma stream com áudio encontrada para '{display_name}'. Usando fallback de vídeo. Qualidade: {best_format.get('resolution', 'N/A')}")

                if manifest_url:
                    m3u8_lines.append(
                        # USA O NOVO TVG ID AQUI
                        f'#EXTINF:-1 tvg-id="{current_tvg_id}" tvg-name="{display_name}" group-title="Streams",{display_name}')
                    m3u8_lines.append(manifest_url)
                else:
                    print(f"AVISO: Nenhum stream M3U8 válido encontrado para '{display_name}'.")

    except Exception as e:
        print(f"DEBUG: Erro ao processar canal '{name}': {e}")
        write_fallback_stream(name, channel_id, category, m3u8_lines)


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
                    write_fallback_stream(name, channel_id, category, m3u8_lines)
            else:
                write_fallback_stream(name, channel_id, category, m3u8_lines)
    except Exception:
        write_fallback_stream(name, channel_id, category, m3u8_lines)


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
