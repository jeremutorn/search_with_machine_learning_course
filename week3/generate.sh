#!/bin/bash

# Generates all of the models that will be used for part 3 of the coursework.

INPUT='./phone_products'
OUTPUT='/workspace/datasets/fasttext'
PRODUCT_CAT="${OUTPUT}/product_category_data.fasttext"
PRODUCT_TRAIN="${OUTPUT}/product_category_data.train.fasttext"
PRODUCT_TEST="${OUTPUT}/product_category_data.test.fasttext"
PRODUCT_MODEL="${OUTPUT}/product_category_data.fasttext.model"
PRODUCT_TITLES="${OUTPUT}/product_titles.fasttext"
PRODUCT_TITLE_MODEL="${OUTPUT}/product_titles.fasttext.model"

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

python createContentTrainingData.py \
	--input        "$INPUT" \
	--output       "$PRODUCT_CAT" \
	--min_products 5 \
	--max_catdepth 4 \
|| {
	ret="$?"
	echo 'Error creating product data.'
	exit "$?"
}

python createTrainTestData.py \
	--input        "$PRODUCT_CAT" \
	--output_train "$PRODUCT_TRAIN" \
	--output_test  "$PRODUCT_TEST" \
	--train_size   3600 \
	--test_size    1200 \
|| {
	ret="$?"
	echo 'Error creating product training data.'
	exit "$?"
}

python createModel.py \
	--input_train "$PRODUCT_TRAIN" \
	--input_test  "$PRODUCT_TEST" \
	--output      "$PRODUCT_MODEL" \
|| {
	ret="$?"
	echo 'Error creating product model.'
	exit "$?"
}

python extractTitles.py \
	--input       "$INPUT" \
	--output      "$PRODUCT_TITLES" \
	--sample_rate 1.0 \
|| {
	ret="$?"
	echo 'Error extracting titles.'
	exit "$?"
}

python titleModel.py \
	--input "$PRODUCT_TITLES" \
	--output "$PRODUCT_TITLE_MODEL" \
	--min_count 10 \
|| {
	ret="$?"
	echo 'Error creating title model.'
	exit "$?"
}
