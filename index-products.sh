#!/bin/bash

# Call index-single.sh with arguments appropriate for indexing the Best Buy
# products data.

DIR="${0%/*}"
if [ "$DIR" == "$0" ] ; then
	DIR=''
else
	DIR="${DIR}/"
fi
BASE='/workspace/search_with_machine_learning_course'
exec "${DIR}index-single.sh" \
	'bbuy_products' \
	"${BASE}/opensearch/bbuy_products.json" \
	"${BASE}/logstash/index-bbuy.logstash" \
	'products_data'
