#!/bin/bash

# Call index-single.sh with arguments appropriate for indexing the Best Buy
# products data.

function usage() {
	echo "Usage: ${0##*/} <weekN>"
	echo 'Need the week number to know where to get the configuration files.'
	echo 'Examples:  week1, week2, week3, or week4.'
	exit 2
}
WEEK="$1" ; shift

DIR="${0%/*}"
if [ "$DIR" == "$0" ] ; then
	DIR=''
else
	DIR="${DIR}/"
fi
BASE='/workspace/search_with_machine_learning_course'

case "$WEEK" in
	('week1')
		MAPPING="${BASE}/opensearch/bbuy_products.json"
		;;
	('week2')
		MAPPING="${BASE}/${WEEK}/conf/bbuy_products.json"
		;;
	('week3')
		MAPPING="${BASE}/${WEEK}/conf/bbuy_products.json"
		;;
	('week4')
		MAPPING="${BASE}/${WEEK}/conf/bbuy_products.json"
		;;
	(*)
		echo 'Unknown argument.'
		echo
		usage
		;;
esac

exec "${DIR}index-single.sh" \
	'bbuy_products' \
	"$MAPPING" \
	"${BASE}/logstash/index-bbuy.logstash" \
	'products_data'
