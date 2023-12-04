#!/bin/bash

python_var='python3'


if [ -d .env ]; then
    source .env/bin/activate
fi

$python_var main.py
