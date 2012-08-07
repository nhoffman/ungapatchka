#!/bin/bash

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "usage: dev/setup.sh projectname scriptname"
    exit
fi

find . -name "*.py" -or -name kapow | xargs sed -i "s/pypackage/$1/g;s/pypack/$2/g"
mv pypackage $1
mv pypack $2
