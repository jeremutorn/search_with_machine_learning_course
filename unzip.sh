#!/bin/bash

for s in "$@" ; do
	d="${s%.gz}"
	if [ "$s" == "$d" ] ; then
		echo "Skipping ${s} (does not end in .gz)."
		continue
	fi
	if [ -e "$d" ] ; then
		echo "Skipping ${s} (already unzipped)."
		continue
	fi
	echo "Unzipping ${s} -> ${d} ..."
	gunzip -c -- "$s" >"$d" || {
		ret="$?"
		echo 'Unzip failed.'
		rm -f -- "$d"
		exit "$ret"
	}
done
