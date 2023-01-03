#!/bin/sh

FULLPATH=$(dirname "$0")

echo "Program path is: $FULLPATH"
echo "Starting Relays Program"

VENV_DIR=$FULLPATH/venv


if [[ -d "$VENV_DIR" ]];
then
    echo "Virtual Environment exists."
    source $VENV_DIR/bin/activate
else
    echo "Virtual Environment not exists :c."
    echo "Configuring the virtual environment."
    python3 -m venv $FULLPATH/venv
    source $VENV_DIR/bin/activate
    echo "Installing dependencies."
    pip3 install -r $FULLPATH/requirements.txt
fi

echo "Executing the program"
python3 $FULLPATH/main.py