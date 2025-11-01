# gerador_playlist/config.py
import os
from datetime import timedelta, timezone

# --- Configuração do Gerador ---
SCHEDULE_PAGE_URL = os.getenv("API_URL") + "/api/schedule/"
M3U8_OUTPUT_FILENAME = "schedule_playlist.m3u8"
EPG_OUTPUT_FILENAME = "epg.xml"
LOGO_CACHE_FILE = "logo_cache.json"
EPG_EVENT_DURATION_HOURS = 3
EPG_EVENT_DURATION_HOURS_FUTEBOL = 2
GROUP_SORT_ORDER = ["Futebol", "Basquete", "Futebol Americano", "Hóquei"]
EPG_PAST_EVENT_CUTOFF_HOURS = 0
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
    "All Soccer Events": "Futebol",
    "England - Championship": "Futebol",
    "England - Championship/League One": "Futebol",
    "England - Championship/League One/League Two": "Futebol",
    "England - Championship/League One/League Two/Scottish": "Futebol",
    "England – Championship/League One/League Two/Scottish": "Futebol",
    "England - Championship/EFL Trophy/League One": "Futebol",
    "England - EFL Trophy": "Futebol",
    "England - League One": "Futebol",
    "England - League One/League Two": "Futebol",
    "England - League Two": "Futebol",
    "Major League Soccer": "Futebol",
    "Major League Soccer (MLS)": "Futebol",
    "Soccer - Ireland Republic": "Futebol",
    "Ireland Republic": "Futebol",
    "USL Championship": "Futebol",
    "Scotland Premiership": "Futebol",
    "Premiership Scotland": "Futebol",

    "Basketball": "Basquete",
    "Basketball (NBA)": "Basquete",
    "Basketball (WNBA)": "Basquete",
    "NBA": "Basquete",
    "WNBA": "Basquete",
    "WNBA FINALS": "Basquete",

    "Am. Football": "Futebol Americano",
    "NFL": "Futebol Americano",
    "NCAAF": "Futebol Americano",
    "Am. Football (NCAAF)": "Futebol Americano",
    "Am. Football (NFL)": "Futebol Americano",
    "NCAA College Football": "Futebol Americano",

    "Motorsport": "Automobilismo",
    "Motorsports": "Automobilismo",

    "TV Shows": "Programas de TV",
    "TV Show": "Programas de TV",
    "Big Brother 27 USA 2025 Live": "Programas de TV",
    "Big Brother Naija 2025 Live": "Programas de TV",

    "Baseball": "Beisebol",
    "Baseball (MLB)": "Beisebol",
    "MLB": "Beisebol",

    "Ice Hockey": "Hóquei",
    "Ice Hockey (NHL)": "Hóquei",
    "NHL": "Hóquei",
    "NCAA Ice Hockey": "Hóquei",

    "Tennis": "Tênis",
    "Table Tennis": "Tênis de Mesa",

    "Athletics": "Atletismo",
    "Athletic": "Atletismo",

    "Horse Racing": "Cavalo",
    "Equestrian": "Cavalo",

    "Cricket": "Críquete",
    "Snooker": "Sinuca",
    "Golf": "Golfe",
    "Water polo": "Polo Aquático",
    "Waterpolo": "Polo Aquático",
    "Water Sports": "Esportes Aquáticos",

    "Rugby League": "Rugby",
    "Rugby Union": "Rugby",
    
    "Beach Soccer": "Futebol de Areia",
    "Biathlon": "Biatlo",
    "Triathlon": "Triatlo",
    "Climbing": "Escalada",
    "Sailing / Boating": "Vela",

    "WWE": "Luta Livre",
    "WWE (RAW)": "Luta Livre",
    "WWE (NXT)": "Luta Livre",

    "Badminton": "Badminton",
    "Darts": "Dardos",
    "Boxing": "Boxe",
    "Cycling": "Ciclismo",
    "Bowling": "Boliche",

    "Volleyball": "Voleibol",
    "NCAA Women's Volleyball": "Voleibol",
    "Beach Volleyball": "Voleibol de Praia",

    "Fencing": "Esgrima",
    "Field Hockey": "Hóquei na Grama",
    "Handball": "Handebol",
    "Gymnastics": "Ginástica",
    "PPV Events": "Eventos PPV",

    "Aussie rules": "Futebol Australiano",
    "Aussie Rules": "Futebol Australiano",
    "Aussie Rules (AFL)": "Futebol Australiano",
    "Aussie rules (AFL)": "Futebol Australiano",

    "Winter Sports": "Esportes de Inverno",
    "Ice Skating": "Patinação no Gelo"

}

