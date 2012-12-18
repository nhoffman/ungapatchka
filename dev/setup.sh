#!/bin/bash

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "usage: dev/setup.sh projectname scriptname"
    exit
fi

for fn in $(find . -name "*.py" -or -name kapow); do
    sed -i -e "s/ungapatchka/$1/g" $fn
    sed -i -e "s/kapow/$2/g" $fn
done

mv ungapatchka $1
mv kapow $2

# set up new git repo
rm -rf .git
git init . && git add . && git commit -m "first commit"

# reset version
python setup.py -h > /dev/null

