# Localização: gerador_playlist/scraper.py

import re
import json
from datetime import datetime, timezone
import pytz  # ### ALTERADO ###: Importamos a biblioteca pytz
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Importando de outros módulos do nosso pacote
from . import config
from .utils import find_best_logo_url


def _parse_date_from_key(date_key: str):  # ### ALTERADO ###: Removido o tipo de retorno para permitir None
    """Extrai e converte a data a partir da chave do JSON (ex: 'Monday 12 Aug 2024')."""
    try:  # ### ALTERADO ###: Envolvemos em um try/except mais robusto
        date_str_part = date_key.split(' - ')[0]
        date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_part)
        possible_formats = ['%A %d %b %Y', '%A %d %B %Y']
        for date_format in possible_formats:
            try:
                return datetime.strptime(date_str_cleaned, date_format).date()
            except ValueError:
                continue
        raise ValueError("Nenhum formato de data correspondeu")  # ### ALTERADO ###
    except (ValueError, IndexError):  # ### ALTERADO ###
        print(f"AVISO: Não foi possível parsear a data '{date_key}'. Pulando os eventos deste dia.")
        return None  # ### ALTERADO ###: Retornamos None em caso de falha


def _reformat_event_name(original_name: str) -> str:
    """Re-formata o nome do evento para 'Partida : Liga'."""
    try:
        league_part, match_part_full = original_name.split(':', 1)
        match_part = match_part_full.split('(', 1)[0] if '(' in match_part_full else match_part_full
        return f"{match_part.strip()} : {league_part.strip()}"
    except (ValueError, IndexError):
        return original_name


def extract_streams_with_selenium(driver: webdriver.Chrome, url: str, logo_cache: dict) -> list:
    """
    Navega até a URL, aguarda o carregamento, extrai o JSON da página,
    e o transforma em uma lista estruturada de streams.
    """
    print(f"Navegando para: {url} com o Selenium...")
    driver.get(url)
    try:
        WebDriverWait(driver, 60).until_not(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), 'Carregando...'))
        print("Página carregada. Extraindo dados...")
    except TimeoutException:
        print("ERRO: A página demorou demais para carregar.")
        return []

    soup = BeautifulSoup(driver.page_source, 'lxml')
    json_tag = soup.find('code', class_='language-json')
    if not json_tag:
        print("ERRO: Não foi possível encontrar a tag com os dados JSON na página final.")
        return []

    stream_list = []
    order_counter = 0
    base_url = url.split('/api/')[0]
    uk_timezone = pytz.timezone("Europe/London")  # ### ALTERADO ###: Definimos o fuso horário do Reino Unido

    try:
        full_text = json_tag.get_text()
        start_index = full_text.find('{')
        end_index = full_text.rfind('}')
        if start_index == -1 or end_index == -1: raise ValueError("JSON object boundaries not found")

        json_only_text = full_text[start_index: end_index + 1]
        json_cleaned = re.sub(r'^\s*\d+\s*', '', json_only_text, flags=re.MULTILINE)
        data = json.loads(json_cleaned)

        for date_key, categories in data.items():
            event_date = _parse_date_from_key(date_key)
            if not event_date: continue  # ### ALTERADO ###: Pula para o próximo dia se a data for inválida

            for sport_category, events in categories.items():
                translated_sport = config.SPORT_TRANSLATION_MAP.get(sport_category, sport_category)
                if "Tennis" in sport_category: translated_sport = "Tênis"

                for event in events:
                    all_channels = []
                    for channels_data in [event.get('channels'), event.get('channels2')]:
                        if not channels_data: continue
                        if isinstance(channels_data, list):
                            all_channels.extend(channels_data)
                        elif isinstance(channels_data, dict):
                            if 'channel_name' in channels_data:
                                all_channels.append(channels_data)
                            else:
                                all_channels.extend(list(channels_data.values()))

                    for channel in all_channels:
                        try:
                            channel_name = channel['channel_name']
                            channel_id = channel['channel_id']
                            event_time_obj = datetime.strptime(event['time'], '%H:%M').time()

                            # --- ### INÍCIO DA LÓGICA DE FUSO HORÁRIO CORRIGIDA ### ---
                            naive_dt = datetime.combine(event_date, event_time_obj)
                            local_dt = uk_timezone.localize(naive_dt)
                            start_dt_utc = local_dt.astimezone(timezone.utc)
                            # --- ### FIM DA LÓGICA DE FUSO HORÁRIO CORRIGIDA ### ---

                            start_timestamp_ms = int(start_dt_utc.timestamp() * 1000)
                            sport_icon = config.SPORT_ICON_MAP.get(translated_sport, config.DEFAULT_SPORT_ICON)
                            logo_url = find_best_logo_url(channel_name, logo_cache, sport_icon)

                            stream_list.append({
                                'id': channel_id,
                                'stream_url': f"{base_url}/stream/{channel_id}.m3u8",
                                'event_name': _reformat_event_name(event['event']),
                                'sport': translated_sport,
                                'source_name': channel_name,
                                'start_timestamp_ms': str(start_timestamp_ms),
                                'original_order': order_counter,
                                'logo_url': logo_url,
                            })
                            order_counter += 1
                        except (KeyError, ValueError) as e:
                            print(f"AVISO: Pulando canal mal formatado. Detalhes: {e} | Canal: {channel}")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao processar o JSON da página. Detalhes: {e}")

    print(f"Extração com Selenium concluída. {len(stream_list)} streams encontrados.")
    return stream_list