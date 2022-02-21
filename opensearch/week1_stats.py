#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Quick script to perform the searches and display the results requested at
the end of the week 1 assignment.
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

for index in ('bbuy_products', 'bbuy_queries'):
    print('Number of documents in {i:s}:  {c:d}'.format(
          i=index, c=client.count(index=index)['count']))

aggByDepartment = client.search(
    index='bbuy_products',
    body={
        'size': 0,
        'query': {
            'match_all': {}
        },
        'aggs': {
            'departments': {
                'terms': {
                    'field': 'department.keyword',
                }
            }
        }
    })
name = 'Computers'
count = 0
for bucket in aggByDepartment['aggregations']['departments']['buckets']:
    if (bucket['key'].lower() == name.lower()):
        count += bucket['doc_count']
print('Number of documents in {n:s} department:  {c:d}'.format(
      n=name, c=count))

field = 'image'
missingImage = client.count(
    index='bbuy_products',
    body={
        'query': {
            'bool': {
                'must_not': {
                    'exists': {
                        'field': field
                    }
                }
            }
        }
    })
print('Number of documents missing a value for field {f:s}:  {c:d}'.format(
      f=field, c=missingImage['count']))
