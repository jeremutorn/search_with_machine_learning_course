#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Provides a quick inverted index to see what, if any, words appear to link
``linux'' and ``proteins'' in wiki_sample.txt.
'''

import sys

from collections import namedtuple
from collections import defaultdict

class TokenFreq(namedtuple('Token', ('freq', 'token'))):
    '''
    Frequency and token pair.
    '''
    # Cleaner to just write:
    #   TokenFreq = namedtuple(...)
    # but this way associates a docstring with the class.
    pass
# End of TokenFreq class.

class TokenizedDocument(namedtuple('TokenizedDocument', ('tokenFreqs', 'doc'))):
    '''
    A structure combining a document (as a string) and a tuple of
    TokenFreqs.
    '''
    # Cleaner to just write:
    #   TokenizedDocument = namedtuple(...)
    # but this way associates a docstring with the class.
    pass
# End of TokenizedDocument class.

class DocFreq(namedtuple('DocFreq', ('tokenFreq', 'ID', 'tokenizedDoc'))):
    '''
    A structure combining a TokenizedDocument, along with a TokenFreq
    instance giving a normalized token and the frequency of that token in
    the document.  Also stores a document ID.
    '''
    # Cleaner to just write:
    #   DocFreq = namedtuple(...)
    # but this way associates a docstring with the class.
    pass
# End of DocFreq class.

class TokenizedIndex(object):
    '''
    Class that stores a collection of TokenizedDocuments, and provides
    indexing to them based on ID and tokens.
    '''

    def __init__(self):
        '''
        Initializes an empty index.
        '''
        self._docList       = list()
        self._invertedIndex = defaultdict(list)
    # End of __init__().

    def __len__(self):
        '''
        Returns the number of documents this has stored.
        '''
        return len(self._docList)
    # End of __len__().

    @staticmethod
    def normalize(token):
        '''
        Returns a normalized version of a token.
        '''
        return token.lower()
    # End of normalize().

    def genTokenizedDoc(self, doc):
        '''
        Given a document (as a string), this forms a tuple of TokenFreqs
        and returns a TokenizedDocument.  The TokenFreqs will be sorted in
        reverse order (highest frequency first).
        '''
        tokenDict = defaultdict(lambda: 0)
        for token in doc.split():
            tokenDict[self.normalize(token)] += 1
        tokenFreqs = tuple(TokenFreq(freq, token) for (token, freq) \
                           in sorted(tokenDict.items()))
        return TokenizedDocument(tokenFreqs, doc)
    # End of genTokenizedDoc().

    def add(self, doc):
        '''
        Given a document as a string, this tokenizes it and stores it in
        the index.  Returns the ID of the document.
        '''
        tokenizedDoc = self.genTokenizedDoc(doc)
        docID = len(self._docList)
        self._docList.append(tokenizedDoc)
        for tokenFreq in tokenizedDoc.tokenFreqs:
            self._invertedIndex[tokenFreq.token].append(
                DocFreq(tokenFreq.freq, docID, tokenizedDoc))
        return docID
    # End of add().

    def finalize(self):
        '''
        Sorts all of the results that may be returned by getDocsByToken()
        by decreasing frequency.  Intended to be used once all of the
        documents have been added.
        '''
        for docFreqList in self._invertedIndex.values():
            docFreqList.sort(reverse=True)
    # End of finalize().

    def getDocByID(self, docID):
        '''
        Returns the TokenizedDocument associated with the given ID.  Raises
        IndexError if docID is invalid.
        '''
        # Let this raise IndexError if appropriate.
        return self._docList[docID]
    # End of getDocByID().

    def getDocsByToken(self, token):
        '''
        Returns a tuple of DocFreq instances associated with the given
        token.  Returns an empty tuple if there are no matches.
        '''
        ret = self._invertedIndex.get(self.normalize(token), None)
        if (ret is None):
            # Only generate the empty tuple if no match was found.
            return tuple()
        return tuple(ret)
    # End of getDocsByToken().

    _docList = None
    '''
    A list of TokenizedDocuments.  The ID of a document is its index in
    this list.
    '''

    _invertedIndex = None
    '''
    A dictionary mapping normalized tokens to lists of documents containing
    the tokens, as DocFreq instances.
    '''
# End of InvertedIndex class.

if ('__main__' == __name__):
    index = TokenizedIndex()
    print('Reading documents from stdin ...')
    for line in sys.stdin:
        index.add(line.strip())
    index.finalize()
    print('Read {l:d} documents.'.format(l=len(index)))

    # Collect the documents with the desired terms.
    topN = 5
    docFreqsDict = dict()
    for token in ('linux', 'proteins'):
        docFreqs            = index.getDocsByToken(token)
        docFreqsDict[token] = docFreqs
        print('Here are the top {N:d} documents for {t:s}:'.format(
              N=topN, t=token))
        for ind in range(0, min(topN, len(docFreqs))):
            docFreq = docFreqs[ind]
            print('ID: {ID:d}  Freq: {freq:d}  doc: {d:s}'.format(
                  ID=docFreq.ID, freq=docFreq.tokenFreq, d=docFreq.tokenizedDoc.doc))

    # Look at documents that contained all the desired terms.
    firstN = 5
    IDSet = None
    for (token, docFreqs) in docFreqsDict.items():
        idSet = set(docFreq.ID for docFreq in docFreqs)
        if (IDSet is None):
            IDSet = idSet
        else:
            IDSet = IDSet.intersection(idSet)
    if (IDSet is None or 0 >= len(IDSet)):
        print('No documents contained all terms.')
    else:
        IDs = list(IDSet)
        IDs.sort()
        print('Here are the first {N:d} documents for all terms:'.format(N=firstN))
        for ind in range(0, min(topN, len(IDs))):
            print('ID: {ID:d}  Freq: {freq:d}  doc: {d:s}'.format(
                  ID=docFreqs.ID, freq=docFreqs.freq, d=docFreqs.doc))

    # Look at all tokens that are commonly related with all the desired
    # terms.
    # For each term, create a dictionary mapping tokens to the number of
    # times they appear in documents with the term, scaled to the number of
    # documents that contained the term.  Keep the scores for all the terms
    # in a single list associated with the related token.
    sortedTokens     = tuple(sorted(docFreqsDict.keys()))
    relatedTokenDict = defaultdict(lambda: [0] * len(sortedTokens))
    for (ind, token) in enumerate(sortedTokens):
        for docFreq in docFreqsDict[token]:
            for tokenFreq in docFreq.tokenizedDoc.tokenFreqs:
                relatedTokenDict[tokenFreq.token][ind] += 1 / len(docFreqs)
    # Collect the scores into tuples, and sort by the minimum score.
    scoredTokens = list((min(scores), token, tuple(scores))
                        for (token, scores) in relatedTokenDict.items())
    scoredTokens.sort(reverse=True)

    # Show the most related tokens.
    # Pick a larger selection, as the most commonly related terms are
    # things like the, of, and, a, for, etc.
    topN = 32
    print('Here are the top {N:d} related tokens for all terms:'.format(
          N=topN))
    for ind in range(0, min(topN, len(scoredTokens))):
        (minScore, token, scores) = scoredTokens[ind]
        print('{tok:s}:  score: {s:s}'.format(
              tok=token, s=str(scores)))
