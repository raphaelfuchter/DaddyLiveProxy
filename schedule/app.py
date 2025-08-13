# --- Bibliotecas ---
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
from typing import Union, List
import http.server
import socketserver
import threading

# --- Configuração do Gerador ---
SCHEDULE_PAGE_URL = "http://192.168.68.19:3000/api/schedule/"
M3U8_OUTPUT_FILENAME = "schedule_playlist.m3u8"
EPG_OUTPUT_FILENAME = "epg.xml"
LOGO_CACHE_FILE = "logo_cache.json"
EPG_EVENT_DURATION_HOURS = 2
GROUP_SORT_ORDER = ["Futebol", "Basquete", "Futebol Americano", "Automobilismo", "Hóquei no Gelo", "Beisebol", "Programas de TV", "Tênis", "Futsal", "MMA"]
EPG_PAST_EVENT_CUTOFF_HOURS = 1
EPG_PAST_EVENT_CUTOFF_HOURS_FUTEBOL = 0.5
EPG_LOCAL_TIMEZONE_OFFSET_HOURS = -3
GITHUB_API_URL = "https://api.github.com/repos/tv-logo/tv-logos/contents/countries"
LOGO_CACHE_EXPIRATION_HOURS = 2
DEFAULT_SPORT_ICON = "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/sports.png"
PLACEHOLDER_TEXT = "Programação Não Disponível"
SERVER_IP = "192.168.68.19"
SERVER_PORT = 8007

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
    "Sinuca": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/snooker.png",
    "Golfe": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/golf.png"
}
SPORT_TRANSLATION_MAP = {
    "Soccer": "Futebol", "Basketball": "Basquete", "Am. Football": "Futebol Americano", "Tennis": "Tênis",
    "Motorsport": "Automobilismo", "Snooker": "Sinuca", "Ice Hockey": "Hóquei no Gelo", "Baseball": "Beisebol",
    "TV Shows": "Programas de TV", "Cricket": "Críquete", "WWE": "Luta Livre", "Badminton": "Badminton",
    "Darts": "Dardos", "Boxing": "Boxe", "Athletics": "Atletismo", "Cycling": "Ciclismo", "Bowling": "Boliche",
    "Horse Racing": "Corrida de Cavalos", "Volleyball": "Volei", "Water polo": "Polo Aquático",
    "Water Sports": "Esportes Aquáticos", "Fencing": "Esgrima", "Field Hockey": "Hóquei na Grama",
    "Handball": "Handebol", "Gymnastics": "Ginástica", "PPV Events": "Eventos PPV",
    "Aussie rules": "Futebol Australiano", "Golf": "Golfe"
}

STATIC_CHANNELS = [
    {
        "id": "cazetv.br", "name": "CazéTV", "platform": "youtube",
        "url": "https://www.youtube.com/@CazeTV/live",
        "logo": "https://yt3.googleusercontent.com/o6S4_2-y_2pA_0_f5q2I_D2aO2eWSUj1SOK2IeI2O5W2w_imACs_yGNQY8Y-r3tO9k4c_d2a=s176-c-k-c0x00ffffff-no-rj",
    },
    {
        "id": "gaules.br", "name": "Gaules", "platform": "kick",
        "url": "https://kick.com/gaules",
        "logo": "https://files.kick.com/images/user/6313/profile_image/conversion/c5109b43-234b-4375-ba19-72f13386663f-full.webp",
    },
    {
        "id": "zigueira.br", "name": "Zigueira", "platform": "kick",
        "url": "https://kick.com/zigueira",
        "logo": "https://files.kick.com/images/user/158654/profile_image/conversion/b7325619-813c-43f1-bd12-70b9ac44a86f-full.webp",
    },
    {
        "id": "thedarkness.br", "name": "Piores Gamers do Mundo", "platform": "youtube",
        "url": "https://www.youtube.com/@pioresgamersdomundo/live",
        "logo": "https://yt3.googleusercontent.com/ytc/AIdro_k62oYF2_5BD29f2pP_LraNqKBCnkb8vLdD8d5s-Q=s176-c-k-c0x00ffffff-no-rj",
    },
    {
        "id": "alanzoka.br", "name": "Alanzoka", "platform": "twitch",
        "url": "https://www.twitch.tv/alanzoka",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/15cec952-c1ba-4ff8-a79c-53c2fa5bd269-profile_image-300x300.png",
    }
]

