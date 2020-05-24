#!/usr/bin/env bash

set -e

REPO_BASE_DIR=$(dirname $(dirname $(realpath -s $0)))
cd $REPO_BASE_DIR

docker-compose down -v --remove-orphans
docker-compose build
docker-compose up -d
docker-compose exec backend pytest /app/tests "$@"
