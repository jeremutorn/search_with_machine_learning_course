from opensearchpy import OpenSearch
import json

'''
Provides a simple class with internals and class methods for performing
some common, simple tasks.
'''

class OS(object):
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

    @classmethod
    def count(cls, index):
        '''
        Prints the results of a count on the given index.
        '''
        print(cls.client.cat.count(index=index, params={'v': 'true'}))

    @classmethod
    def mapping(cls, index):
        '''
        Prints the mapping of the given index.
        '''
        print(json.dumps(cls.client.indices.get_mapping(index=index), indent=2))

    @classmethod
    def samples(cls, index, field, count=16):
        '''
        Returns sample values from the given field in the given index.
        '''
        searchResult = cls.client.search(index=index, body={
            'size': count,
            'query': {
                'exists': {
                    'field': field
                }
            }
        })
        matchingDocs = searchResult.get('hits', {}).get('hits', [])
        return [doc.get('_source', {}).get(field, None) for doc in matchingDocs]
