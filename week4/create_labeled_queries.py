import os
import time
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import csv

# Useful if you want to perform stemming.
import nltk
stemmer = nltk.stem.PorterStemmer()

from collections import defaultdict

from utilities.normalizer import Normalizer
normalizer = Normalizer(stemmer=stemmer)

from utilities.category_tree import Category, CategoryTree

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/labeled_query_data.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=queries_file_name, help="The input queries file to read")
general.add_argument("--categories", default=categories_file_name, help="The categories XML file to parse to get the category tree")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
queries_file_name = args.input
categories_file_name = args.categories
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

print('Parsing category XML {n:s} ...'.format(n=categories_file_name))
tree = ET.parse(categories_file_name)
root = tree.getroot()
# Parse the category XML file into a CategoryTree.
categoryTree = CategoryTree()
for child in root:
    category = Category(ID  =child.find('id'  ).text, \
                        name=child.find('name').text)
    cat_path = [Category(ID  =cat.find('id'  ).text, \
                         name=cat.find('name').text) \
                for cat in child.find('path')]
    if (category != cat_path[-1]):
        raise Exception('ID/name does not match path')
    categoryTree.add(cat_path)
categoryDict = categoryTree.categoryDict
print('  Found {l:d} categories.'.format(l=len(categoryDict)))

# Check that parsing worked correctly by checking the root nodes and the
# nubmer of leaf nodes against what the assignment says we should have.
rootNodes = list()
leafNodes = list()
for categoryNode in categoryDict.values():
    if (categoryNode.parent is None):
        rootNodes.append(categoryNode)
    if (0 >= len(categoryNode.childrenDict)):
        leafNodes.append(categoryNode)
leafNameSet = set(node.name for node in leafNodes)
print('Found {l:d} root nodes:'.format(l=len(rootNodes)))
displayCount = 5
for categoryNode in sorted(rootNodes, key=lambda node: node.ID):
    if (0 >= displayCount):
        print('  ...')
        break
    print('  ID: {ID:s}  name: {name:s}'.format(
          ID  =categoryNode.ID,
          name=categoryNode.name))
    displayCount -= 1
print('Found {l:d} leaf nodes ({n:d} unique names):'.format(
      l=len(leafNodes), n=len(leafNameSet)))
displayCount = 2
for categoryNode in sorted(leafNodes, key=lambda node: node.ID):
    if (0 >= displayCount):
        print('  ...')
        break
    print('  ID: {ID:s}  name: {name:s}'.format(
          ID  =categoryNode.ID,
          name=categoryNode.name))
    displayCount -= 1
expectedRootNodes = ['cat00000']
if (expectedRootNodes != sorted(node.ID for node in rootNodes)):
    raise Exception('rootNodes not what was expected')
# NOTE:
# The coursework says there are 1540 leaf categories (but I now understand
# that they use ``leaf'' to mean any category, leaf or not, mentioned by a
# query; I suppose it is a leaf in the sense that it is the end of the
# category path represented by the query -- the 1540 should be reported by
# a different line below).
# I found a different number.  I checked by modifying categoryViewer.py so
# it counted the number of paths that were NOT substrings of the next path
# when unique paths were sorted.  I then found out that paths by names were
# not unique (sometimes there are multiple children categories with
# different IDs, but the same name), so I also modified categoryViewer.py
# to print out paths using IDs instead of names.  That produced the same
# number of category leaves given here:
expectedLeafNodeLength = 3889
if (expectedLeafNodeLength != len(leafNodes)):
    raise Exception('leafNodes was not the expected length')

# Order all of the category nodes by increasing depth.
# While at it, create a mapping of ID to depth.
breadthFirstNodes = sorted(rootNodes, key=lambda node: node.ID)
categoryDepth     = dict()
ind = 0
while (ind < len(breadthFirstNodes)):
    curNode = breadthFirstNodes[ind]
    parNode = curNode.parent
    if (parNode is None):
        categoryDepth[curNode.ID] = 0
    else:
        categoryDepth[curNode.ID] = categoryDepth[parNode.ID] + 1
    childrenNodes = sorted(curNode.childrenDict.values(), \
                           key=lambda node: node.ID)
    breadthFirstNodes.extend(childrenNodes)
    ind += 1
if (len(breadthFirstNodes) != len(categoryDict)):
    raise Exception('Not all categories are reachable from root nodes')

# Read the training data into pandas
print('Reading queries from {n:s} ...'.format(n=queries_file_name))
df = pd.read_csv(queries_file_name)[['category', 'query']]
print('Read {l:d} queries with {n:d} distinct categories.'.format(
      l=len(df), n=len(set(df['category']))))
df = df[df['category'].isin(categoryDict)]
print('After filtering to known categories, there are:')
# This is the line that should report the 1540 categories:
print('  {l:d} queries with {n:d} distinct categories.'.format(
      l=len(df), n=len(set(df['category']))))

