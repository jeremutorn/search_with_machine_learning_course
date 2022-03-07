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
general.add_argument('--input_train', default='/workspace/datasets/fasttext/train.fasttext', help='The input file from which to read the training data')
general.add_argument('--input_test', default='/workspace/datasets/fasttext/test.fasttext', help='The input file from which to read the test data')
general.add_argument('--output', default='/workspace/datasets/fasttext/model.fasttext',  help='The output base file to which to write model data')

args = parser.parse_args()

print('Training with data from {i:s} ...'.format(i=args.input_train))
model = fasttext.train_supervised(input=args.input_train, lr=1.0, epoch=25, wordNgrams=2)

print('Testing with data from {i:s} ...'.format(i=args.input_test))
(N, precision, recall) = model.test(args.input_test)
print('N   :  {N:d}'   .format(N=N))
print('prec:  {p:0.4f}'.format(p=precision))
print('rec :  {r:0.4f}'.format(r=recall))

print('Saving model to {o:s} ...'.format(o=args.output))
model.save_model(args.output)
