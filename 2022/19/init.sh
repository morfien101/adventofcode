#!/usr/bin/env bash

activate_path="./d19-venv/bin/activate"

if [ -f "$activate_path" ]; then
    echo "Virtual environment already exists"
    source "$activate_path"
else
    echo "Creating virtual environment"
    python -m venv d19-venv
    source "$activate_path"
fi

pip install -r requirements.txt
