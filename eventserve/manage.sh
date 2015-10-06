#!/bin/bash

APP_ROOT=$HOME/tweetmap/eventserve
VENV=${APP_ROOT}/vpython

function usage() {
    cat <<USAGE
Usage: ./manage.sh <command>
Commands:
    build - creates the virtual environment
    run - runs this app
USAGE
}

if [ -z "$1" ]; then
    usage
    exit 1
fi

cd $APP_ROOT || exit 1

case $1 in
    build)
        if [ -e $VENV ];  then
            rm -rf $VENV
        fi
        virtualenv $VENV
        source vpython/bin/activate
        pip install pip==7.1.2
        pip install -r requirements.txt
        ;;
    test)
        source $VENV/bin/activate
        PYTHONPATH="." exec python -m unittest discover
        ;;
    run)
        source $VENV/bin/activate
        PYTHONPATH="." exec python eventserve/app.py
        ;;
    *)
        usage
        exit 1
esac


