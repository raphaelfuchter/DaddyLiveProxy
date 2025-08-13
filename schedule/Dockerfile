# Dockerfile para o projeto do Gerador

# 1. Imagem base com Python
FROM python:3.9-slim

# 2. Evita prompts interativos durante a construção da imagem
ENV DEBIAN_FRONTEND=noninteractive

# 3. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Instala dependências do sistema e o Google Chrome de forma segura e otimizada
RUN apt-get update && apt-get install -y \
    # Dependências para o Chrome e outras ferramentas
    wget \
    gnupg \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libfontconfig1 \
    # O pacote problemático libgconf-2-4 foi REMOVIDO
    && \
    # Instalação SEGURA do Google Chrome (método moderno)
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    # Limpa o cache do apt para reduzir o tamanho da imagem
    rm -rf /var/lib/apt/lists/*

# 5. Copia o arquivo de dependências do Python
COPY requirements.txt .

# 6. Instala as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copia o seu script Python para o contêiner
COPY app.py .

# 8. Cria as pastas que o script precisa (opcional, mas mantido do seu original)
RUN mkdir -p output cache

# 9. Expõe a porta que o servidor HTTP irá usar
EXPOSE 8007

# 10. Comando para executar o script em tempo real
CMD ["python", "-u", "app.py"]