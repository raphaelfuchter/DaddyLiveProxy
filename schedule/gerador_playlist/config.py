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
    "Motorsports": "Automobilismo",
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
    "Rugby League": "Rugby",
    "Rugby Union": "Rugby",
    "Beach Soccer": "Futebol de Areia",
    "Biathlon": "Biatlo",
    "Climbing": "Escalada",
    "Sailing / Boating": "Vela",

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
        "id": "gauleskick.br", "name": "Gaules Kick", "platform": "kick",
        "url": "https://www.kick.com/gaules",
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
        "id": "thedarknesskick.br", "name": "TheDarkness Kick", "platform": "kick",
        "url": "http://kick.com/thedarknesspgdm",
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
        "id": "brksedu.br", "name": "BRKsEDU", "platform": "youtube",
        "url": "https://www.youtube.com/BRKsEDU/streams",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/brksedu-profile_image-8068004d415ba841-300x300.png",
    },
    {
        "id": "flowgames.br", "name": "Flow Games", "platform": "youtube",
        "url": "https://www.youtube.com/@FlowGamesPodcast/streams",
        "logo": "https://flowgames.gg/wp-content/uploads/2022/10/logo.png",
    },
    {
        "id": "gaules.br", "name": "Gaules", "platform": "youtube",
        "url": "https://www.youtube.com/gaules/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Gaules_logo_blue.svg/2560px-Gaules_logo_blue.svg.png",
    },
    {
        "id": "toptvsports.br", "name": "TopTV Sports", "platform": "youtube",
        "url": "https://www.youtube.com/@TopTVSports/streams",
        "logo": "https://play-lh.googleusercontent.com/CNiyVHxKoH3DgF-8ldwVLmAZFGUkNLPRS5zfOQUSBxLXlg8X0x_RKXrHrBI-2cswvg",
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
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/EscudoCriciumaEC.svg/2560px-EscudoCriciumaEC.svg.png",
    },
    {
        "id": "metropoles.br", "name": "Metrópoles", "platform": "youtube",
        "url": "https://www.youtube.com/Metr%C3%B3polesTV/streams",
        "logo": "https://play-lh.googleusercontent.com/Eod-arKwRBPDNBTlZXrXGUvNb4vX1KF038waVYZnDW5jpULjX6MLyd2NHeiXk9EkHQ",
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