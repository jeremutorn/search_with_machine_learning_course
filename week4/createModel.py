#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Script to read the output of createTrainTestData.py and use it to train,
test, and save a supervised fasttext model.
'''

import argparse

import fasttext

parser = argparse.ArgumentParser(description='Generate and test a model from training/test data')
general = parser.add_argument_group('general')
general.add_argument('--input_train', default='/workspace/datasets/labeled_query_data.fasttext.train', help='The input file from which to read the training data')
general.add_argument('--input_test', default='/workspace/datasets/labeled_query_data.fasttext.test', help='The input file from which to read the test data')
general.add_argument('--output', default='/workspace/datasets/labeled_query_data.fasttext.model',  help='The output base file to which to write model data')

args = parser.parse_args()

print('Training with data from {i:s} ...'.format(i=args.input_train))
# Adding lr=1.0 tended to make the results worse.
# Adding epoch=25 tended to make the results worse.
# Bigrams (wordNgrams=2) did not seem to make a lot of difference, but
# maybe was an improvement.
# Removing both lr=1.0 and epoch=25 was not as good as either lr=1.0 or
# epoch=25 alone, so settled on something a little closer to the default
# values, but not quite.
model = fasttext.train_supervised(input=args.input_train, lr=0.25, epoch=16, wordNgrams=2)

# Run tests for fetching a few different number of results.
print('Testing with data from {i:s} ...'.format(i=args.input_test))
for k in (1, 3, 5):
    print('  Running test with fetching {k:d} results ...'.format(k=k))
    (N, precision, recall) = model.test(args.input_test, k=k)
    print('    N   @{k:d}:  {N:d}'   .format(N=N        , k=k))
    print('    prec@{k:d}:  {p:0.4f}'.format(p=precision, k=k))
    print('    rec @{k:d}:  {r:0.4f}'.format(r=recall   , k=k))

print('Saving model to {o:s} ...'.format(o=args.output))
model.save_model(args.output)
