# main.py

import os
import time
import threading
import http.server
import socketserver
from datetime import datetime, timedelta, timezone

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Importando da nossa nova estrutura de pacotes
from gerador_playlist import config, utils, scraper, generators


def gerador_main():
    """Função principal que orquestra a geração da playlist e EPG."""
    print("--- Gerador de Playlist e EPG ---")

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if not GITHUB_TOKEN:
        print("\nAVISO: GITHUB_TOKEN não definida.")

    logo_cache = utils.obter_urls_logos_com_cache(GITHUB_TOKEN)

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
        stream_data = scraper.extract_streams_with_selenium(driver, config.SCHEDULE_PAGE_URL, logo_cache)
    finally:
        if driver:
            print("\nProcesso de extração finalizado. Fechando o navegador.")
            driver.quit()

    now_utc = datetime.now(timezone.utc)
    filtered_streams = [
        s for s in stream_data
        if (datetime.fromtimestamp(int(s['start_timestamp_ms']) / 1000, tz=timezone.utc) + timedelta(
            hours=config.EPG_EVENT_DURATION_HOURS)) >=
           (now_utc - timedelta(hours=(config.EPG_PAST_EVENT_CUTOFF_HOURS_FUTEBOL if s[
                                                                                         'sport'] == 'Futebol' else config.EPG_PAST_EVENT_CUTOFF_HOURS)))
    ] if stream_data else []

    if stream_data:
        print(f"\nStreams extraídos: {len(stream_data)}. Válidos após filtro: {len(filtered_streams)}.")
        if not filtered_streams:
            print("Nenhum evento futuro ou em andamento encontrado.")
    else:
        print("\nNenhum stream dinâmico foi extraído.")

    # Gerar e salvar arquivos
    m3u8_content = generators.generate_m3u8_content(filtered_streams)
    epg_content = generators.generate_xmltv_epg(filtered_streams)

    try:
        with open(config.M3U8_OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            f.write(m3u8_content)
        print(f"✅ Sucesso! Arquivo '{config.M3U8_OUTPUT_FILENAME}' gerado.")
    except IOError as e:
        print(f"❌ ERRO ao salvar M3U8: {e}")

    try:
        with open(config.EPG_OUTPUT_FILENAME, "w", encoding="utf-8") as f:
            f.write(epg_content)
        print(f"✅ Sucesso! Arquivo '{config.EPG_OUTPUT_FILENAME}' gerado.")
    except IOError as e:
        print(f"❌ ERRO ao salvar EPG: {e}")


def loop_de_atualizacao():
    """Loop infinito que chama o gerador em intervalos de 30 minutos."""
    while True:
        agora = datetime.now()
        proxima_execucao = (agora + timedelta(minutes=30)).replace(minute=(0 if agora.minute >= 30 else 30), second=0,
                                                                   microsecond=0)

        espera_segundos = (proxima_execucao - agora).total_seconds()
        print(
            f"\n{'=' * 50}\nCiclo finalizado. Próxima atualização: {proxima_execucao.strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 50}\n")

        if espera_segundos > 0:
            time.sleep(espera_segundos)

        print(f"\n{'=' * 50}\nHORA DA ATUALIZAÇÃO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'=' * 50}")
        try:
            gerador_main()
        except Exception as e:
            print(f"❌ ERRO INESPERADO DURANTE A EXECUÇÃO DO GERADOR: {e}")


def iniciar_servidor():
    """Inicia um servidor HTTP simples para servir os arquivos gerados."""
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", config.SERVER_PORT), handler) as httpd:
        print("\n\n--- Servidor HTTP iniciado ---")
        print(f"Servindo na porta {config.SERVER_PORT}.")
        print(f"Playlist M3U8: http://{config.SERVER_IP}:{config.SERVER_PORT}/{config.M3U8_OUTPUT_FILENAME}")
        print(f"Guia EPG XML:  http://{config.SERVER_IP}:{config.SERVER_PORT}/{config.EPG_OUTPUT_FILENAME}")
        httpd.serve_forever()


if __name__ == "__main__":
    print("Executando o gerador pela primeira vez...")
    try:
        gerador_main()
    except Exception as e:
        print(f"❌ ERRO NA EXECUÇÃO INICIAL DO GERADOR: {e}")

    print("\nIniciando a thread de atualizações futuras...")
    gerador_thread = threading.Thread(target=loop_de_atualizacao, daemon=True)
    gerador_thread.start()

    iniciar_servidor()