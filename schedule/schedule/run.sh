#!/bin/bash

while true
do
  echo "----------------------------------------"
  echo "Executando o script: $(date)"
  echo "----------------------------------------"
  
  # Executa o seu script Python
  python schedule_down.py
  
  echo "----------------------------------------"
  echo "Execução concluída. Aguardando 30 minutos..."
  echo "----------------------------------------"
  
  # Espera 30 minutos (1800 segundos)
  sleep 1800
done