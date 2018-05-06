#!/usr/bin/env bash

# Python virtualenv setup

PROJECT=$(dirname $0)
VENV_BIN=$(which virtualenv)

# check if virtualenv is available
if [[ $VENV_BIN != "" ]]; then
    echo "DEBUG: virtualenv found: ${VENV_BIN}"
    virtualenv venv
else
    pip install virtualenv
fi

#exit 0

# check if virtualenv profile is avaialable
if [[ -f .env ]]; then
  . .env
else
    echo "==> ERROR! Can't activate Python VirtualEnv for ${PROJECT}!"
    exit 1
fi

pip install -r requirements.txt