# --- Funções do Gerador ---

def obter_urls_logos_com_cache(api_url: str, github_token: Union[str, None]) -> dict:
    # ... (código mantido 100% igual ao seu)
    if os.path.exists(LOGO_CACHE_FILE):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(LOGO_CACHE_FILE))
        if (datetime.now() - file_mod_time) < timedelta(hours=LOGO_CACHE_EXPIRATION_HOURS):
            print("Carregando logos do cache local (válido).")
            with open(LOGO_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    print("\nBuscando catálogo de logos do GitHub...")
    headers = {}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
        print("Usando token do GitHub para autenticação.")
    logo_cache = {}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        countries = response.json()
        for country in countries:
            if country['type'] == 'dir':
                country_resp = requests.get(country['url'], headers=headers)
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
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code in [401, 403]:
            print("DICA: O token do GitHub pode ser inválido, expirado ou o limite de requisições foi excedido.")
    return logo_cache

def normalize_text(text: str) -> str:
    # ... (código mantido 100% igual ao seu)
    if not text: return ""
    text = text.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'\b(hd|sd|fhd|uhd|4k|24h|ao vivo|multiaudio)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

def find_best_logo_url(source_name: str, logo_cache: dict, sport_icon: str) -> str:
    # ... (código mantido 100% igual ao seu)
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
    # ... (código mantido 100% igual ao seu)
    return re.sub(r'[^a-zA-Z0-9.-]', '', name.replace(' ', ''))

def parse_date_from_key(date_key: str) -> datetime.date:
    # ... (código mantido 100% igual ao seu)
    date_str_part = date_key.split(' - ')[0]
    date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_part)
    possible_formats = ['%A %d %b %Y', '%A %d %B %Y']
    for date_format in possible_formats:
        try:
            return datetime.strptime(date_str_cleaned, date_format).date()
        except ValueError:
            continue
    print(f"AVISO: Não foi possível parsear a data '{date_key}'. Usando data de hoje.")
    return datetime.now().date()

def reformat_event_name(original_name: str) -> str:
    # ... (código mantido 100% igual ao seu)
    try:
        league_part, match_part_full = original_name.split(':', 1)
        match_part = match_part_full.split('(', 1)[0] if '(' in match_part_full else match_part_full
        return f"{match_part.strip()} : {league_part.strip()}"
    except (ValueError, IndexError):
        return original_name

def extract_streams_with_selenium(driver: webdriver.Chrome, url: str, logo_cache: dict) -> list:
    # ... (código mantido 100% igual ao seu)
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
                            start_dt_utc = datetime.combine(event_date, event_time_obj).replace(tzinfo=timezone.utc)
                            start_timestamp_ms = int(start_dt_utc.timestamp() * 1000)
                            sport_icon = SPORT_ICON_MAP.get(translated_sport, DEFAULT_SPORT_ICON)
                            logo_url = find_best_logo_url(channel_name, logo_cache, sport_icon)
                            stream_list.append({
                                'id': channel_id, 'stream_url': f"{base_url}/stream/{channel_id}.m3u8",
                                'event_name': reformat_event_name(event['event']), 'sport': translated_sport,
                                'source_name': channel_name, 'start_timestamp_ms': str(start_timestamp_ms),
                                'original_order': order_counter, 'logo_url': logo_url,
                            })
                            order_counter += 1
                        except (KeyError, ValueError) as e:
                            print(f"AVISO: Pulando canal mal formatado. Detalhes: {e} | Canal: {channel}")
    except Exception as e:
        print(f"ERRO CRÍTICO: Falha ao processar o JSON da página. Detalhes: {e}")
    print(f"Extração com Selenium concluída. {len(stream_list)} streams encontrados.")
    return stream_list

def generate_m3u8_content(stream_list: list) -> str:
    # ... (código mantido 100% igual ao seu)
    m3u8_lines = ["#EXTM3U"]
    if not stream_list: 
        print("\nNenhum stream dinâmico encontrado para o M3U8.")
        return "\n".join(m3u8_lines)
    
    print("\nOrdenando streams dinâmicos e gerando M3U8...")
    sort_map = {group.lower(): i for i, group in enumerate(GROUP_SORT_ORDER)}
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

# --- Funções Verificadoras de Plataforma ---