# Normalize queries.
print('Normalizing queries ...')
normalizedQueryMap = {query:None for query in df['query']}
print('  Reduced down to {l:d} distinct queries.'.format(
      l=len(normalizedQueryMap)))
reportDelta = 4
nextReport  = time.time() + reportDelta
for (ind, query) in enumerate(sorted(normalizedQueryMap.keys())):
    normalizedQueryMap[query] = normalizer.normalize(query)
    if (time.time() >= nextReport):
        num = ind + 1
        den = len(normalizedQueryMap)
        print('  Current progress:  {n:d} (of {d:d}, {p:5.2f}%)'.format(
              n=num, d=den, p=100.*num/den))
        nextReport = time.time() + reportDelta
df['query'] = [normalizedQueryMap[query] for query in df['query']]

print('Assigning queries to category nodes ...')
# Start with a map of category ID to the number of queries mapped directly
# to that ID.
skipCount          = defaultdict(lambda: 0)
queryCount         = defaultdict(lambda: 0)
totalQueriesMapped = 0
for ID in df['category']:
    if (ID not in categoryDict):
        skipCount[ID] += 1
    queryCount[ID]     += 1
    totalQueriesMapped += 1
if (0 < len(skipCount)):
    print('WARNING:  Skipped {l:d} unrecognized category IDs ({n:d} queries).'.format(
          l=len(skipCount), n=sum(skipCount.values())))
if (len(df) - totalQueriesMapped != sum(skipCount.values())):
    raise Exception('INTERNAL ERROR:  Some queries are unaccounted for')
if (len(df) != totalQueriesMapped):
    raise Exception('INTERNAL ERROR:  Pre-filtering of queries missed some unmapped queries')
# In order of decreasing depth, increase the number of queries associated
# with the categories by the sum of the counts of all of the immediate
# children.  Because this is done in order of decreasing depth, this has
# already been done for all the child nodes by the time we get to the
# current node, so this will result in each category being associated with
# the number of queries associated with any category in the subtree rooted
# at that node.
for categoryNode in reversed(breadthFirstNodes):
    for child in categoryNode.childrenDict.values():
        queryCount[categoryNode.ID] += queryCount[child.ID]
# Quick check:  The root node should be associated with all the queries.
if (queryCount[rootNodes[0].ID] != totalQueriesMapped):
    raise Exception('Not all mapped queries were associated with root node')
# Create a second map of ID to category.  Each category ID should map to
# the closest ancestor with at least min_queries queries associated with
# its subtree.
# By traversing in order of increasing depth, each element may be mapped to
# either itself or a value already mapped for its parent, without needing
# to traverse up to the full depth of the node for each node.
categoryMap = dict()
for (unusedDepth, ID) in sorted((categoryDepth[ID], ID) \
                                for ID in queryCount.keys()):
    if (queryCount[ID] < min_queries):
        node = categoryDict[ID]
        parNode = node.parent
        if (parNode is None):
            raise Exception('min_queries is more than the number of queries in the tree')
        # Because categoryMap is being filled in order of increasing node
        # depth, the parent should already be mapped.
        categoryMap[ID] = categoryMap[parNode.ID]
    else:
        categoryMap[ID] = ID
# Roll up the query categories.
origQueryCategories = set(df['category'])
df['category'] = [categoryMap[category] for category in df['category']]
rolledQueryCategories = set(df['category'])
print('  Assigned {l:d} queries to {r:d} distinct categories (from {o:d}).'.format(
      l=len(df), r=len(rolledQueryCategories), o=len(origQueryCategories)))

# Here, I was trying to figure out why the course materials say there are
# 1540 leaf nodes in the category tree.  Try taking just the categories
# mentioned in queries, and see if there are 1540 leaf nodes there.
# This does not work.  As mentioned above, the 1540 is the number of
# distinct categories mentioned by the queries, before filtering to known
# categories (one of the lines above should report 1540).
print('Trying a category tree reduced to categories mentioned in queries ...')
reducedCategoryTree = CategoryTree()
for (ID, count) in queryCount.items():
    # During the accumulation procedure, all nodes were added to
    # queryCount, even the ones not referenced by queries.  Filter those
    # back out.
    if (0 >= count):
        continue
    reducedCategoryTree.add(categoryTree[ID].path)
reducedRootNodes = list()
reducedLeafNodes = list()
for categoryNode in reducedCategoryTree.categoryDict.values():
    if (categoryNode.parent is None):
        reducedRootNodes.append(categoryNode)
    if (0 >= len(categoryNode.childrenDict)):
        reducedLeafNodes.append(categoryNode)
print('  Found {r:d} root nodes and {l:d} leaf nodes ({ld:d} distinct names).'.format(
      r=len(reducedRootNodes), l=len(reducedLeafNodes),
      ld=len(set(reducedLeafNodes))))
print('  Overall, {l:d} categories.'.format(
      l=len(reducedCategoryTree.categoryDict)))

# Create labels in fastText format.
df['label'] = '__label__' + df['category']

# Output labeled query data as a space-separated file.
df['output'] = df['label'] + ' ' + df['query']
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
