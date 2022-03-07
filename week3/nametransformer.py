# -*- coding: utf-8 -*-

import nltk.stem

class NameTransformer(object):
    '''
    Quick class to provide a method for transforming product names.
    '''

    def transform(self, name):
        '''
        Transforms a name, converting to lowercase, removing punctuation,
        setmming, and so on.
        '''
        lowerCase = name.lower()
        unknownCharactersRemoved = \
            ''.join(map(lambda c: c if (c in self._allowedCharacters) else ' ',
            lowerCase))
        stemmed = ' '.join(self._stemmer.stem(word) \
                           for word in unknownCharactersRemoved.split())
        return stemmed
    # End of transform().

    _stemmer = nltk.stem.SnowballStemmer('english')
    '''
    The stemmer to use for transforming.
    '''

    _allowedCharacters = set()
    '''
    Characters not in this set will be removed.
    '''
    _allowedCharacters.update(chr(o) for o in range(ord('0'), ord('9') + 1))
    _allowedCharacters.update(chr(o) for o in range(ord('A'), ord('Z') + 1))
    _allowedCharacters.update(chr(o) for o in range(ord('a'), ord('z') + 1))
    _allowedCharacters.update(('-', '_', '"', "'", '$', '%'))
# End of NameTransformer class.
