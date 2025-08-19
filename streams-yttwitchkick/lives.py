#! /usr/bin-python3
import os
import sys
from datetime import datetime, timedelta

import pytz
from lxml import etree
import yt_dlp
from yt_dlp import utils as yt_dlp_utils

# --- CONFIGURAÇÕES GLOBAIS ---
INPUT_FILE = 'links.txt'
OUTPUT_M3U8_FILE = 'lives.m3u8'
OUTPUT_EPG_FILE = 'epg.xml'
FALLBACK_VIDEO_URL = "https://www.youtube.com/watch?v=9pudYN0rJnk"
VIDEOS_A_VERIFICAR = 50

tz = pytz.timezone('Europe/London')
channels = []


def generate_times(curr_dt: datetime):
    last_hour = curr_dt.replace(microsecond=0, second=0, minute=0)
    last_hour = tz.localize(last_hour)
    start_dates = [last_hour]
    for x in range(7):
        last_hour += timedelta(hours=3)
        start_dates.append(last_hour)
    end_dates = start_dates[1:]
    end_dates.append(start_dates[-1] + timedelta(hours=3))
    return start_dates, end_dates


def build_xml_tv(streams: list) -> bytes:
    data = etree.Element("tv")
    data.set("generator-info-name", "youtube-live-epg")
    data.set("generator-info-url", "https://github.com/dp247/YouTubeToM3U8")
    for stream in streams:
        channel = etree.SubElement(data, "channel")
        channel.set("id", stream[1])
        name = etree.SubElement(channel, "display-name")
        name.set("lang", "en")
        name.text = stream[0]
        dt_format = '%Ym%d%H%M%S %z'
        start_dates, end_dates = generate_times(datetime.now())
        for idx, val in enumerate(start_dates):
            programme = etree.SubElement(data, 'programme')
            programme.set("channel", stream[1])
            programme.set("start", val.strftime(dt_format))
            programme.set("stop", end_dates[idx].strftime(dt_format))
            title = etree.SubElement(programme, "title")
            title.set('lang', 'en')
            title.text = stream[3] if stream[3] else f'LIVE: {stream[0]}'
            description = etree.SubElement(programme, "desc")
            description.set('lang', 'en')
            description.text = stream[4] if stream[4] else 'No description provided'
            icon = etree.SubElement(programme, "icon")
            icon.set('src', stream[5])
    return etree.tostring(data, pretty_print=True, encoding='utf-8')


def write_fallback_stream(channel_name: str, channel_id: str, category: str):
    print(f"INFO: Nenhuma live ativa encontrada para '{channel_name}'. Usando fallback.")
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(FALLBACK_VIDEO_URL, download=False)
            fallback_manifest_url = next((f['url'] for f in reversed(info.get('formats', [])) if
                                          f.get('protocol') == 'm3u8_native' and f.get('vcodec') != 'none'), None)
            if fallback_manifest_url:
                with open(OUTPUT_M3U8_FILE, 'a', encoding='utf-8') as m3u8_file:
                    m3u8_file.write(
                        f'\n#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{channel_name} (Offline)" group-title="{category}", {channel_name} (Offline)\n')
                    m3u8_file.write(f"{fallback_manifest_url}\n")
    except Exception as fallback_e:
        print(f"ERRO: Falha crítica ao obter o M3U8 do vídeo de fallback. {fallback_e}")


