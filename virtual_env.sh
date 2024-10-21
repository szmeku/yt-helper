#!/bin/bash

# to run it in current shell (to activate venv effectively)
# run `. virtual_env.sh`

if [ ! -d "venv" ]; then

    echo "venv doesn't exist, creating and activating"

    virtualenv --python=python3 venv

    source venv/bin/activate

    pip install -r requirements.txt
else

    echo "venv exists, just activating "
    source venv/bin/activate
fi
