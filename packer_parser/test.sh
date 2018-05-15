#!/usr/bin/env bash

# Integration test script

PROJECT=$(dirname $0)
VENV_BIN=$(which virtualenv)
BIN="${PROJECT}/parser.py"
PARAM0="--config=test/example2.yaml"
PARAM1="--package=test/box.tgz"

echo "==> ${BIN} ${PARAM0} ${PARAM1}"
eval "${BIN} ${PARAM0} ${PARAM1}"
RC=$?

echo "==> RC ${RC} from test script!"
exit ${RC}
