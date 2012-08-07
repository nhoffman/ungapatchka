#!/bin/bash

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "usage: dev/setup.sh projectname scriptname"
    exit
fi

mv pypackage $1
mv pypack $2
find . -name "*.py" | xargs sed "s/pypackage/$1/g;s/pypack/$2/g"
