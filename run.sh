#!/bin/bash

export PYTHONPATH=$PWD/project/
echo python path is: 
echo $PYTHONPATH

echo "Launching program"
#echo $@
python3 "$@"
