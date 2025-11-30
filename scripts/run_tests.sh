#!/bin/bash

# Define cores para saída bonita no terminal
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN} Iniciando Pipeline de Testes...${NC}"

# Derruba containers antigos para garantir um ambiente limpo
echo " Limpando ambiente anterior..."
docker-compose down --remove-orphans

# Constrói e sobe os containers em background
echo " Construindo e subindo containers..."
# Adicione --build se quiser forçar o rebuild sempre
docker-compose up -d --build

# Aguarda o banco de dados
sleep 5 

# Executa os testes via Pytest dentro do container 'web'
echo " Executando testes..."
docker-compose exec -T web pytest

# Captura o código de saída do pytest (0 = sucesso, 1 = falha)
TEST_EXIT_CODE=$?

# Derruba o ambiente
echo " Finalizando ambiente..."
docker-compose down

# Verifica o resultado
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN} Todos os testes passaram com sucesso!${NC}"
    exit 0
else
    echo -e "${RED} Falha nos testes.${NC}"
    exit 1
fi