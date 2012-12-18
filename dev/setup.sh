#!/bin/bash

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "usage: dev/setup.sh projectname scriptname"
    exit
fi

if [[ $1 == $2 ]]; then
    echo "Projectame and scriptname must be different."
    exit
fi

./kapow repl -r ungapatchka:$1 -r kapow:$2 \
    $(find . -name "*.py" -or -name kapow)

mv ungapatchka $1
mv kapow $2

# set up new git repo
rm -rf .git
git init . && git add . && git commit -m "first commit"

# reset version
python setup.py -h > /dev/null

