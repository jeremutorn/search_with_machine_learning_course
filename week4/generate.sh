#!/bin/bash

# Generates all of the models that will be used for week 4 of the
# coursework.

INPUT_QUERIES='/workspace/datasets/train.csv'
INPUT_CATEGORIES='/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'
OUTPUT='/workspace/datasets/query_training'
QUERY_CATEGORIES="${OUTPUT}/query_categories.csv"
QUERY_TRAIN="${OUTPUT}/query_categories.train.csv"
QUERY_TEST="${OUTPUT}/query_categories.test.csv"
QUERY_MODEL="${OUTPUT}/query_categories.fasttext.model"

rm -rf -- "$OUTPUT" || {
	ret="$?"
	echo "Unable to remove ${OUTPUT}."
	exit "$ret"
}

mkdir -p -- "$OUTPUT" || {
	ret="$?"
	echo "Unable to create ${OUTPUT}."
	exit "$ret"
}

python create_labeled_queries.py \
	--input        "$INPUT_QUERIES" \
	--categories   "$INPUT_CATEGORIES" \
	--output       "$QUERY_CATEGORIES" \
	--min_queries  128 \
|| {
	ret="$?"
	echo 'Error creating query/category mappings.'
	exit "$?"
}
