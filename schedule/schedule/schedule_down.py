import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import html
import re
import requests
import difflib
from urllib.parse import unquote
import unicodedata
import collections

# --- Configuração ---
SCHEDULE_PAGE_URL = "http://192.168.68.19:3000/api/schedule/"
# Saída em pastas dedicadas para facilitar o mapeamento com Docker
M3U8_OUTPUT_FILENAME = "output/schedule_playlist.m3u8"
EPG_OUTPUT_FILENAME = "output/epg.xml"
EPG_EVENT_DURATION_HOURS = 2
GROUP_SORT_ORDER = ["Futebol", "Basquete", "Futebol Americano", "Automobilismo", "Hóquei no Gelo", "Beisebol", "Programas de TV", "Tênis", "Futsal", "MMA"]
EPG_PAST_EVENT_CUTOFF_HOURS = 1

# Fuso horário para a lógica de "dia inteiro" do EPG (UTC-3 para Horário de Brasília)
EPG_LOCAL_TIMEZONE_OFFSET_HOURS = -3

# Repositório de logos e cache local
GITHUB_API_URL = "https://api.github.com/repos/tv-logo/tv-logos/contents/countries"
LOGO_CACHE_FILE = "cache/logo_cache.json"
LOGO_CACHE_EXPIRATION_HOURS = 48

# --- URLs dos Ícones - VERSÃO FINAL COM NOMES DE ARQUIVO CORRETOS ---
DEFAULT_SPORT_ICON = "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/sports.png"

SPORT_ICON_MAP = {
    "Futebol": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/soccer.png",
    "Basquete": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/basketball.png",
    "Futebol Americano": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/americanfootball.png",
    "Automobilismo": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/motorsport.png",
    "Programas de TV": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/tv.png",
    "Beisebol": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/baseball.png",
    "Hóquei no Gelo": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/hockey.png",
    "Tênis": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/tennis.png",
    "Atletismo": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/Athletics.png",
    "Corrida de Cavalos": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/horse.png",
    "Críquete": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/cricket.png",
    "Ciclismo": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/bike.png",
    "Sinuca": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/snooker.png"
}

SPORT_TRANSLATION_MAP = {
    "Soccer": "Futebol",
    "Basketball": "Basquete",
    "Am. Football": "Futebol Americano",
    "Tennis": "Tênis",
    "Motorsport": "Automobilismo",
    "Snooker": "Sinuca",
    "Ice Hockey": "Hóquei no Gelo",
    "Baseball": "Beisebol",
    "TV Shows": "Programas de TV",
    "Cricket": "Críquete",
    "WWE": "Luta Livre",
    "Badminton": "Badminton",
    "Darts": "Dardos",
    "Boxing": "Boxe",
    "Athletics": "Atletismo",
    "Cycling": "Ciclismo",
    "Bowling": "Boliche"  ,
    "Horse Racing": "Corrida de Cavalos",
    "Volleyball": "Volei",
    "Water polo": "Polo Aquático",
    "Water Sports": "Esportes Aquáticos",
    "Fencing": "Esgrima",
    "Field Hockey": "Hóquei na Grama",
    "Handball": "Handebol",
    "Gymnastics": "Ginástica",
    "PPV Events": "Eventos PPV"
}
# --- Fim da Configuração ---

