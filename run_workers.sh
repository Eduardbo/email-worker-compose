#!/bin/sh

# Script helper para subir e escalar workers
cd "$(dirname "$0")"

# Build e sobe todos os serviços
docker compose up -d --build

# Escala workers para 3 instâncias
docker compose up -d --scale workers=3

# Segue logs dos workers com timestamps
docker compose logs -f -t workers
