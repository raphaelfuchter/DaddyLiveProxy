# gerador_playlist/config.py

from datetime import timedelta, timezone

# --- Configuração do Gerador ---
SCHEDULE_PAGE_URL = "http://192.168.68.19:3000/api/schedule/"
M3U8_OUTPUT_FILENAME = "schedule_playlist.m3u8"
EPG_OUTPUT_FILENAME = "epg.xml"
LOGO_CACHE_FILE = "logo_cache.json"
EPG_EVENT_DURATION_HOURS = 2
EPG_EVENT_DURATION_HOURS_FUTEBOL_AMERICANO = 3
GROUP_SORT_ORDER = ["Futebol", "Basquete", "Futebol Americano", "Hóquei"]
EPG_PAST_EVENT_CUTOFF_HOURS = 0.5
EPG_PAST_EVENT_CUTOFF_HOURS_FUTEBOL = 0.5
EPG_LOCAL_TIMEZONE_OFFSET_HOURS = -3
GITHUB_API_URL = "https://api.github.com/repos/tv-logo/tv-logos/contents/countries"
LOGO_CACHE_EXPIRATION_HOURS = 2
DEFAULT_SPORT_ICON = "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/sports.png"
PLACEHOLDER_TEXT = "Offline"
SERVER_IP = "192.168.68.19"
SERVER_PORT = 8007
LOCAL_TZ = timezone(timedelta(hours=EPG_LOCAL_TIMEZONE_OFFSET_HOURS))

# --- Mapeamentos ---
SPORT_ICON_MAP = {
    "Futebol": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/soccer.png",
    "Basquete": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/basketball.png",
    "Futebol Americano": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/americanfootball.png",
    "Automobilismo": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/motorsport.png",
    "Programas de TV": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/tv.png",
    "Beisebol": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/baseball.png",
    "Hóquei": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/hockey.png",
    "Tênis": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/tennis.png",
    "Atletismo": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/Athletics.png",
    "Corrida de Cavalos": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/horse.png",
    "Equestres": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/horse.png",
    "Críquete": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/cricket.png",
    "Sinuca": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/snooker.png",
    "Golfe": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/golf.png",
    "Polo Aquático": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/golf.png",
    "Esportes Aquáticos": "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/gerador_playlist/logos/water.png"
}
SPORT_TRANSLATION_MAP = {
    "Soccer": "Futebol",
    "Basketball": "Basquete",
    "Am. Football": "Futebol Americano",
    "Motorsport": "Automobilismo",
    "TV Shows": "Programas de TV",
    "TV Show": "Programas de TV",
    "Baseball": "Beisebol",
    "Ice Hockey": "Hóquei",
    "Tennis": "Tênis",
    "Athletics": "Atletismo",
    "Horse Racing": "Corrida de Cavalos",
    "Cricket": "Críquete",
    "Snooker": "Sinuca",
    "Golf": "Golfe",
    "Water polo": "Polo Aquático",
    "Water Sports": "Esportes Aquáticos",
    "Equestrian": "Equestres",

    "WWE": "Luta Livre",
    "Badminton": "Badminton",
    "Darts": "Dardos",
    "Boxing": "Boxe",
    "Cycling": "Ciclismo",
    "Bowling": "Boliche",
    "Volleyball": "Voleibol",
    "Fencing": "Esgrima",
    "Field Hockey": "Hóquei na Grama",
    "Handball": "Handebol",
    "Gymnastics": "Ginástica",
    "PPV Events": "Eventos PPV",
    "Aussie rules": "Futebol Australiano"
}

