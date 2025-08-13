# gerador_playlist/generators.py

import html
from datetime import datetime, timedelta, timezone
from typing import List, Dict

# Importando módulos do nosso pacote
from . import config
from . import platform_checkers
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

def _generate_static_channels_epg(xml_lines: List[str]):
    """
    Gera as entradas de canal e programação para a lista de canais estáticos.
    (Função interna, chamada por generate_xmltv_epg)
    """
    print("\nVerificando status dos canais estáticos para o EPG...")

    for channel in config.STATIC_CHANNELS:
        print(f"- Verificando {channel['name']} ({channel['platform']})...")
        checker_func = platform_checkers.PLATFORM_CHECKERS.get(channel['platform'])
        live_title = checker_func(channel['url']) if checker_func else None

        # Adiciona a definição do canal ao XML
        xml_lines.append(f'  <channel id="{channel["id"]}">')
        xml_lines.append(f'    <display-name>{html.escape(channel["name"])}</display-name>')
        xml_lines.append(f'    <icon src="{html.escape(channel["logo"])}" />')
        xml_lines.append('  </channel>')

        now_utc = datetime.now(timezone.utc)
        if live_title:
            print(f"  -> {channel['name']} está AO VIVO: {live_title}")
            event_start_utc = now_utc
            event_end_utc = event_start_utc + timedelta(hours=config.EPG_EVENT_DURATION_HOURS)
            now_local = now_utc.astimezone(config.LOCAL_TZ)
            local_day_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
            local_day_end = local_day_start + timedelta(days=1)
            day_start_utc = local_day_start.astimezone(timezone.utc)
            day_end_utc = local_day_end.astimezone(timezone.utc)

            # Placeholder para antes do evento ao vivo (se aplicável)
            if event_start_utc > day_start_utc:
                day_start_utc = day_start_utc - timedelta(days=1)
                start_str = day_start_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = event_start_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
                xml_lines.append(f'    <title lang="pt">{config.PLACEHOLDER_TEXT}</title>')
                xml_lines.append('  </programme>')

            # Programa do evento ao vivo
            start_str = event_start_utc.strftime('%Y%m%d%H%M%S %z')
            stop_str = event_end_utc.strftime('%Y%m%d%H%M%S %z')
            safe_prog_title = html.escape(live_title)
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
            xml_lines.append(f'    <title lang="pt">{safe_prog_title}</title>')
            xml_lines.append(f'    <desc lang="pt">{safe_prog_title}</desc>')
            xml_lines.append('  </programme>')

            # Placeholder para depois do evento ao vivo
            if event_end_utc < day_end_utc:
                start_str = event_end_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = day_end_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
                xml_lines.append(f'    <title lang="pt">{config.PLACEHOLDER_TEXT}</title>')
                xml_lines.append('  </programme>')
        else:
            # Se o canal está offline, cria um único placeholder longo
            print(f"  -> {channel['name']} está offline.")
            start_str = now_utc.strftime('%Y%m%d%H%M%S %z')
            now_local = now_utc.astimezone(config.LOCAL_TZ)
            local_day_end = now_local.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            day_end_utc = local_day_end.astimezone(timezone.utc)
            stop_str = day_end_utc.strftime('%Y%m%d%H%M%S %z')
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
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
            end_dt_utc = start_dt_utc + timedelta(hours=config.EPG_EVENT_DURATION_HOURS)

            start_dt_local = start_dt_utc.astimezone(config.LOCAL_TZ)
            local_day_start = start_dt_local.replace(hour=0, minute=0, second=0, microsecond=0)
            day_start_utc = local_day_start.astimezone(timezone.utc)
            local_day_end = local_day_start + timedelta(days=1)
            day_end_utc = local_day_end.astimezone(timezone.utc)

            safe_event_name = html.escape(stream['event_name'])
            safe_channel_name = html.escape(stream['source_name'])

            # Placeholder 'Não iniciado'
            if start_dt_utc > day_start_utc:
                day_start_utc_mod = day_start_utc - timedelta(days=1)
                start_str = day_start_utc_mod.strftime('%Y%m%d%H%M%S %z')
                stop_str = start_dt_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
                xml_lines.append('    <title lang="pt">Não iniciado</title>')
                xml_lines.append('  </programme>')

            # Programa do evento principal
            start_str = start_dt_utc.strftime('%Y%m%d%H%M%S %z')
            stop_str = end_dt_utc.strftime('%Y%m%d%H%M%S %z')
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
            xml_lines.append(f'    <title lang="pt">{safe_channel_name}</title>')
            xml_lines.append(f'    <desc lang="pt">{safe_event_name}</desc>')
            xml_lines.append('  </programme>')

            # Placeholder 'Finalizado'
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


def generate_xmltv_epg(stream_list: List[Dict]) -> str:
    """Orquestra a geração do arquivo EPG completo chamando as funções especializadas."""
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']

    _generate_static_channels_epg(xml_lines)
    _generate_dynamic_streams_epg(xml_lines, stream_list)

    xml_lines.append('</tv>')
    return "\n".join(xml_lines)