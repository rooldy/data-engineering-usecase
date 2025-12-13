#!/bin/bash

echo "Reset complet"

cd docker || exit 1
docker-compose down -v
