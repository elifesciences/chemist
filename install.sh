#!/bin/bash
set -e

if [ ! -d venv ]; then
    virtualenv --python=`which python2` venv
fi
source venv/bin/activate
pip install -r requirements.txt
