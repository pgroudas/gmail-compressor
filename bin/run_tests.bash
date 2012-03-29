#!/bin/bash

basedir="`dirname $0`/.."

pushd "$basedir" > /dev/null 2>&1

export PYTHONPATH="$basedir:$PYTHONPATH"

command -v nosetests >/dev/null 2>&1 || { echo >&2 "I require nosetests to run.  Install it with 'easy_install nose' or 'pip install nose'.  Aborting."; exit 1; }

/usr/bin/env nosetests tests

popd > /dev/null 2>&1
