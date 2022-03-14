#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Script to read the output of create_labeled_queries.py, sample it, and
write training and test data to output files.
'''

import argparse
import random

parser = argparse.ArgumentParser(description='Set up test and train data')
general = parser.add_argument_group('general')
general.add_argument('--input', default='/workspace/datasets/labeled_query_data.txt',  help='The input file with the lines from which to select training and test data')
general.add_argument('--output_train', default='/workspace/datasets/labeled_query_data.fasttext.train', help='The output file to which to write the selected training data')
general.add_argument('--output_test', default='/workspace/datasets/labeled_query_data.fasttext.test', help='The output file to which to write the selected test data')
general.add_argument('--train_size', default=65536, type=int, help='The number of lines of training data to select')
general.add_argument('--test_size', default=65536, type=int, help='The number of lines of test data to select')

args = parser.parse_args()

print('Reading input from {i:s} ...'.format(i=args.input))
inputData = list()
with open(args.input, 'r') as handle:
    for line in handle:
        inputData.append(line)
print('Read {l:d} records.'.format(l=len(inputData)))

selectCount = args.train_size + args.test_size
if (selectCount > len(inputData)):
    raise ValueError('Cannot select {s:d} records from {l:d}'.format(
                     s=selectCount, l=len(inputData)))
print('Selecting {s:d} records ...'.format(s=selectCount))
selectedData = random.sample(inputData, selectCount)
if (len(selectedData) != selectCount):
    raise Exception('Internal error:  Selected data size ({l:d}) does not match selectCount ({s:d})'.format(
                    l=len(selectedData), s=selectCount))
trainData = selectedData[:args.train_size]
testData  = selectedData[args.train_size:]

print('Writing train data to {o:s} ({l:d} lines) ...'.format(
      o=args.output_train, l=len(trainData)))
with open(args.output_train, 'w') as handle:
    handle.write(''.join(trainData))

print('Writing test data to {o:s} ({l:d} lines) ...'.format(
      o=args.output_test, l=len(testData)))
with open(args.output_test, 'w') as handle:
    handle.write(''.join(testData))
