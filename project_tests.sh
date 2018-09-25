#!/bin/bash
set -e

source venv/bin/activate
python -m unittest test_chemist
