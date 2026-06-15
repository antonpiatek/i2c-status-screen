#!/bin/bash
cd "$(dirname "$0")"
. .venv/bin/activate
python monitor.py
