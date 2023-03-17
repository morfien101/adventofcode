#!/usr/bin/env bash

venv="d20-venv"
activate_path="./${venv}/bin/activate"

if [ -f "$activate_path" ]; then
    echo "Virtual environment already exists"
    source "$activate_path"
else
    echo "Creating virtual environment"
    python -m venv ${venv}
    source "$activate_path"
fi

pip install -r requirements.txt
