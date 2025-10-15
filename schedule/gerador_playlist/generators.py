# gerador_playlist/generators.py

import html
import re
from datetime import datetime, timedelta, timezone
from typing import List, Dict

# Adicionando novas importações para verificação de live
import yt_dlp
from yt_dlp import utils as yt_dlp_utils

# Importando módulos do nosso pacote
from . import config
from .utils import sanitize_id


def generate_m3u8_content(stream_list: List[Dict]) -> str:
    """Gera o conteúdo do arquivo M3U8 a partir da lista de streams dinâmicos."""
    m3u8_lines = ["#EXTM3U"]
    if not stream_list:
        print("\nNenhum stream dinâmico encontrado para o M3U8.")
        return "\n".join(m3u8_lines)

    print("\nOrdenando streams dinâmicos e gerando M3U8...")
    sort_map = {group.lower(): i for i, group in enumerate(config.GROUP_SORT_ORDER)}
    stream_list.sort(key=lambda s: (
        s['sport'].lower() not in sort_map,
        sort_map.get(s['sport'].lower(), float('inf')),
        s['sport'].lower(),
        int(s['start_timestamp_ms'])
    ))
    for stream in stream_list:
        unique_event_id = sanitize_id(f"evt.{stream['source_name']}.{stream['start_timestamp_ms']}")
        display_title = f"{stream['event_name']}"
        extinf = (f'#EXTINF:-1 tvg-id="{unique_event_id}" tvg-logo="{stream["logo_url"]}" '
                  f'group-title="{stream["sport"]}",{display_title}')
        m3u8_lines.extend([extinf, stream['stream_url']])
    return "\n".join(m3u8_lines)


# --- Funções de Geração de EPG (Completas) ---

def get_live_videos(channel: Dict) -> List[Dict]:
    """
    Verifica um canal (YouTube, Twitch, Kick) e retorna uma lista de dicionários de vídeos ao vivo.
    Usa a lógica de yt-dlp para encontrar streams ativos.
    """
    platform = channel.get("platform")
    url = channel.get("url")
    name = channel.get("name")
    live_videos = []

    if not all([platform, url, name]):
        return []

    print(f"- Verificando {name} ({platform})...")

    try:
        if platform == 'youtube':
            exclusion_filter = yt_dlp_utils.match_filter_func("is_live & live_status != 'is_upcoming' & live_status != 'was_live' & live_status = 'is_live'")
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'playlistend': 100,  # Verifica um número razoável de vídeos
                'ignoreerrors': False,
                'match_filter': exclusion_filter
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(url, download=False, process=True)
                live_videos = [e for e in playlist_info.get('entries', []) if e is not None]

        elif platform in ['twitch', 'kick']:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info.get('is_live'):
                    live_videos.append(info)

    except yt_dlp.utils.DownloadError as e:
        # Trata o erro específico de lives agendadas, que não são capturadas pelo filtro
        if 'This live event will begin' in str(e):
            print(f"INFO: Ignorando live agendada para o canal '{name}'.")
        else:
            print(f"DEBUG: Erro de download ao processar o canal '{name}': {e}")
    except Exception as e:
        print(f"  -> AVISO: Erro ao verificar o canal '{name}': {e}")

    return live_videos


def _generate_static_channels_epg(xml_lines: List[str]):
    """
    Gera as entradas de canal e programação para a lista de canais estáticos,
    usando uma verificação de live aprimorada com yt-dlp e tratando múltiplos streams.
    """
    print("\nVerificando status dos canais estáticos para o EPG...")

    for channel in config.STATIC_CHANNELS:
        base_channel_id = channel["id"]
        base_channel_name = channel["name"]
        base_channel_logo = channel["logo"]

        live_videos = get_live_videos(channel)
        now_utc = datetime.now(timezone.utc)

        # Se não houver lives, gera um único canal offline para o ID base
        if not live_videos:
            print(f"  -> {base_channel_name} está offline.")
            continue

        # Se houver uma ou mais lives, processa cada uma
        print(f"  -> {base_channel_name} está AO VIVO com {len(live_videos)} stream(s).")
        for index, video_info in enumerate(live_videos, 1):
            is_multi_stream = len(live_videos) > 1
            display_name = f"{base_channel_name} {index}" if is_multi_stream else base_channel_name
            
            if is_multi_stream:
                id_parts = base_channel_id.split('.')
                current_tvg_id = f"{id_parts[0]}{index}.{id_parts[-1]}"
            else:
                current_tvg_id = base_channel_id

            live_title = video_info.get('title', 'Live Stream')
            live_title = _format_title(live_title)

            # Adiciona a definição do canal para cada stream
            xml_lines.append(f'  <channel id="{current_tvg_id}">')
            xml_lines.append(f'    <display-name>{html.escape(display_name)}</display-name>')
            xml_lines.append(f'    <icon src="{html.escape(base_channel_logo)}" />')
            xml_lines.append('  </channel>')

            # Gera a programação para o canal específico
            event_start_utc = now_utc
            event_end_utc = event_start_utc + timedelta(hours=config.EPG_EVENT_DURATION_HOURS)
            now_local = now_utc.astimezone(config.LOCAL_TZ)
            local_day_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
            day_start_utc = local_day_start.astimezone(timezone.utc)
            local_day_end = local_day_start + timedelta(days=1)
            day_end_utc = local_day_end.astimezone(timezone.utc)

            if event_start_utc > day_start_utc:
                day_start_utc = day_start_utc - timedelta(days=1)
                start_str = day_start_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = event_start_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{current_tvg_id}">')
                xml_lines.append(f'    <title lang="pt">{config.PLACEHOLDER_TEXT}</title>')
                xml_lines.append('  </programme>')

            start_str = event_start_utc.strftime('%Y%m%d%H%M%S %z')
            stop_str = event_end_utc.strftime('%Y%m%d%H%M%S %z')
            safe_prog_title = html.escape(live_title)
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{current_tvg_id}">')
            xml_lines.append(f'    <title lang="pt">{safe_prog_title}</title>')
            xml_lines.append(f'    <desc lang="pt">{safe_prog_title}</desc>')
            xml_lines.append('  </programme>')

            if event_end_utc < day_end_utc:
                start_str = event_end_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = day_end_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{current_tvg_id}">')
                xml_lines.append(f'    <title lang="pt">{config.PLACEHOLDER_TEXT}</title>')
                xml_lines.append('  </programme>')


