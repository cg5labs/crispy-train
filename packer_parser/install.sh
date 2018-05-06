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

# check if virtualenv profile is avaialable
if [[ -f .env ]]; then
  . .env
else
  echo "==> ERROR! Can't activate Python VirtualEnv for ${PROJECT}!"
  exit 1
fi

# check if pip requirements.txt is available, then pip install the modules
if [[ -f requirements.txt ]]; then 
  pip install -r requirements.txt
  RC=$?
else
  echo "==> ERROR! Missing requirements.txt in Python VirtualEnv for ${PROJECT}!"
  exit 2
fi

exit ${RC}
