# 1. Imagem base com Python
FROM python:3.9-slim

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copia apenas o script para o diretório de trabalho no contêiner
COPY init_server.py .

# 4. Expõe a porta que o servidor usa
EXPOSE 8007

# 5. Comando para executar quando o contêiner iniciar
CMD ["python", "-u", "init_server.py"]