STATIC_CHANNELS = [
    {
        "id": "cazetv.br", "name": "CazéTV", "platform": "youtube",
        "url": "https://www.youtube.com/@CazeTV/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/2/22/Logotipo_da_Caz%C3%A9TV.png",
    },
    {
        "id": "getv.br", "name": "geTV", "platform": "youtube",
        "url": "https://www.youtube.com/@getv/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/0/03/GE_TV.png",
    },
    {
        "id": "esbrasilyt.br", "name": "ESPN Brasil YouTube", "platform": "youtube",
        "url": "https://www.youtube.com/@espnbrasil/streams",
        "logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/united-states/espn-us.png?raw=true",
    },
    {
        "id": "canalgoat.br", "name": "Canal Goat", "platform": "youtube",
        "url": "https://www.youtube.com/@canalgoatbr/streams",
        "logo": "https://canalgoat.com.br/wp-content/uploads/2024/10/Canal-Goat-Escudo-Color.png",
    },
    {
        "id": "desimpedidos.br", "name": "Desimpedidos", "platform": "youtube",
        "url": "https://www.youtube.com/desimpedidos/streams",
        "logo": "https://desimpedidos.com.br/assets/logos/LOGO_DESIMPEDIDOS_BRANCO.png",
    },
    {
        "id": "sportynetbrasil.br", "name": "SportyNet", "platform": "youtube",
        "url": "https://www.youtube.com/@SportyNetBrasil/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/SportyNet.png/500px-SportyNet.png",
    },
    {
        "id": "tntsportsbr.br", "name": "TNT Sports", "platform": "youtube",
        "url": "https://www.youtube.com/@TNTSportsBR/streams",
        "logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/brazil/tnt-br.png?raw=true",
    },
    {
        "id": "nbabrasil.br", "name": "NBA Brasil", "platform": "youtube",
        "url": "https://www.youtube.com/@nbabrasil/streams",
        "logo": "https://github.com/tv-logo/tv-logos/blob/main/countries/united-states/nba-tv-us.png?raw=true",
    },
    {
        "id": "xsports.br", "name": "XSports", "platform": "youtube",
        "url": "https://www.youtube.com/@xsports.brasil/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Xsports_logo.png",
    },
    {
        "id": "catarinense.br", "name": "Federação Catarinense", "platform": "youtube",
        "url": "https://www.youtube.com/@fcf_futebol/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/6/64/FCFsc.png",
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
        "id": "toptvsports.br", "name": "TopTV Sports", "platform": "youtube",
        "url": "https://www.youtube.com/@TopTVSports/streams",
        "logo": "https://play-lh.googleusercontent.com/CNiyVHxKoH3DgF-8ldwVLmAZFGUkNLPRS5zfOQUSBxLXlg8X0x_RKXrHrBI-2cswvg",
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
        "id": "canalcn.br", "name": "Canal CN", "platform": "youtube",
        "url": "https://www.youtube.com/@CanalCNSL/streams",
        "logo": "https://yt3.googleusercontent.com/DxIQ6cI1fqqj-LgHuHMGWLAUdyy2gB5EL1mojWhy1uACz-_xvuXv3SjUZZXcRADJ0MnrKfATqg=s160-c-k-c0x00ffffff-no-rj",
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
        "id": "kingleaguebrasil.br", "name": "Kings League Brasil", "platform": "youtube",
        "url": "https://www.youtube.com/@KingsLeagueBrazil/streams",
        "logo": "https://www.eventim.com.br/obj/media/BR-eventim/galery/222x222/k/kingsleaguebrazil-eventim-lineupartista.png",
    },
    {
        "id": "gauleskick.br", "name": "Gaules", "platform": "kick",
        "url": "https://www.kick.com/gaules",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Gaules_logo_blue.svg/2560px-Gaules_logo_blue.svg.png",
    },
    {
        "id": "madhouse.br", "name": "MadHouse", "platform": "youtube",
        "url": "https://www.youtube.com/@madhouse_tv/streams",
        "logo": "https://yt3.googleusercontent.com/_M2g8lJ9um3e2P_s27WNrStVeCiXhnZb4PrNF3tdM73Xd1iywqM6sI7XQOLV-j5ODaNzGLBiBg=s900-c-k-c0x00ffffff-no-rj",
    },
    {
        "id": "coringa.br", "name": "Coringa", "platform": "kick",
        "url": "https://kick.com/coringa",
        "logo": "https://files.kick.com/images/user/4204697/profile_image/conversion/6bfa12a8-780a-43ed-9950-2388580ebbb1-fullsize.webp",
    },
    {
        "id": "zigueira.br", "name": "Zigueira", "platform": "kick",
        "url": "https://kick.com/zigueira",
        "logo": "https://files.kick.com/images/user/55276375/profile_image/bc9947ee-9f86-4036-8236-82252e8c4d9c",
    },
    {
        "id": "thedarknesskick.br", "name": "TheDarkness", "platform": "kick",
        "url": "http://kick.com/thedarkness",
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
        "id": "casemiro.br", "name": "Casemiro", "platform": "twitch",
        "url": "https://www.twitch.tv/casimito",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/32805a78-d927-48bd-8089-bf5efed53ea4-profile_image-70x70.png",
    },
    {
        "id": "yuukiing.br", "name": "YUUKiing", "platform": "kick",
        "url": "https://kick.com/yuukiing",
        "logo": "https://pbs.twimg.com/profile_images/1816896313641869312/gYGgEA81_400x400.jpg",
    },
    {
        "id": "onezera.br", "name": "One", "platform": "kick",
        "url": "https://kick.com/onezeratv",
        "logo": "https://files.kick.com/images/user/8737828/profile_image/conversion/1567d37f-bfc1-4ff1-bfe5-f7f420dfaf98-fullsize.webp",
    },
    {
        "id": "diogo1.br", "name": "DIOGO1fps", "platform": "kick",
        "url": "https://kick.com/diogo1fps",
        "logo": "https://files.kick.com/images/user/11972307/profile_image/conversion/01921796-ab08-4880-af25-2dbfe81302e9-fullsize.webp",
    },
    {
        "id": "sks.br", "name": "SkS", "platform": "kick",
        "url": "https://kick.com/sksfps1",
        "logo": "https://files.kick.com/images/user/55762018/profile_image/conversion/374dc3fe-80df-4c3c-bb23-214cda57548c-fullsize.webp",
    },
    {
        "id": "liminha.br", "name": "Liminha", "platform": "kick",
        "url": "https://kick.com/liminhag0d",
        "logo": "https://files.kick.com/images/user/53038940/profile_image/conversion/796a002a-d309-46d3-b5ff-ba1d6ef7ac42-fullsize.webp",
    },
{
        "id": "revo1tzgg.br", "name": "Revo1Tzgg", "platform": "twitch",
        "url": "https://www.twitch.tv/revo1tzgg",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/6f1a3f1b-bd6c-404a-9bc3-ab099e7a60af-profile_image-70x70.png",
    },
    {
        "id": "shroud.br", "name": "Shroud", "platform": "twitch",
        "url": "https://www.twitch.tv/shroud",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/7ed5e0c6-0191-4eef-8328-4af6e4ea5318-profile_image-70x70.png",
    },
    {
        "id": "summit1g.br", "name": "Summit1g", "platform": "twitch",
        "url": "https://www.twitch.tv/summit1g",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/99aa4739-21d6-40af-86ae-4b4d3457fce4-profile_image-70x70.png",
    },
    {
        "id": "skadoodle.br", "name": "Skadoodle", "platform": "twitch",
        "url": "https://www.twitch.tv/skadoodle",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/8d88427e-923e-4613-97cb-390b4efab238-profile_image-70x70.png",
    },
    {
        "id": "tecnosh.br", "name": "Tecnosh", "platform": "kick",
        "url": "https://www.kick.com/tecnosh",
        "logo": "https://files.kick.com/images/user/80483557/profile_image/conversion/4f7e564f-128c-4f4d-b04b-68a8636156ca-fullsize.webp",
    },
    {
        "id": "brino.br", "name": "Brino", "platform": "twitch",
        "url": "https://www.twitch.tv/brino",
        "logo": "https://static-cdn.jtvnw.net/jtv_user_pictures/62c899c1-fdda-4d3a-aefc-7993c41c1618-profile_image-70x70.png",
    },
    {
        "id": "coreano.br", "name": "Coreano", "platform": "kick",
        "url": "https://kick.com/coreano",
        "logo": "https://files.kick.com/images/user/8829981/profile_image/conversion/5d8b0dc8-7500-4cb6-b206-f0a6165e33af-fullsize.webp",
    },
    {
        "id": "valorantbr.br", "name": "Valorant Sports", "platform": "youtube",
        "url": "https://www.youtube.com/valorantesportsbr/streams",
        "logo": "https://freelogopng.com/images/all_img/1664302686valorant-icon-png.png",
    },
    {
        "id": "rainbow6br.br", "name": "Rainbow6 BR", "platform": "youtube",
        "url": "https://www.youtube.com/@Rainbow6BR/streams",
        "logo": "https://yt3.googleusercontent.com/Wn05v8kKrKqv7mGzA7PtvP0bK3WvOKCQQHgFhLXX_qTsDWC0RF5rtMFv2La_UOHbnUB4JGkAgls=s160-c-k-c0x00ffffff-no-rj",
    },
    {
        "id": "gaules.br", "name": "Gaules", "platform": "youtube",
        "url": "https://www.youtube.com/gaules/streams",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Gaules_logo_blue.svg/2560px-Gaules_logo_blue.svg.png",
    },
    {
        "id": "metropolesesportes.br", "name": "Metrópoles Esportes", "platform": "youtube",
        "url": "https://www.youtube.com/@MetropolesEsportes/streams",
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
        "name": "GE TV",
        "video_id": "11134179",
        "tvg_id": "Sports.Dummy.us",
        "tvg_logo": "https://upload.wikimedia.org/wikipedia/commons/0/03/GE_TV.png",
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