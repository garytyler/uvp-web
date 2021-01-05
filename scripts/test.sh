#! /usr/bin/env bash

docker-compose down --volumes --remove-orphans
docker-compose up --detach --build
docker-compose exec backend poetry run pytest --cov=app tests/unit
docker-compose exec frontend npm run coverage:unit
docker-compose exec frontend npm run coverage:e2e
