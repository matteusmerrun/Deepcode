#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

if [ -f "venv/bin/python" ]; then
    ./venv/bin/python main.py "$@"
elif [ -f ".venv/bin/python" ]; then
    ./.venv/bin/python main.py "$@"
else
    python3 main.py "$@"
fi
