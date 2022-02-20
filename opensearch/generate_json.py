#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Generate the JSON mapping files for the Best Buy OpenSearch indices.
'''

import json

settings = {
    'index.refresh_interval': '5s',
    'index': {
        'query': {
            'default_field': 'description'
        }
    }
}

booleanMapping = { 'type': 'boolean' }

numberMapping = { 'type': 'float' }

intMapping = { 'type': 'long' }

# Prices seem to be in units of cents, so scaling by 100 should be OK.  In
# the US, some prices go to tenths of a cent.  To be safe, scale by 10000.
priceMapping = { 'type': 'scaled_float', 'scaling_factor': 10000 }

# Set the date format that appears to be used in the data.
dateMapping = { 'type': 'date', 'format': 'yyyy-MM-dd' }
# Have a time format, for times down to milliseconds.
# The funny milliseconds specification allows this to parse three digits,
# two digits, and 1 digits after the decimal point.
# Furthermore, sometimes there is a space, and sometimes a T, between the
# date and time.
timeMapping = { 'type': 'date', 'format': "yyyy-MM-dd[ ]['T']HH:mm:ss[.][SSS][SS][S][X]" }

textMapping = { 'type': 'text', 'fields': {
    'keyword': { 'type': 'keyword', 'ignore_above': 256 }
} }

# Not sure how to handle strings that contain HTML formatting code, so
# treat them as normal text for now.
htmlMapping = textMapping

# Not sure how to handle URLs, so treat them as normal text for now.
urlMapping = textMapping

# Categories have names like cat00000.  Treat as text for now.
catMapping = textMapping

# IDs appear to be integer-valued, but the ordering is probably not
# important, so treat them as normal text for now.
idMapping = textMapping
# Ditto for SKU.
skuMapping = textMapping

# It would be nice for dimensions to be converted to numeric value in a
# fixed unit, but it is not obvious if there is a pre-built mapping for
# that, so just use text mapping for now.  Also, the formatting is not
# always the same for the number, sometimes using integer inches, decimal
# inches, and fractional inches.
# Examples:  30", 35-5/8", 0.6".
dimMapping = textMapping

# Weights have different units.  It would be nice if there were a mapping
# that converted to a numeric value with a particular unit.  For now,
# though, just treat it as text.
weightMapping = textMapping

englishMapping = textMapping.copy()
englishMapping['analyzer'] = 'english'

productsDict = {
    'settings': settings,
    'mappings': {
        'properties': {
            'productId': idMapping,
            'sku': skuMapping,
            'name': englishMapping,
            'type': englishMapping,
            'startDate': dateMapping,
            'active': booleanMapping,
            'regularPrice': priceMapping,
            'salePrice': priceMapping,
            'onSale': booleanMapping,
            'digital': booleanMapping,
            'frequentlyPurchasedWith': idMapping,
            'accessories': idMapping,
            'relatedProducts': idMapping,
            # None of the records appear to have an entry for this field,
            # so just treat it as arbitrary text.
            'crossSell': textMapping,
            'salesRankShortTerm': intMapping,
            'salesRankMediumTerm': intMapping,
            'salesRankLongTerm': intMapping,
            'bestSellingRank': intMapping,
            'url': urlMapping,
            'categoryPath': htmlMapping,
            'categoryPathIds': catMapping,
            'categoryLeaf': catMapping,
            # Seems like it should be integer-valued, but the values are
            # given as 1.0, 2.0, 3.0, etc., so treat as non-integer.
            'categoryPathCount': numberMapping,
            'customerReviewCount': intMapping,
            'customerReviewAverage': numberMapping,
            'inStoreAvailability': booleanMapping,
            'onlineAvailability': booleanMapping,
            'releaseDate': dateMapping,
            'shippingCost': priceMapping,
            'shortDescription': englishMapping,
            'shortDescriptionHtml': htmlMapping,
            'class': englishMapping,
            'classId': idMapping,
            'subclass': textMapping,
            'subclassId': htmlMapping,
            'department': englishMapping,
            'departmentId': idMapping,
            'bestBuyItemId': idMapping,
            'description': englishMapping,
            'manufacturer': textMapping,
            'modelNumber': textMapping,
            'image': urlMapping,
            # Example:  New
            # Might benefit from stemming.
            'condition': englishMapping,
            'inStorePickup': booleanMapping,
            'homeDelivery': booleanMapping,
            'quantityLimit': intMapping,
            # Example:  Stainless-Steel
            # Might benefit from stemming.
            'color': englishMapping,
            'depth': dimMapping,
            'height': dimMapping,
            'weight': weightMapping,
            # Odd that this is strictly numeric when weight has units.
            # Might be nice if there was some way to force the same units
            # for the two, but for now, just treat this as a number.
            'shippingWeight': numberMapping,
            'width': dimMapping,
            'longDescription': englishMapping,
            'longDescriptionHtml': htmlMapping,
            'features': englishMapping,
        }
    }
}

queriesDict = {
    'settings': settings,
    'mappings': {
        'properties': {
            # Seems to be a hash value.  Treat as a string.
            'user': textMapping,
            'category': catMapping,
            'query': englishMapping,
            'click_time': timeMapping,
            'query_time': timeMapping,
        }
    }
}

for (path, jsonDict) in (
    ('bbuy_products.json', productsDict),
    ('bbuy_queries.json' ,  queriesDict),
):
    with open(path, 'w') as handle:
        handle.write(json.dumps(jsonDict, indent=2))