def format_youtube_title(title: str) -> str:
    # ... (código mantido 100% igual ao seu)
    if not title: return "Evento Ao Vivo"
    cleaned_title = re.sub(r'ao vivo:?\s*\|?\s*', '', title, flags=re.IGNORECASE).strip()
    return cleaned_title.title()

def get_youtube_live_title(channel_url: str) -> Union[str, None]:
    # ... (código mantido 100% igual ao seu)
    try:
        headers = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.5"}
        response = requests.get(channel_url, headers=headers, timeout=10)
        response.raise_for_status()
        if '"isLive":true' in response.text:
            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.find('meta', property='og:title')
            if title_tag and title_tag.get('content'):
                return format_youtube_title(title_tag.get('content'))
            return "Evento Ao Vivo"
    except requests.exceptions.RequestException as e:
        print(f"  - AVISO: Falha ao verificar YouTube ({channel_url}). Erro: {e}")
    return None

def get_kick_live_title(channel_url: str) -> Union[str, None]:
    """Verifica um canal do Kick via API e retorna o título da live."""
    try:
        slug = channel_url.split('/')[-1]
        api_url = f"https://kick.com/api/v2/channels/{slug}"
        
        # --- LINHA ADICIONADA ---
        # Adiciona o cabeçalho para simular um navegador
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        # Passa os headers na requisição
        response = requests.get(api_url, headers=headers, timeout=10)
        
        response.raise_for_status()
        data = response.json()
        if data.get('livestream'):
            return data['livestream'].get('session_title', 'Evento Ao Vivo')
    except requests.exceptions.RequestException as e:
        print(f"  - AVISO: Falha ao verificar Kick ({channel_url}). Erro: {e}")
    return None

def get_twitch_live_title(channel_url: str) -> Union[str, None]:
    # ... (código mantido 100% igual ao seu)
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(channel_url, headers=headers, timeout=10)
        response.raise_for_status()
        if 'isLiveBroadcast' in response.text:
            soup = BeautifulSoup(response.text, 'lxml')
            title_tag = soup.select_one('h1[data-a-target="stream-title"], h2[data-a-target="stream-title"]')
            if title_tag:
                return title_tag.text
            return "Evento Ao Vivo"
    except requests.exceptions.RequestException as e:
        print(f"  - AVISO: Falha ao verificar Twitch ({channel_url}). Erro: {e}")
    return None

# --- FUNÇÕES DE GERAÇÃO DE EPG (REFATORADAS) ---

# --- 1. FUNÇÃO PARA CANAIS ESTÁTICOS ---
def generate_static_channels_epg(xml_lines: List[str]):
    """Gera o EPG para a lista de canais estáticos (YouTube, Kick, Twitch, etc.)."""
    print("\nVerificando status dos canais estáticos para o EPG...")
    local_tz = timezone(timedelta(hours=EPG_LOCAL_TIMEZONE_OFFSET_HOURS))
    
    platform_checkers = {
        'youtube': get_youtube_live_title,
        'kick': get_kick_live_title,
        'twitch': get_twitch_live_title,
    }

    for channel in STATIC_CHANNELS:
        print(f"- Verificando {channel['name']} ({channel['platform']})...")
        checker_func = platform_checkers.get(channel['platform'])
        live_title = None
        if checker_func:
            live_title = checker_func(channel['url'])
        
        xml_lines.append(f'  <channel id="{channel["id"]}">')
        xml_lines.append(f'    <display-name>{html.escape(channel["name"])}</display-name>')
        xml_lines.append(f'    <icon src="{html.escape(channel["logo"])}" />')
        xml_lines.append('  </channel>')

        now_utc = datetime.now(timezone.utc)
        if live_title:
            print(f"  -> {channel['name']} está AO VIVO: {live_title}")
            event_start_utc = now_utc
            event_end_utc = event_start_utc + timedelta(hours=EPG_EVENT_DURATION_HOURS)
            now_local = now_utc.astimezone(local_tz)
            local_day_start = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
            local_day_end = local_day_start + timedelta(days=1)
            day_start_utc = local_day_start.astimezone(timezone.utc)
            day_end_utc = local_day_end.astimezone(timezone.utc)

            if event_start_utc > day_start_utc:
                day_start_utc = day_start_utc - timedelta(days=1)
                start_str = day_start_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = event_start_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
                xml_lines.append(f'    <title lang="pt">{PLACEHOLDER_TEXT}</title>')
                xml_lines.append('  </programme>')

            start_str = event_start_utc.strftime('%Y%m%d%H%M%S %z')
            stop_str = event_end_utc.strftime('%Y%m%d%H%M%S %z')
            safe_prog_title = html.escape(live_title)
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
            xml_lines.append(f'    <title lang="pt">{safe_prog_title}</title>')
            xml_lines.append(f'    <desc lang="pt">{safe_prog_title}</desc>')
            xml_lines.append('  </programme>')

            if event_end_utc < day_end_utc:
                start_str = event_end_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = day_end_utc.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
                xml_lines.append(f'    <title lang="pt">{PLACEHOLDER_TEXT}</title>')
                xml_lines.append('  </programme>')
        else:
            print(f"  -> {channel['name']} está offline.")
            start_str = now_utc.strftime('%Y%m%d%H%M%S %z')
            now_local = now_utc.astimezone(local_tz)
            local_day_end = now_local.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            day_end_utc = local_day_end.astimezone(timezone.utc)
            stop_str = day_end_utc.strftime('%Y%m%d%H%M%S %z')
            xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{channel["id"]}">')
            xml_lines.append(f'    <title lang="pt">{PLACEHOLDER_TEXT}</title>')
            xml_lines.append('  </programme>')

