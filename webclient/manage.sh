#!/bin/bash

APP_ROOT=/home/ubuntu/tweetmap/webclient
VENV=${APP_ROOT}/vpython

function usage() {
    cat <<USAGE
Usage: ./manage.sh <command>
Commands:
    build - builds this app
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
        rm -rf dist
        cp -a app dist
    run)
        echo "Served directly from dist through nginx"
        ;;
    *)
        usage
        exit 1
esac


