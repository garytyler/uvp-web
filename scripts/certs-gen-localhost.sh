#! /usr/bin/env bash

set -e

if [ ! $(command -v mkcert) ]; then
    echo "$(basename $0): Aborting. mkcert command not found."
    exit $?
fi

SCRIPTS_DIR=$(dirname $(realpath -s $0))
PROJECT_DIR=$(dirname $SCRIPTS_DIR)
SELFSIGNED_DIR=$PROJECT_DIR/traefik/self-signed

rm -rf "$SELFSIGNED_DIR"
mkdir --parents "$SELFSIGNED_DIR"

mkcert \
    --cert-file "$SELFSIGNED_DIR/localhost-cert.pem" \
    --key-file "$SELFSIGNED_DIR/localhost-key.pem" \
    "localhost" \
    "traefik.localhost" \
    "pgadmin.localhost"
