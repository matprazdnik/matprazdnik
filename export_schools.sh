#!/bin/bash

CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -d 'venv' ] ; then
    source $CURRENT_SCRIPT_DIR/venv/bin/activate
    cd $CURRENT_SCRIPT_DIR

    export PYTHONPATH=$(pwd)
    export DJANGO_SETTINGS_MODULE='matprazdnik.settings'

    if [ -z '$1' ] ; then
        echo 'Usage: export_schools.sh PATH_TO_NEW_FILE'
    else
        python3 populate_db_scripts/extract_schools.py $1
    fi
else
    echo "$0: No venv found.  Check README.md for setup instructions"
fi
