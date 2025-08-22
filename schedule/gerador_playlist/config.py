# gerador_playlist/config.py

from datetime import timedelta, timezone

# --- Configuração do Gerador ---
SCHEDULE_PAGE_URL = "http://192.168.68.19:3000/api/schedule/"
M3U8_OUTPUT_FILENAME = "schedule_playlist.m3u8"
EPG_OUTPUT_FILENAME = "epg.xml"
LOGO_CACHE_FILE = "logo_cache.json"
EPG_EVENT_DURATION_HOURS = 2
EPG_EVENT_DURATION_HOURS_FUTEBOL_AMERICANO = 3
GROUP_SORT_ORDER = ["Futebol", "Basquete", "Futebol Americano", "Automobilismo", "Hóquei no Gelo", "Beisebol", "Programas de TV", "Tênis", "Futsal", "MMA"]
EPG_PAST_EVENT_CUTOFF_HOURS = 0.5
EPG_PAST_EVENT_CUTOFF_HOURS_FUTEBOL = 0.5
EPG_LOCAL_TIMEZONE_OFFSET_HOURS = -3
GITHUB_API_URL = "https://api.github.com/repos/tv-logo/tv-logos/contents/countries"
LOGO_CACHE_EXPIRATION_HOURS = 2
DEFAULT_SPORT_ICON = "https://raw.githubusercontent.com/raphaelfuchter/DaddyLiveProxy/refs/heads/master/schedule/schedule/logos/sports.png"
PLACEHOLDER_TEXT = "Offline"
SERVER_IP = "192.168.68.19"
SERVER_PORT = 8007
LOCAL_TZ = timezone(timedelta(hours=EPG_LOCAL_TIMEZONE_OFFSET_HOURS))

# --- Mapeamentos ---
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
        "url": "https://www.youtube.com/@CazeTV/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/2/22/Logotipo_da_Caz%C3%A9TV.png",
    },
    {
        "id": "canalgoat.br", "name": "Canal Goat", "platform": "youtube",
        "url": "https://www.youtube.com/@canalgoatbr/streams",
        "logo": "https://canalgoat.com.br/wp-content/uploads/2024/10/Canal-Goat-Escudo-Color.png",
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
        "logo": "https://fgf.com.br/marcas/logo_FGF.png",
    },
    {
        "id": "catarinense.br", "name": "Federação Catarinense", "platform": "youtube",
        "url": "https://www.youtube.com/@fcf_futebol/streams",
        "logo": "https://images.seeklogo.com/logo-png/5/2/federacao-catarinense-de-futebol-sc-br-logo-png_seeklogo-53294.png",
    },
    {
        "id": "sportynetbrasil.br", "name": "SportyNet", "platform": "youtube",
        "url": "https://www.youtube.com/@SportyNetBrasil/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/SportyNet.png/500px-SportyNet.png",
    },
    {
        "id": "sdplives.br", "name": "SDP", "platform": "youtube",
        "url": "https://www.youtube.com/SDPLivesEsportivas/streams",
        "logo": "https://yt3.googleusercontent.com/39TgdCB7Creiv2ymMKfksMzmbS2jbbK8d6-ZIBTQKPlLoHjg9KY4bA-AKSZP8S2rrMHh8dPC9qs=s900-c-k-c0x00ffffff-no-rj",
    },
    {
        "id": "canalcnsl.br", "name": "Canal CN", "platform": "youtube",
        "url": "https://www.youtube.com/@CanalCNSL/streams",
        "logo": "https://instagram.fccm4-1.fna.fbcdn.net/v/t51.2885-19/293333104_802178497622384_7106071998501232957_n.jpg?stp=dst-jpg_s150x150_tt6&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby41MzkuY2FuYXJ5In0&_nc_ht=instagram.fccm4-1.fna.fbcdn.net&_nc_cat=108&_nc_oc=Q6cZ2QE9SW7Zwm3tJjB_Kll2sgSzTj-EAesq_4TnvB3REAlexQn0ghD5Ala4n15vGm_lx3I&_nc_ohc=xMibaOswx0cQ7kNvwH3Se4q&_nc_gid=Hxt0n6m_NXWa9RpDxPLS_A&edm=AOQ1c0wBAAAA&ccb=7-5&oh=00_AfUd973zji3tmXwxdovcvv6TWNVQF9JphQmelmKtHlfm4Q&oe=68AEE450&_nc_sid=8b3546",
    }
]