#!/bin/bash

# Call index-single.sh with arguments appropriate for indexing the Best Buy
# queries data.

DIR="${0%/*}"
if [ "$DIR" != "$0" ] ; then
	DIR="${DIR}/"
else
	DIR=''
fi
BASE='/workspace/search_with_machine_learning_course'
exec "${DIR}index-single.sh" \
	'bbuy_queries' \
	"${BASE}/opensearch/bbuy_queries.json" \
	"${BASE}/logstash/index-bbuy-queries.logstash" \
	'query_data'
