# Dockerfile para o projeto unificado (Gerador + Servidor)

# 1. Imagem base com Python
FROM python:3.9-slim

# 2. Evita prompts interativos durante a construção da imagem
ENV DEBIAN_FRONTEND=noninteractive

# 3. Instala as dependências do sistema necessárias para o Google Chrome headless
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Baixa e instala a versão estável do Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# 5. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 6. Copia o arquivo de dependências do Python para o contêiner
COPY requirements.txt .

# 7. Instala as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copia o seu script Python unificado para o contêiner
#    (Assumindo que você o salvou como 'app.py')
COPY app.py .

# 9. Cria as pastas de saída e de cache que o script precisa para funcionar
RUN mkdir -p output cache

# 10. Expõe a porta que o servidor HTTP irá usar
EXPOSE 8007

# 11. Comando para executar o script quando o contêiner iniciar
#     O '-u' garante que os 'prints' do Python apareçam nos logs do Docker em tempo real
CMD ["python", "-u", "app.py"]