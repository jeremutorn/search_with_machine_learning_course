# -*- coding: utf-8 -*-

import nltk.stem

class Normalizer(object):
    '''
    Quick class to provide a method for normalizing strings.
    '''

    def __init__(self, stemmer=None, allowedCharacters=None):
        '''
        Initializes the normalizer.
        stemmer, if provided, should be a Stemmer than will be used to
        override the default stemmer.
        allowedCharacters, if provided, should be a set of characters that
        will be kept (all other characters will be replaced with spaces).
        '''
        if (stemmer is not None):
            self._stemmer = stemmer
        if (allowedCharacters is not None):
            self._allowedCharacters = allowedCharacters
    # End of __init__().

    def normalize(self, s):
        '''
        Transforms s, converting to lowercase, removing punctuation,
        stemming, and so on.
        '''
        lowerCase = s.lower()
        unknownCharactersRemoved = \
            ''.join(map(lambda c: c if (c in self._allowedCharacters) else ' ',
            lowerCase))
        stemmed = ' '.join(self._stemmer.stem(word) \
                           for word in unknownCharactersRemoved.split())
        return stemmed
    # End of normalize().

    _stemmer = nltk.stem.SnowballStemmer('english')
    '''
    The stemmer to use for normalizing.
    '''

    _allowedCharacters = set()
    '''
    Characters not in this set will be removed.
    '''
    _allowedCharacters.update(chr(o) for o in range(ord('0'), ord('9') + 1))
    _allowedCharacters.update(chr(o) for o in range(ord('A'), ord('Z') + 1))
    _allowedCharacters.update(chr(o) for o in range(ord('a'), ord('z') + 1))
# End of Normalizer class.
