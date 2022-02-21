#!/bin/bash

# On the command line, give the directory name of the flask app to run.
# Should be week1, week2, week3, or week4.
# This will then attempt to run flask as described in the README.

DIR="$1"
if [ -z "$DIR" -o ! -d "$DIR" ] ; then
	echo 'Need a flask app directory.'
	exit 2
fi

FLASK_ENV=development FLASK_APP="$DIR" \
PRIOR_CLICKS_LOC=/workspace/ltr_output/train.csv \
exec python3.9 -m flask run --port 3000
