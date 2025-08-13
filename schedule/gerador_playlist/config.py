# gerador_playlist/config.py

from datetime import timedelta, timezone

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