import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlsplit, parse_qs
import urllib3

# Desabilita os avisos de SSL (por causa do verify=False)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuração ---
URL = "https://dlhd.dad/"


# --------------------

def extrair_schedule():
    """
    Este script acessa a URL e extrai a agenda, retornando um JSON
    no formato:
    {
        "Dia String Completa": {
            "Categoria String": [
                { "event": ..., "time": ..., "channels": [...], "channels2": [] },
                ...
            ]
        }
    }
    Ignorando as seções "Extra".
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 1. Baixar o conteúdo HTML da página
        print(f"Acessando {URL}...")
        response = requests.get(URL, headers=headers, verify=False)
        response.raise_for_status()
        print("Página baixada com sucesso.")

        # 2. Iniciar o BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # ESTRUTURA PRINCIPAL: Um dicionário de dias
        schedule_final_agrupado = {}

        # ### MUDANÇA IMPORTANTE ###
        # 3. Encontrar o container da agenda principal PELO ID
        # Isso evita que ele pegue os "Extra Schedule"
        main_schedule_div = soup.find('div', id='schedule')

        if not main_schedule_div:
            print("Não foi possível encontrar o container principal da agenda (id='schedule').")
            return None

        # 4. Encontrar todos os blocos de 'dia' APENAS DENTRO do container principal
        blocos_dia = main_schedule_div.find_all('div', class_='schedule__day')

        if not blocos_dia:
            print("Nenhum bloco de dia ('schedule__day') encontrado dentro de id='schedule'.")
            return None

        print(f"Encontrados {len(blocos_dia)} blocos de dia. Processando...")

        for dia_div in blocos_dia:
            # 5. Extrair o título do dia (string completa)
            dia_title_element = dia_div.find('div', class_='schedule__dayTitle')
            if not dia_title_element:
                continue

            dia_atual_raw = dia_title_element.get_text(strip=True)  # Ex: "Monday 20th Oct2025 - Schedule Time UK GMT"

            categorias_deste_dia = {}
            schedule_final_agrupado[dia_atual_raw] = categorias_deste_dia

            # 6. Encontrar todas as 'categorias' DENTRO deste dia
            categorias = dia_div.find_all('div', class_='schedule__category')

            if not categorias:
                continue

            for categoria_div in categorias:
                # 7. Extrair o nome da categoria
                categoria_meta = categoria_div.find('div', class_='card__meta')
                if not categoria_meta:
                    continue

                nome_categoria = categoria_meta.get_text(strip=True)  # Ex: "TV Shows"

                eventos_desta_categoria = []
                categorias_deste_dia[nome_categoria] = eventos_desta_categoria

                # 8. Encontrar todos os 'eventos' dentro desta categoria
                eventos = categoria_div.find_all('div', class_='schedule__event')

                for evento_div in eventos:

                    time_span = evento_div.find('span', class_='schedule__time')
                    hora_evento = time_span.get_text(strip=True) if time_span else 'N/A'

                    title_span = evento_div.find('span', class_='schedule__eventTitle')
                    titulo_evento = title_span.get_text(strip=True) if title_span else 'N/A'

                    canais_lista = []
                    channels_div = evento_div.find('div', class_='schedule__channels')

                    if channels_div:
                        links_canais = channels_div.find_all('a')
                        for link in links_canais:
                            nome_canal = link.get_text(strip=True)
                            href = link.get('href')
                            channel_id = 'N/A'
                            if href:
                                try:
                                    query_params = parse_qs(urlsplit(href).query)
                                    if 'id' in query_params:
                                        channel_id = query_params['id'][0]
                                except Exception:
                                    pass

                            canais_lista.append({
                                "channel_name": nome_canal,
                                "channel_id": channel_id
                            })

                    # 9. Montar o objeto de evento no formato esperado pelo schedule.py
                    evento_obj = {
                        "time": hora_evento,
                        "event": titulo_evento,
                        "channels": canais_lista,
                        "channels2": []  # Adicionado para corresponder ao schedule.py
                    }
                    eventos_desta_categoria.append(evento_obj)

        if schedule_final_agrupado:
            print("\n--- EXTRAÇÃO CONCLUÍDA ---")
            # 10. Retornar o resultado completo como JSON
            return json.dumps(schedule_final_agrupado, ensure_ascii=False)
        else:
            print("Nenhum evento individual foi extraído.")
            return None  # Retorna None se nada for encontrado


    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP ao acessar a página: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de rede ao acessar a página: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

# Remova ou comente o bloco if __name__ == "__main__"
# if __name__ == "__main__":
#     print(extrair_schedule())