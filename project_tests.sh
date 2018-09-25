#!/bin/bash
set -e

source venv/bin/activate
ln -s example-app.cfg app.cfg
python -m unittest test_chemist
