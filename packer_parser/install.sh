#!/usr/bin/env bash
PROJECT=$(dirname $0)

if [[ -f .env ]]; then
  . .env
else
    echo "==> ERROR! Can't activate Python VirtualEnv for ${PROJECT}!"
    exit 1
fi

pip install -r requirements.txt
