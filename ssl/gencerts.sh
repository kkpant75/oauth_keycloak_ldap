#!/bin/bash
set -e

mkdir -p certs

if [ ! -f "certs/cert.pem" ]; then
    echo "Generating self-signed certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
else
    echo "Certificates already exist."
fi