# --- 2. FUNÇÃO PARA STREAMS DINÂMICOS ---
def generate_dynamic_streams_epg(xml_lines: List[str], stream_list: List[dict]):
    """Gera o EPG para a lista de streams dinâmicos (vindos do Selenium)."""
    if not stream_list:
        print("\nNenhum stream dinâmico para adicionar ao EPG.")
        return

    print("\nAdicionando canais dinâmicos ao EPG...")
    generated_channel_ids = set()
    local_tz = timezone(timedelta(hours=EPG_LOCAL_TIMEZONE_OFFSET_HOURS))

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
            end_dt_utc = start_dt_utc + timedelta(hours=EPG_EVENT_DURATION_HOURS)
            
            start_dt_local = start_dt_utc.astimezone(local_tz)
            local_day_start = start_dt_local.replace(hour=0, minute=0, second=0, microsecond=0)
            day_start_utc = local_day_start.astimezone(timezone.utc)
            local_day_end = local_day_start + timedelta(days=1)
            day_end_utc = local_day_end.astimezone(timezone.utc)

            safe_event_name = html.escape(stream['event_name'])
            safe_channel_name = html.escape(stream['source_name'])

            if start_dt_utc > day_start_utc:
                # Sua lógica original para placeholders de canais dinâmicos
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
                 # Sua lógica original para placeholders de canais dinâmicos
                day_end_utc_mod = day_end_utc + timedelta(days=1)
                start_str = end_dt_utc.strftime('%Y%m%d%H%M%S %z')
                stop_str = day_end_utc_mod.strftime('%Y%m%d%H%M%S %z')
                xml_lines.append(f'  <programme start="{start_str}" stop="{stop_str}" channel="{unique_event_id}">')
                xml_lines.append('    <title lang="pt">Finalizado</title>')
                xml_lines.append('  </programme>')
        except (ValueError, TypeError) as e:
            print(f"AVISO: Pulando evento dinâmico no EPG devido a erro de dados: {e}")
            continue

# --- 3. FUNÇÃO PRINCIPAL "ORQUESTRADORA" ---
def generate_xmltv_epg(stream_list: List[dict]) -> str:
    """Orquestra a geração do arquivo EPG chamando as funções especializadas."""
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv>']
    
    generate_static_channels_epg(xml_lines)
    generate_dynamic_streams_epg(xml_lines, stream_list)
    
    xml_lines.append('</tv>')
    return "\n".join(xml_lines)

