#!/bin/bash

CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -d 'venv' ] ; then
    source $CURRENT_SCRIPT_DIR/venv/bin/activate
    cd $CURRENT_SCRIPT_DIR

    export PYTHONPATH=$(pwd)
    export DJANGO_SETTINGS_MODULE='matprazdnik.settings'

    if [ -z '$1' ] ; then
        echo 'Usage: update_db.sh [REGISTRATION_DB.csv|SCHOOL_LIST.csv] [-participants|-schools]'
    else
        python3 populate_db_scripts/update_db.py $1 $2
    fi
else
    echo "$0: No venv found.  Check README.md for setup instructions"
fi