def _generate_dynamic_streams_epg(xml_lines: List[str], stream_list: List[Dict]):
    """
    Gera as entradas de canal e programação para a lista de streams dinâmicos.
    (Função interna, chamada por generate_xmltv_epg)
    """
    if not stream_list:
        print("\nNenhum stream dinâmico para adicionar ao EPG.")
        return

    print("\nAdicionando canais dinâmicos ao EPG...")
    generated_channel_ids = set()

    for stream in stream_list:
        try:
            unique_event_id = sanitize_id(f"evt.{stream['source_name']}.{stream['start_timestamp_ms']}")
            if unique_event_id not in generated_channel_ids:
                xml_lines.append(f'  <channel id="{unique_event_id}">')
                xml_lines.append(f'    <display-name>{html.escape(stream["source_name"])}</display-name>')
                xml_lines.append(f'    <icon src="{html.escape(stream["logo_url"])}" />')
                xml_lines.append('  </channel>')
                generated_channel_ids.add(unique_event_id)

            timestamp_ms = int(stream['start_timestamp_ms'])
            start_dt_utc = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            
            if stream['sport'] == "Futebol":
                duration_hours = config.EPG_EVENT_DURATION_HOURS_FUTEBOL
            else:
                duration_hours = config.EPG_EVENT_DURATION_HOURS
            end_dt_utc = start_dt_utc + timedelta(hours=duration_hours)

            start_dt_local = start_dt_utc.astimezone(config.LOCAL_TZ)
            local_day_start = start_dt_local.replace(hour=0, minute=0, second=0, microsecond=0)
            day_start_utc = local_day_start.astimezone(timezone.utc)
            local_day_end = local_day_start + timedelta(days=1)
            day_end_utc = local_day_end.astimezone(timezone.utc)

            safe_event_name = html.escape(stream['event_name'])
            safe_channel_name = html.escape(stream['source_name'])

            if start_dt_utc > day_start_utc:
                day_start_utc_mod = day_start_utc - timedelta(days=1)
                start_str = day_start_utc_mod.strftime('%Y%m%d%H%M%S %z')
                stop_str = start_dt_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
                xml_lines.append('    <title lang="pt">Não iniciado</title>')
                xml_lines.append('  </programme>')

            start_str = start_dt_utc.strftime('%Y%m%d%H%M%S %z')
            stop_str = end_dt_utc.strftime('%Y%m%d%H%M%S %z')
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
            xml_lines.append(f'    <title lang="pt">{safe_channel_name}</title>')
            xml_lines.append(f'    <desc lang="pt">{safe_event_name}</desc>')
            xml_lines.append('  </programme>')

            if end_dt_utc < day_end_utc:
                day_end_utc_mod = day_end_utc + timedelta(days=1)
                start_str = end_dt_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = day_end_utc_mod.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
                xml_lines.append('    <title lang="pt">Finalizado</title>')
                xml_lines.append('  </programme>')

        except (ValueError, TypeError) as e:
            print(f"AVISO: Pulando evento dinâmico no EPG devido a erro de dados: {e}")
            continue

def _format_title(title: str) -> str:
    if not title: return "Ao Vivo"
    pattern = r'(?:ao vivo(?: e com imagens)?|com imagens):?\s*\|?\s*|\s*\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}$'
    cleaned_title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()
    title = cleaned_title.title() if cleaned_title else "Ao Vivo"
    return title

def generate_xmltv_epg(stream_list: List[Dict]) -> str:
    """Orquestra a geração do arquivo EPG completo chamando as funções especializadas."""
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']

    _generate_static_channels_epg(xml_lines)
    _generate_dynamic_streams_epg(xml_lines, stream_list)

    xml_lines.append('</tv>')
    return "\n".join(xml_lines)
