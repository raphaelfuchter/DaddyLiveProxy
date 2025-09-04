# gerador_playlist/utils.py

import os
import json
import re
import unicodedata
import difflib
from urllib.parse import unquote
from datetime import datetime, timedelta
from typing import Union, Dict
import requests
from . import config


def obter_urls_logos_com_cache(github_token: Union[str, None]) -> Dict:
    if os.path.exists(config.LOGO_CACHE_FILE):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(config.LOGO_CACHE_FILE))
        if (datetime.now() - file_mod_time) < timedelta(hours=config.LOGO_CACHE_EXPIRATION_HOURS):
            print("Carregando logos do cache local (válido).")
            with open(config.LOGO_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)

    print("\nBuscando catálogo de logos do GitHub...")
    headers = {}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
        print("Usando token do GitHub para autenticação.")

    logo_cache = {}
    try:
        response = requests.get(config.GITHUB_API_URL, headers=headers)
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

        with open(config.LOGO_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(logo_cache, f, indent=2)
        print(f"Catálogo de {len(logo_cache)} logos carregado e salvo em cache.")

    except requests.exceptions.RequestException as e:
        print(f"AVISO: Falha ao buscar logos do GitHub. Erro: {e}")
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code in [401, 403]:
            print("DICA: O token do GitHub pode ser inválido, expirado ou o limite de requisições foi excedido.")

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

    # Simple caching of normalized keys within the function call
    if not hasattr(find_best_logo_url, "normalized_keys_cache") or find_best_logo_url.normalized_keys_cache.get(
            'keys') != logo_cache.keys():
        normalized_keys = {normalize_text(k): k for k in logo_cache.keys()}
        find_best_logo_url.normalized_keys_cache = {'keys': logo_cache.keys(), 'normalized': normalized_keys}

    normalized_keys_map = find_best_logo_url.normalized_keys_cache['normalized']
    best_match = difflib.get_close_matches(normalized_source, normalized_keys_map.keys(), n=1, cutoff=0.7)

    if best_match:
        original_key = normalized_keys_map[best_match[0]]
        return logo_cache[original_key]

    return sport_icon


def sanitize_id(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9.-]', '', name.replace(' ', ''))

def _parse_date_from_key(date_key: str) -> datetime.date:
    """Extrai e converte a data a partir da chave do JSON (ex: 'Monday 12 Aug 2024')."""
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