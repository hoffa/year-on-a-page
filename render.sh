#!/bin/sh
set -eux

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py --year 2024 > 2024.svg
.venv/bin/python main.py --year 2025 > 2025.svg
