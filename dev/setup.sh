#!/bin/bash

if [[ -z $1 ]] || [[ -z $2 ]]; then
    echo "usage: dev/setup.sh projectname scriptname"
    exit
fi

python dev/insteadofsed.py ungapatchka $1 \
    $(find . -name "*.py" -or -name kapow)

python dev/insteadofsed.py kapow $2 \
    $(find . -name "*.py" -or -name kapow)

mv ungapatchka $1
mv kapow $2

# set up new git repo
rm -rf .git
git init . && git add . && git commit -m "first commit"

# reset version
python setup.py -h > /dev/null

