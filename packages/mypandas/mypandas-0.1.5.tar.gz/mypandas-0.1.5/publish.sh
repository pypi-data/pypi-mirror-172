#!/usr/bin/env bash
set -eou pipefail

rm -rf dist
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
deactivate
rm -rf venv
