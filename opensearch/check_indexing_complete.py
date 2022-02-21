#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Quick script to query that the indices have the expected (hardcoded) number
of ddocuments in them, indicating that indexing is finished.
'''

from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

for (index, expected) in (
        ('bbuy_products', 1275077),
        ('bbuy_queries' , 1865269),
        ('bbuy_annotations', 4862)
):
    actual = client.count(index=index)['count']
    if (actual == expected):
        print('{i:s} is complete.'.format(i=index))
    elif (actual < expected and expected > 0):
        print('{i:s} is at {a:d} / {e:d} ({p:5.2f}%)'.format(
              i=index, a=actual, e=expected, p=100*actual/expected))
    else:
        print('{i:s} received unexpected results:  actual: {a:d}  expected: {e:d}.'.format(
              i=index, a=actual, e=expected))
