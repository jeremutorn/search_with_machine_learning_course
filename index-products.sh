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
		INDEX_NAME='bbuy_products'
		MAPPING="${BASE}/opensearch/bbuy_products.json"
		LOGSTASH="${BASE}/logstash/index-bbuy.logstash"
		DATADIR='products_data'
		;;
	('week2')
		INDEX_NAME='bbuy_products'
		MAPPING="${BASE}/${WEEK}/conf/bbuy_products.json"
		LOGSTASH="${BASE}/logstash/index-bbuy.logstash"
		DATADIR='products_data'
		;;
	('week3')
		# This week works off a smaller product set, and does extra
		# processing on them.
		INDEX_NAME='bbuy_annotations'
		MAPPING="${BASE}/${WEEK}/conf/bbuy_annotations.json"
		LOGSTASH="${BASE}/${WEEK}/conf/index-bbuy-http-filter.logstash"
		DATADIR='products_annotations_data'
		;;
	('week4')
		INDEX_NAME='bbuy_products'
		MAPPING="${BASE}/${WEEK}/conf/bbuy_products.json"
		LOGSTASH="${BASE}/logstash/index-bbuy.logstash"
		DATADIR='products_data'
		;;
	(*)
		echo 'Unknown argument.'
		echo
		usage
		;;
esac

exec "${DIR}index-single.sh" \
	"$INDEX_NAME" \
	"$MAPPING" \
	"$LOGSTASH" \
	"$DATADIR"
