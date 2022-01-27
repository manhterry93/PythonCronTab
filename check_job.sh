#!/bin/sh
DIR="$( cd "$( dirname "$0" )" && pwd )"
echo "Script location: ${DIR}"
python3 ${DIR}/main.py check_job