def obter_urls_logos_com_cache(api_url: str) -> dict:
    if os.path.exists(LOGO_CACHE_FILE):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(LOGO_CACHE_FILE))
        if (datetime.now() - file_mod_time) < timedelta(hours=LOGO_CACHE_EXPIRATION_HOURS):
            print("Carregando logos do cache local (válido).")
            with open(LOGO_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    print("\nBuscando catálogo de logos do GitHub...")
    logo_cache = {}
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        countries = response.json()
        for country in countries:
            if country['type'] == 'dir':
                country_resp = requests.get(country['url'])
                country_resp.raise_for_status()
                logos = country_resp.json()
                for logo in logos:
                    if logo['type'] == 'file' and any(logo['name'].endswith(ext) for ext in ['.png', '.jpg', '.svg']):
                        file_name_without_ext = os.path.splitext(unquote(logo['name']))[0]
                        logo_cache[file_name_without_ext] = logo['download_url']
        with open(LOGO_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(logo_cache, f, indent=2)
        print(f"Catálogo de {len(logo_cache)} logos carregado e salvo em cache.")
    except requests.exceptions.RequestException as e:
        print(f"AVISO: Falha ao buscar logos do GitHub. Erro: {e}")
    return logo_cache

def normalize_text(text: str) -> str:
    if not text: return ""
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'\b(hd|sd|fhd|uhd|4k|24h|ao vivo|multiaudio)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

def find_best_logo_url(source_name: str, logo_cache: dict, sport_icon: str) -> str:
    if not logo_cache or not source_name: return sport_icon
    normalized_source = normalize_text(source_name)
    if not hasattr(find_best_logo_url, "normalized_keys"):
       find_best_logo_url.normalized_keys = {normalize_text(k): k for k in logo_cache.keys()}
    normalized_keys = find_best_logo_url.normalized_keys
    best_match = difflib.get_close_matches(normalized_source, normalized_keys.keys(), n=1, cutoff=0.7)
    if best_match:
        original_key = normalized_keys[best_match[0]]
        return logo_cache[original_key]
    return sport_icon

def sanitize_id(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9.-]', '', name.replace(' ', ''))

def parse_date_from_key(date_key: str) -> datetime.date:
    date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_key.split(' - ')[0])
    try:
        return datetime.strptime(date_str_cleaned, '%A %d %B %Y').date()
    except ValueError:
        print(f"AVISO: Não foi possível parsear a data '{date_key}'. Usando data de hoje como fallback.")
        return datetime.now().date()

def reformat_event_name(original_name: str) -> str:
    """
    Reformata o nome do evento de 'Liga : Jogo (Canal)' para 'Jogo : Liga'.
    """
    try:
        # Divide a string no primeiro ':' para separar a liga do resto
        league_part, match_part_full = original_name.split(':', 1)
        
        # Remove a informação do canal, que geralmente está entre parênteses
        if '(' in match_part_full:
            match_part = match_part_full.split('(', 1)[0]
        else:
            match_part = match_part_full

        # Remove espaços em branco extras das partes
        league_part = league_part.strip()
        match_part = match_part.strip()
        
        # Retorna a string no novo formato
        return f"{match_part} : {league_part}"
    except (ValueError, IndexError):
        # Se a string não tiver o formato esperado (ex: sem ':'), retorna o nome original
        return original_name

def extract_streams_with_selenium(driver: webdriver.Chrome, url: str, logo_cache: dict) -> list:
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
    
    try:
        full_text = json_tag.get_text()
        start_index = full_text.find('{')
        end_index = full_text.rfind('}')
        if start_index == -1 or end_index == -1: raise ValueError("JSON object boundaries not found")
        json_only_text = full_text[start_index : end_index + 1]
        json_cleaned = re.sub(r'^\s*\d+\s*', '', json_only_text, flags=re.MULTILINE)
        data = json.loads(json_cleaned)
        
        for date_key, categories in data.items():
            event_date = parse_date_from_key(date_key)
            if not event_date: continue
            
            for sport_category, events in categories.items():
                translated_sport = SPORT_TRANSLATION_MAP.get(sport_category, sport_category)
                if "Tennis" in sport_category: translated_sport = "Tênis"

                for event in events:
                    channels1_data = event.get('channels', [])
                    channels2_data = event.get('channels2', [])
                    list1 = [channels1_data] if isinstance(channels1_data, dict) else (channels1_data or [])
                    list2 = [channels2_data] if isinstance(channels2_data, dict) else (channels2_data or [])
                    all_channels = list1 + list2
                    
                    for channel in all_channels:
                        try:
                            channel_name = channel['channel_name']
                            channel_id = channel['channel_id']
                            event_time_obj = datetime.strptime(event['time'], '%H:%M').time()
                            start_dt_utc = datetime.combine(event_date, event_time_obj).replace(tzinfo=timezone.utc)
                            start_timestamp_ms = int(start_dt_utc.timestamp() * 1000)

                            sport_icon = SPORT_ICON_MAP.get(translated_sport, DEFAULT_SPORT_ICON)
                            logo_url = find_best_logo_url(channel_name, logo_cache, sport_icon)

                            stream_list.append({
                                'id': channel_id,
                                'stream_url': f"{base_url}/stream/{channel_id}.m3u8",
                                'event_name': reformat_event_name(event['event']),
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

def generate_m3u8_content(stream_list: list) -> str:
    """Gera o M3U8 com um ID de evento único para cada entrada, garantindo o mapeamento 1-para-1 com o EPG."""
    m3u8_lines = ["#EXTM3U"]
    if not stream_list: return "\n".join(m3u8_lines)
    
    print("\nOrdenando streams e gerando M3U8 com IDs de evento únicos...")
    sort_map = {group.lower(): i for i, group in enumerate(GROUP_SORT_ORDER)}
    stream_list.sort(key=lambda s: (sort_map.get(s['sport'].lower(), len(sort_map)), int(s['start_timestamp_ms'])))

    for stream in stream_list:
        # --- ALTERAÇÃO PRINCIPAL ---
        # ID agora é único POR EVENTO, combinando canal e horário.
        # Isso garante que cada linha do M3U tenha seu próprio EPG isolado.
        unique_event_id = sanitize_id(f"evt.{stream['source_name']}.{stream['start_timestamp_ms']}")
        
        # O nome que aparece na lista é o nome do evento.
        display_title = f"{stream['event_name']}"
        
        extinf = (f'#EXTINF:-1 tvg-id="{unique_event_id}" '
                  f'tvg-logo="{stream["logo_url"]}" '
                  f'group-title="{stream["sport"]}",'
                  f'{display_title}')
        m3u8_lines.extend([extinf, stream['stream_url']])
    return "\n".join(m3u8_lines)

def generate_xmltv_epg(stream_list: list) -> str:
    """Gera EPG onde cada evento é um canal virtual isolado, preenchendo o dia inteiro com status."""
    if not stream_list: return ""
    print("Gerando EPG com canais virtuais (dia inteiro) por evento...")

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']
    local_tz = timezone(timedelta(hours=EPG_LOCAL_TIMEZONE_OFFSET_HOURS))
    generated_channel_ids = set()

    # Itera em cada stream para criar um canal e uma grade de dia inteiro para cada um
    for stream in stream_list:
        try:
            # ID único do evento, deve ser IDÊNTICO ao usado no M3U8
            unique_event_id = sanitize_id(f"evt.{stream['source_name']}.{stream['start_timestamp_ms']}")

            # Adiciona a tag <channel> para nosso canal virtual (apenas uma vez)
            if unique_event_id not in generated_channel_ids:
                xml_lines.append(f'  <channel id="{unique_event_id}">')
                xml_lines.append(f'    <display-name>{html.escape(stream["source_name"])}</display-name>')
                xml_lines.append(f'    <icon src="{html.escape(stream["logo_url"])}" />')
                xml_lines.append('  </channel>')
                generated_channel_ids.add(unique_event_id)

            # --- Lógica para preencher o dia ---
            timestamp_ms = int(stream['start_timestamp_ms'])
            start_dt_utc = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            end_dt_utc = start_dt_utc + timedelta(hours=EPG_EVENT_DURATION_HOURS)

            # Calcula os limites do dia no fuso horário local para o evento
            start_dt_local = start_dt_utc.astimezone(local_tz)
            local_day_start = start_dt_local.replace(hour=0, minute=0, second=0, microsecond=0)
            local_day_end = local_day_start + timedelta(days=1)
            
            # Converte os limites do dia para UTC para usar no XML
            day_start_utc = local_day_start.astimezone(timezone.utc)
            day_end_utc = local_day_end.astimezone(timezone.utc)

            safe_event_name = html.escape(stream['event_name'])
            safe_channel_name = html.escape(stream['source_name'])

            # Bloco 1: "Evento não iniciado" (do início do dia até o começo do evento)
            if start_dt_utc > day_start_utc:
                
                day_start_utc = day_start_utc - timedelta(days=1)
                
                start_str = day_start_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = start_dt_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
                xml_lines.append('    <title lang="pt">Não iniciado</title>')
                xml_lines.append('  </programme>')

            # Bloco 2: O evento real
            start_str = start_dt_utc.strftime('%Y%m%d%H%M%S %z')
            stop_str = end_dt_utc.strftime('%Y%m%d%H%M%S %z')
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
            xml_lines.append(f'    <title lang="pt">{safe_channel_name}</title>')
            xml_lines.append(f'    <desc lang="pt">{safe_event_name}</desc>')
            xml_lines.append('  </programme>')

            # Bloco 3: "Evento finalizado" (do fim do evento até o fim do dia)
            if end_dt_utc < day_end_utc:
                
                day_end_utc = day_end_utc + timedelta(days=1)
                
                start_str = end_dt_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = day_end_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
                xml_lines.append('    <title lang="pt">Finalizado</title>')
                xml_lines.append('  </programme>')
            
        except (ValueError, TypeError) as e:
            print(f"AVISO: Pulando evento no EPG devido a erro de dados: {e}")
            continue
            
    xml_lines.append('</tv>')
    return "\n".join(xml_lines)

def main():
    print("--- Gerador de Playlist e EPG ---")
    logo_cache = obter_urls_logos_com_cache(GITHUB_API_URL)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    stream_data = []
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        stream_data = extract_streams_with_selenium(driver, SCHEDULE_PAGE_URL, logo_cache)
    finally:
        if 'driver' in locals() and driver:
            print("\nProcesso de extração finalizado. Fechando o navegador.")
            driver.quit()

    if not stream_data:
        print("\nNenhum stream foi extraído. Nenhum arquivo será gerado.")
        return

    now_utc = datetime.now(timezone.utc)
    cutoff_time = now_utc - timedelta(hours=EPG_PAST_EVENT_CUTOFF_HOURS)
    
    filtered_streams = [
        s for s in stream_data
        if (datetime.fromtimestamp(int(s['start_timestamp_ms']) / 1000, tz=timezone.utc) + timedelta(hours=EPG_EVENT_DURATION_HOURS)) >= cutoff_time
    ]
    print(f"\nTotal de streams extraídos: {len(stream_data)}. Válidos após filtro de tempo: {len(filtered_streams)}.")

    if not filtered_streams:
        print("Nenhum evento futuro ou em andamento encontrado.")
        return

    m3u8_content = generate_m3u8_content(filtered_streams)
    epg_content = generate_xmltv_epg(filtered_streams)

    try:
        os.makedirs(os.path.dirname(M3U8_OUTPUT_FILENAME), exist_ok=True)
        with open(M3U8_OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            f.write(m3u8_content)
        print(f"✅ Sucesso! Arquivo '{M3U8_OUTPUT_FILENAME}' gerado.")
    except IOError as e:
        print(f"❌ ERRO ao salvar M3U8: {e}")
    try:
        os.makedirs(os.path.dirname(EPG_OUTPUT_FILENAME), exist_ok=True)
        with open(EPG_OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            f.write(epg_content)
        print(f"✅ Sucesso! Arquivo '{EPG_OUTPUT_FILENAME}' gerado.")
    except IOError as e:
        print(f"❌ ERRO ao salvar EPG: {e}")

if __name__ == "__main__":
    main()