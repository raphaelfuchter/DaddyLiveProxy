# 1. Imagem base com Python
# Usamos uma imagem "slim" que é menor e mais otimizada.
FROM python:3.9-slim

# 2. Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copia todos os arquivos da pasta atual (incluindo a pasta "playlist") para o diretório de trabalho no contêiner
COPY . .

# 4. Expõe a porta que o servidor usa
# Isso informa ao Docker que o contêiner escutará na porta 8007.
EXPOSE 8007

# 5. Comando para executar quando o contêiner iniciar
# O "-u" (unbuffered) faz com que os "prints" do Python apareçam nos logs do Docker em tempo real.
CMD ["python", "-u", "init_server.py"]