# --- Função Principal de Execução ---
def gerador_main():
    # ... (código mantido 100% igual ao seu)
    print("--- Gerador de Playlist e EPG ---")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        print("\nAVISO: GITHUB_TOKEN não definida.")
    logo_cache = obter_urls_logos_com_cache(GITHUB_API_URL, GITHUB_TOKEN)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    stream_data = []
    driver = None
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        stream_data = extract_streams_with_selenium(driver, SCHEDULE_PAGE_URL, logo_cache)
    finally:
        if driver:
            print("\nProcesso de extração finalizado. Fechando o navegador.")
            driver.quit()

    now_utc = datetime.now(timezone.utc)
    filtered_streams = []
    if stream_data:
        filtered_streams = [
            s for s in stream_data
            if (datetime.fromtimestamp(int(s['start_timestamp_ms']) / 1000, tz=timezone.utc) + timedelta(hours=EPG_EVENT_DURATION_HOURS)) >=
               (now_utc - timedelta(hours=(EPG_PAST_EVENT_CUTOFF_HOURS_FUTEBOL if s['sport'] == 'Futebol' else EPG_PAST_EVENT_CUTOFF_HOURS)))
        ]
        print(f"\nStreams extraídos: {len(stream_data)}. Válidos após filtro de tempo: {len(filtered_streams)}.")
        if not filtered_streams and stream_data:
             print("Nenhum evento futuro ou em andamento encontrado nos streams dinâmicos.")
    else:
        print("\nNenhum stream dinâmico foi extraído.")
    
    m3u8_content = generate_m3u8_content(filtered_streams)
    # A geração do EPG agora acontece independentemente de haver streams dinâmicos
    epg_content = generate_xmltv_epg(filtered_streams)
    
    if m3u8_content and len(m3u8_content.splitlines()) > 1:
        try:
            with open(M3U8_OUTPUT_FILENAME, "w", encoding="utf-8") as f: f.write(m3u8_content)
            print(f"✅ Sucesso! Arquivo '{M3U8_OUTPUT_FILENAME}' gerado.")
        except IOError as e:
            print(f"❌ ERRO ao salvar M3U8: {e}")
    else:
        print(f"✅ Arquivo '{M3U8_OUTPUT_FILENAME}' gerado vazio (sem streams dinâmicos).")

    try:
        with open(EPG_OUTPUT_FILENAME, "w", encoding="utf-8") as f: f.write(epg_content)
        print(f"✅ Sucesso! Arquivo '{EPG_OUTPUT_FILENAME}' gerado.")
    except IOError as e:
        print(f"❌ ERRO ao salvar EPG: {e}")

# --- Funções para Servidor e Agendamento ---
def loop_de_atualizacao_sincronizada():
    # ... (código mantido 100% igual ao seu)
    while True:
        agora = datetime.now()
        minuto_atual = agora.minute
        if minuto_atual < 30:
            proxima_execucao = agora.replace(minute=30, second=0, microsecond=0)
        else:
            proxima_execucao = (agora + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        
        espera_em_segundos = (proxima_execucao - agora).total_seconds()
        print("\n" + "="*50)
        print(f"Ciclo finalizado. Próxima atualização: {proxima_execucao.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50 + "\n")
        
        if espera_em_segundos > 0:
            time.sleep(espera_em_segundos)
        
        print("\n" + "="*50)
        print(f"HORA DA ATUALIZAÇÃO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        try:
            gerador_main()
        except Exception as e:
            print(f"❌ ERRO INESPERADO DURANTE A EXECUÇÃO DO GERADOR: {e}")

def iniciar_servidor():
    # ... (código mantido 100% igual ao seu)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", SERVER_PORT), handler) as httpd:
        print("\n\n--- Servidor HTTP iniciado ---")
        print(f"Servindo na porta {SERVER_PORT}.")
        print(f"\nLinks para uso na sua rede local:")
        print(f"  Playlist M3U8: http://{SERVER_IP}:{SERVER_PORT}/{M3U8_OUTPUT_FILENAME}")
        print(f"  Guia EPG XML:  http://{SERVER_IP}:{SERVER_PORT}/{EPG_OUTPUT_FILENAME}")
        print("\nAtualizações automáticas a cada :00 e :30 de cada hora.")      
        httpd.serve_forever()

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    # ... (código mantido 100% igual ao seu)
    print("Executando o gerador pela primeira vez...")
    try:
        gerador_main()
    except Exception as e:
        print(f"❌ ERRO NA EXECUÇÃO INICIAL DO GERADOR: {e}")
    
    print("\nIniciando a thread de atualizações futuras...")
    gerador_thread = threading.Thread(target=loop_de_atualizacao_sincronizada, daemon=True)
    gerador_thread.start()
    
    iniciar_servidor()