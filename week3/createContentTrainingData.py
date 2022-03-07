import argparse
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path

from collections import defaultdict
from collections import namedtuple

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

# Directory for product data
directory = r'/workspace/search_with_machine_learning_course/data/pruned_products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")

# Consuming all of the product data will take over an hour! But we still want to be able to obtain a representative sample.
general.add_argument("--sample_rate", default=1.0, type=float, help="The rate at which to sample input (default is 1.0)")

general.add_argument("--min_products", default=0, type=int, help="The minimum number of products per category (default is 0).")

general.add_argument("--max_catdepth", default=-1, type=int, help="The maximum category depth that will be used as a category (the default, -1, means always use maximum depth)")

args = parser.parse_args()
output_file = args.output
path = Path(output_file)
output_dir = path.parent
if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

if args.input:
    directory = args.input
min_products = args.min_products
sample_rate = args.sample_rate

nameTransformer = NameTransformer()
catMap = defaultdict(list)
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        print("Processing %s" % filename)
        f = os.path.join(directory, filename)
        tree = ET.parse(f)
        root = tree.getroot()
        for child in root:
            if random.random() > sample_rate:
                continue
            # Check to make sure category name is valid
            name = child.find('name')
            if (name is None or name.text is None):
                continue
            name = name.text
            catPath = child.find('categoryPath')
            if (catPath is None or 0 >= len(catPath)):
                continue
            catDepth = min(len(catPath) - 1, args.max_catdepth)
            category = catPath[catDepth]
            # category should be an iterable of category names; select the
            # first, which seems to be the more programmatic descriptor;
            # subsequent ones are more natural-language oriented.
            if (0 >= len(category)):
                continue
            category = category[0]
            if (category is None or category.text is None):
                continue
            category = category.text

            # Replace newline chars with spaces so fastText doesn't complain
            name = name.replace('\n', ' ')
            # Just in case there are spaces.
            category.replace(' ', '_')
            catMap[category].append(name)

print("Writing results to %s" % output_file)
with open(output_file, 'w') as output:
    for (cat, nameList) in sorted(catMap.items()):
        if (len(nameList) < args.min_products):
            continue
        for name in nameList:
            output.write("__label__%s %s\n" % (cat, name))
