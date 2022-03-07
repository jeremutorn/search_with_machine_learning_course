#!/bin/bash

INPUT="$1"  ; shift
OUTPUT="$1" ; shift
if [ -z "$INPUT" -o -z "$OUTPUT" ] ; then
	echo 'Need INPUT and OUTPUT.'
	exit 1
fi
exec fasttext supervised -input "$INPUT" -output "$OUTPUT" -epoch 25