def process_youtube_channel(channel_url: str, channel_name: str, channel_id: str, category: str):
    """Usa um filtro de exclusão com a sintaxe correta para ser rápido e preciso."""

    # Filtro de exclusão com a sintaxe mais simples e direta possível.
    exclusion_filter = yt_dlp_utils.match_filter_func("live_status != 'is_upcoming' & live_status != 'was_live'")

    ydl_opts = {
        'quiet': True, 'no_warnings': True,
        'match_filter': exclusion_filter,
        'playlistend': VIDEOS_A_VERIFICAR,
    }
    found_live_stream = False
    try:
        print(f"INFO: Canal '{channel_name}' - Buscando lives com filtro de exclusão (rápido)...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(channel_url, download=False)

            candidate_videos = playlist_info.get('entries', [])

            if candidate_videos:
                print(f"INFO: {len(candidate_videos)} candidato(s) encontrado(s) após o filtro.")
                for video_info in candidate_videos:
                    if video_info and video_info.get('is_live'):
                        video_title = video_info.get('title', channel_name)
                        print(f"INFO: LIVE ENCONTRADA! '{channel_name}': {video_title}")
                        manifest_url = next((f['url'] for f in reversed(video_info.get('formats', [])) if
                                             f.get('protocol') == 'm3u8_native' and f.get('vcodec') != 'none'), None)
                        if manifest_url:
                            found_live_stream = True
                            with open(OUTPUT_M3U8_FILE, 'a', encoding='utf-8') as m3u8_file:
                                m3u8_file.write(
                                    f'\n#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{video_title}" group-title="{category}", {video_title}\n')
                                m3u8_file.write(f"{manifest_url}\n")
                            channels.append((video_title, channel_id, category, video_info.get('title'),
                                             video_info.get('description'), video_info.get('thumbnail')))
    except Exception as e:
        # Erros podem acontecer se o filtro não encontrar nada ou se houver um problema de rede.
        print(f"DEBUG: Ocorreu uma exceção controlada no processamento do canal '{channel_name}': {e}")

    if not found_live_stream:
        write_fallback_stream(channel_name, channel_id, category)


def process_single_stream(stream_url: str, channel_name: str, channel_id: str, category: str):
    """Lógica para plataformas de stream único (Twitch, Kick)."""
    ydl_opts = {'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(stream_url, download=False)
            if info.get('is_live'):
                stream_title = info.get('title', channel_name)
                print(f"INFO: Live [Twitch/Kick] encontrada em '{channel_name}': {stream_title}")
                manifest_url = next((f['url'] for f in reversed(info.get('formats', [])) if
                                     f.get('protocol') == 'm3u8_native' and f.get('vcodec') != 'none'), None)
                if manifest_url:
                    with open(OUTPUT_M3U8_FILE, 'a', encoding='utf-8') as m3u8_file:
                        m3u8_file.write(
                            f'\n#EXTINF:-1 tvg-id="{channel_id}" tvg-name="{stream_title}" group-title="{category}", {stream_title}\n')
                        m3u8_file.write(f"{manifest_url}\n")
                    channels.append((stream_title, channel_id, category, info.get('title'), info.get('description'),
                                     info.get('thumbnail')))
                else:
                    write_fallback_stream(channel_name, channel_id, category)
            else:
                write_fallback_stream(channel_name, channel_id, category)
    except Exception:
        write_fallback_stream(channel_name, channel_id, category)


if __name__ == "__main__":
    print("Atualizando yt-dlp para a versão mais recente...")
    os.system(f'"{sys.executable}" -m pip install --upgrade yt-dlp')
    print("Atualização concluída.\n")

    if os.path.exists(OUTPUT_M3U8_FILE):
        os.remove(OUTPUT_M3U8_FILE)
    try:
        with open(f'./{INPUT_FILE}', encoding='utf-8') as f:
            with open(OUTPUT_M3U8_FILE, 'a', encoding='utf-8') as m3u8_file:
                m3u8_file.write("#EXTM3U\n")
            f.seek(0)
            channel_name, channel_id, category = '', '', ''
            for line in f:
                line = line.strip()
                if not line or line.startswith('##'): continue
                if line.startswith('https:'):
                    if not all([channel_name, channel_id, category]): continue

                    if 'youtube.com' in line:
                        url = line.split('/live')[0].split('/featured')[0]
                        if not url.endswith('/streams'):
                            url = url.rstrip('/') + '/streams'
                        process_youtube_channel(url, channel_name, channel_id, category)
                    elif 'twitch.tv' in line or 'kick.com' in line:
                        process_single_stream(line, channel_name, channel_id, category)
                    else:
                        print(f"AVISO: Plataforma não suportada: {line}")
                else:
                    parts = line.split('||')
                    if len(parts) == 3:
                        channel_name, channel_id, category = parts[0].strip(), parts[1].strip(), parts[
                            2].strip().title()
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{INPUT_FILE}' não foi encontrado.")
        exit()

    if channels:
        print(f"\nGerando arquivo EPG para {len(channels)} stream(s) ao vivo...")
        channel_xml = build_xml_tv(channels)
        with open(OUTPUT_EPG_FILE, 'wb') as f:
            f.write(channel_xml)
    print(f"\nProcesso concluído. Arquivo '{OUTPUT_M3U8_FILE}' gerado.")