STATIC_CHANNELS = [
    {
        "id": "cazetv.br", "name": "CazéTV", "platform": "youtube",
        "url": "https://www.youtube.com/@CazeTV/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/2/22/Logotipo_da_Caz%C3%A9TV.png",
    },
    {
        "id": "canalgoat.br", "name": "Canal Goat", "platform": "youtube",
        "url": "https://www.youtube.com/@canalgoatbr/streams",
        "logo": "https://canalgoat.com.br/wp-content/uploads/2024/10/Canal-Goat-Escudo-Color.png",
    },
    {
        "id": "desimpedidos.br", "name": "Desimpedidos", "platform": "youtube",
        "url": "https://www.youtube.com/desimpedidos/streams",
        "logo": "https://imagensempng.com.br/wp-content/uploads/2023/08/277-1.png",
    },
    {
        "id": "sportynetbrasil.br", "name": "SportyNet", "platform": "youtube",
        "url": "https://www.youtube.com/@SportyNetBrasil/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/SportyNet.png/500px-SportyNet.png",
    },
    {
        "id": "getv.br", "name": "geTV", "platform": "youtube",
        "url": "https://www.youtube.com/@getv/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/d/d7/Logotipo_da_GE_TV.png",
    },
    {
        "id": "gaules.br", "name": "Gaules", "platform": "youtube",
        "url": "https://www.youtube.com/gaules/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Gaules_logo_blue.svg/2560px-Gaules_logo_blue.svg.png",
    },
    {
        "id": "zigueira.br", "name": "Zigueira", "platform": "kick",
        "url": "https://kick.com/zigueira",
        "logo": "https://files.kick.com/images/user/55276375/profile_image/bc9947ee-9f86-4036-8236-82252e8c4d9c",
    },
    {
        "id": "thedarkness.br", "name": "TheDarkness", "platform": "youtube",
        "url": "https://www.youtube.com/@pioresgamersdomundo/streams",
        "logo": "https://yt3.googleusercontent.com/GV7bRHNG0juAAZ-twtvfJ31CdIa5v1jEtQZFL2bhRKHIe2pMPrs3nnBcOaNnNmi7ffLFJ2Ud=s900-c-k-c0x00ffffff-no-rj",
    },
    {
        "id": "alanzoka.br", "name": "Alanzoka", "platform": "twitch",
        "url": "https://www.twitch.tv/alanzoka",
        "logo": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgS_r8bzfeP-s6NqswOn5rtypcmAy5gjJk4xNr9JI5mJDSdTB0sP_Ds-O4aeAjOEGKDWnCggyVPKjCzBXBb-5FOzTeu8O6ATeVo1hFooEb1CMk6Dlyta_l4ZIPjNdLwJzYRqsNySmdK1-pi/s1600/c46b05a0-db41-4c66-b736-3ff018df99ec-profile_ima",
    },
    {
        "id": "funky.br", "name": "FunkyBlackCat", "platform": "youtube",
        "url": "https://www.youtube.com/@funkyblackcat/streams",
        "logo": "https://mir-s3-cdn-cf.behance.net/project_modules/max_632_webp/74034541867565.56070a2d84cd4.png",
    },
    {
        "id": "flowgames.br", "name": "Flow Games", "platform": "youtube",
        "url": "https://www.youtube.com/@FlowGamesPodcast/streams",
        "logo": "https://flowgames.gg/wp-content/uploads/2022/10/logo.png",
    },
    {
        "id": "toptvsports.br", "name": "TopTV Sports", "platform": "youtube",
        "url": "https://www.youtube.com/@TopTVSports/streams",
        "logo": "https://play-lh.googleusercontent.com/CNiyVHxKoH3DgF-8ldwVLmAZFGUkNLPRS5zfOQUSBxLXlg8X0x_RKXrHrBI-2cswvg",
    },
    {
        "id": "metropoles.br", "name": "Metrópoles", "platform": "youtube",
        "url": "https://www.youtube.com/Metr%C3%B3polesTV/streams",
        "logo": "https://play-lh.googleusercontent.com/Eod-arKwRBPDNBTlZXrXGUvNb4vX1KF038waVYZnDW5jpULjX6MLyd2NHeiXk9EkHQ",
    },
    {
        "id": "nbabrasil.br", "name": "NBA Brasil", "platform": "youtube",
        "url": "https://www.youtube.com/@nbabrasil/streams",
        "logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/united-states/nba-tv-us.png?raw=true",
    },
    {
        "id": "paulista.br", "name": "Paulista", "platform": "youtube",
        "url": "https://www.youtube.com/@futebolpaulista/streams",
        "logo": "https://logodownload.org/wp-content/uploads/2020/01/fpf-federacao-paulista-de-futebol-logo-0.png",
    },
    {
        "id": "paulistao.br", "name": "Paulistão", "platform": "youtube",
        "url": "https://www.youtube.com/paulistao/streams",
        "logo": "https://logodownload.org/wp-content/uploads/2020/01/fpf-federacao-paulista-de-futebol-logo-0.png",
    },
    {
        "id": "gauchao.br", "name": "Federação Gaúcha", "platform": "youtube",
        "url": "https://www.youtube.com/@FGFTV/streams",
        "logo": "https://cdn.freebiesupply.com/logos/large/2x/federacao-gaucha-de-futebol-rs-logo-svg-vector.svg",
    },
    {
        "id": "catarinense.br", "name": "Federação Catarinense", "platform": "youtube",
        "url": "https://www.youtube.com/@fcf_futebol/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/6/64/FCFsc.png",
    },
    {
        "id": "sdplives.br", "name": "SDP", "platform": "youtube",
        "url": "https://www.youtube.com/SDPLivesEsportivas/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/ba/SDP_Logo.png",
    },
    {
        "id": "canaldofabricio.br", "name": "Canal do Fabrício", "platform": "youtube",
        "url": "https://www.youtube.com/@ocanaldofabricio/streams",
        "logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsERCiMmfLUlKzMsTzY_vSABSXO_77HpOgkg&s",
    },
    {
        "id": "caterinensefutsal.br", "name": "Catarinense Futsal", "platform": "youtube",
        "url": "https://www.youtube.com/@catarinensefutsal/streams",
        "logo": "https://placarsoft-fcfs.nyc3.digitaloceanspaces.com/01/setting/d3/0a/368359963854250271/fcfs-escudo-368361547053018944.png",
    },
    {
        "id": "carvoeirodoentetv.br", "name": "Carvoeiro Doente TV", "platform": "youtube",
        "url": "https://www.youtube.com/@CarvoeiroDoenteTV/streams",
        "logo": "data:image/jpeg;base64,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",
    }
]

# --- DADOS DOS CANAIS GLOBO PLAY ---
GLOBOPLAY_CHANNELS = [
    {
        "name": "Sportv 4K",
        "video_id": "11529241",
        "tvg_id": "sportv(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/sportv-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "Sportv 1",
        "video_id": "7339108",
        "tvg_id": "sportv(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/sportv-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "Sportv 2",
        "video_id": "7339117",
        "tvg_id": "sportv2(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/sportv2-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "Sportv 3",
        "video_id": "7339123",
        "tvg_id": "sportv3(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/sportv3-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "Globo NSC",
        "video_id": "6120663",
        "tvg_id": "NSCTVCriciuma(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/globo-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "MultiShow",
        "video_id": "7339131",
        "tvg_id": "Multishow(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/multishow-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "BIS",
        "video_id": "7339140",
        "tvg_id": "BIS(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/bis-br.png?raw=true",
        "group_title": "GloboPlay"
    },
    {
        "name": "GloboNews",
        "video_id": "7339101",
        "tvg_id": "GloboNews(Portuguese).br",
        "tvg_logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/globo-news-br.png?raw=true",
        "group_title": "GloboPlay"
    }
]