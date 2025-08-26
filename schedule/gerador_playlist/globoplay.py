import requests
import json

# --- DADOS DOS CANAIS ---
channels = [
    {
        "name": "Globo NSC",
        "video_id": "6120663",
        "tvg_id": "SÃ£o.Paulo/SP..Globo.br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/globo-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "Sportv 1",
        "video_id": "7339108",
        "tvg_id": "SÃ£o.Paulo/SP..SporTV.br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/sportv-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "Sportv 2",
        "video_id": "7339117",
        "tvg_id": "SÃ£o.Paulo/SP..SporTV.2.br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/sportv2-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "Sportv 3",
        "video_id": "7339123",
        "tvg_id": "SÃ£o.Paulo/SP..SporTV.3..brr",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/sportv3-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "MultiShow",
        "video_id": "7339131",
        "tvg_id": "SÃ£o.Paulo/SP..Multishow.br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/multishow-br.png?raw=true",
        "group_title": "GloboPlay"
    }
]

# --- CONFIGURAÇÃO DA REQUISIÇÃO ---
playback_api_url = "https://playback.video.globo.com/v4/video-session"
playback_api_headers = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.8',
    'authorization': 'Bearer 15299621c38903b7a556b8c286adb7b716d693041304d7830386f546c786e52524b6a36464e49466b525274395a556b597a357778367838534b706875713948524b73395541534a65584c6f4433725658666d5663537a433168694552794362485a385a3134413d3d3a303a7573636c7976766a61776b6e6b63786b7962796f',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://globoplay.globo.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://globoplay.globo.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}
payload_base = {
    "player_type": "desktop",
    "quality": "max",
    "content_protection": "widevine",
    "tz": "-03:00",
    "capabilities": {"low_latency": True, "smart_mosaic": True, "dvr": True},
    "consumption": "streaming",
    "metadata": {"name": "web", "device": {"type": "desktop", "os": {}}},
    "version": 2
}

def gerar_conteudo_globoplay():
    """Busca os links de stream dos canais Globoplay e retorna o conteúdo M3U."""
    m3u_content = ""
    urls_encontradas = 0

    for channel in channels:
        print(f"Buscando stream para: {channel['name']}...")
        current_payload = payload_base.copy()
        current_payload['video_id'] = channel['video_id']

        try:
            response = requests.post(playback_api_url, headers=playback_api_headers, json=current_payload)
            response.raise_for_status()

            playback_data = response.json()
            stream_url = playback_data['sources'][0]['url']

            m3u_content += f'#EXTINF:-1 tvg-id="{channel["tvg_id"]}" tvg-name="{channel["name"]}" tvg-logo="{channel["tvg_logo"]}" group-title="{channel["group_title"]}",{channel["name"]}\n'
            m3u_content += stream_url + "\n\n"

            print(f"✅ Sucesso!")
            urls_encontradas += 1

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição para {channel['name']}: {e}")
        except (KeyError, IndexError):
            print(f"❌ Erro ao processar a resposta da API para {channel['name']}.")

    if urls_encontradas > 0:
        print(f"\n✅ {urls_encontradas} canais Globoplay encontrados.")
    else:
        print("\n❌ Nenhum link de stream do Globoplay foi capturado.")

    return m3u_content
