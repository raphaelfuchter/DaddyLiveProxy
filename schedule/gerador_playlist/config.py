# gerador_playlist/config.py

from datetime import timedelta, timezone

# --- Configuração do Gerador ---
SCHEDULE_PAGE_URL = "http://192.168.68.19:3000/api/schedule/"
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
    "USL Championship": "Futebol",
    "Scotland Premiership": "Futebol",

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

    "Winter Sports": "Esportes de Inverno"
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
        "id": "espnbrasilyt.br", "name": "ESPN Brasil", "platform": "youtube",
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
        "logo": "data:image/png;base64,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",
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