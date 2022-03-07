#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Script to read the output of extractTitles.py and use it to train and save a
skipgram fasttext model.
'''

import argparse

import fasttext

parser = argparse.ArgumentParser(description='Generate a model from extracted title data')
general = parser.add_argument_group('general')
general.add_argument('--input', default='/workspace/datasets/fasttext/titles.txt', help='The input file from which to read the extracted titles')
general.add_argument('--output', default='/workspace/datasets/fasttext/model.titles.fasttext',  help='The output base file to which to write model data')
general.add_argument('--min_count', default=-1, type=int, help='Only use words with at least the given number of occurrences in the data')

args = parser.parse_args()

print('Generating model from {i:s} ...'.format(i=args.input))
fasttextArgs = dict()
if (0 <= args.min_count):
    fasttextArgs['minCount'] = args.min_count
model = fasttext.train_unsupervised(model='skipgram',
                                    input=args.input,
                                    **fasttextArgs)

print('Saving model to {o:s} ...'.format(o=args.output))
model.save_model(args.output)
