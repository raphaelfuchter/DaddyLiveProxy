import http.server
import socketserver
import os

# --- Configuração ---
# IP local fixo para garantir que o endereço esteja sempre correto
IP_LOCAL = "192.168.68.19"
# Porta que o servidor irá usar
PORT = 8007
# --- Fim da Configuração ---


# Inicia o servidor
# Usar "0.0.0.0" garante que o servidor seja acessível por outros dispositivos na rede
with socketserver.TCPServer(("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f"--- Servidor HTTP iniciado ---")
    print(f"Seu script gerou a playlist e o EPG.")
    print(f"\nUse os seguintes links nos seus dispositivos na mesma rede:")
    print(f"  Playlist M3U8: http://{IP_LOCAL}:{PORT}/schedule_playlist.m3u8")
    print(f"  Guia EPG XML:  http://{IP_LOCAL}:{PORT}/epg.xml")
    print(f"\nPara parar o servidor, pressione Ctrl+C no terminal.")
    httpd.serve_forever()