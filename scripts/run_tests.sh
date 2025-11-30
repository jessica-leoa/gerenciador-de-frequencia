#!/bin/bash


GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' 

echo -e "${GREEN} Iniciando Pipeline de Testes...${NC}"


echo " Limpando ambiente anterior..."
docker compose down --remove-orphans


echo " Construindo e subindo containers..."

docker compose up -d --build


sleep 5 


echo " Executando testes..."
docker compose exec -T web pytest


TEST_EXIT_CODE=$?


echo " Finalizando ambiente..."
docker compose down


if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN} Todos os testes passaram com sucesso!${NC}"
    exit 0
else
    echo -e "${RED} Falha nos testes.${NC}"
    exit 1
fi