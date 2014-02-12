#!/bin/bash

set -x
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -d 'venv' ] ; then
    source $CURRENT_SCRIPT_DIR/venv/bin/activate
    pip install -r $CURRENT_SCRIPT_DIR/requirements.txt

    # yes "yes" | python $CURRENT_SCRIPT_DIR/manage.py collectstatic
    python3 $CURRENT_SCRIPT_DIR/manage.py syncdb
    python $CURRENT_SCRIPT_DIR/manage.py runserver
else 
    echo "$0: No venv found.  Check README.md for setup instructions"
fi

set +x
