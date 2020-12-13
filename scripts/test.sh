#!/usr/bin/env bash

set -e

REPO_BASE_DIR=$(dirname $(dirname $(realpath -s $0)))
cd $REPO_BASE_DIR

docker-compose down --remove-orphans
docker-compose up --detach --build
docker-compose rm --stop --force -v backend
docker-compose run --name=backend backend pytest "$@"
