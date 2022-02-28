# -*- coding: utf-8 -*-

'''
Module for very basic logging of queries and results.
'''

import os

# The default logger appends to the file at this path.
# Set to None to avoid logging anything.
_defaultPath = None

class QueryLogger(object):
    '''
    Class providing a method for simple logging of queries.
    '''

    def __init__(self, path=None):
        '''
        If path is None, initializes an instance that will not save logs
        anywhere.
        Otherwise, will initializes an instance that will append to a file
        at that path.
        '''
        self._path = path
    # End of __init__().

    def log(self,
            query         =None,
            displayFilters=None,
            appliedFilters=None,
            sortField     =None,
            sortDir       =None,
            model         =None,
            explain       =None,
            response      =None,
            skuSet        =None):
        '''
        Writes information about the query to the log (or does nothing if
        logging was not enabled).
        '''
        if (self._path is None):
            return
        with open(self._path, mode='at', encoding='utf-8') as handle:
            if (not self._isStreamAtBeginning(handle)):
                self._writeLine(handle)

            if (query is None):
                self._writeLine(handle, 'No query.')
            else:
                self._writeLine(handle, 'Query: {q:s}'.format(q=query))

            if (displayFilters):
                self._writeLine(handle, 'Display filters: {d:s}'.format(
                                d=', '.join(displayFilters)))
            if (appliedFilters):
                self._writeLine(handle, 'Applied filters: {a:s}'.format(
                                a=appliedFilters))
            queryInfoList = list()
            if (sortField):
                queryInfoList.append('Sort field: {s:s}'.format(s=sortField))
            if (sortDir):
                queryInfoList.append('Sort dir: {s:s}'.format(s=sortDir))
            if (model):
                queryInfoList.append('Model: {m:s}'.format(m=model))
            if (explain is not None):
                if (explain):
                    queryInfoList.append('Explain is enabled')
                else:
                    queryInfoList.append('Explain is disabled')
            if (0 < len(queryInfoList)):
                self._writeLine(handle, ',  '.join(queryInfoList))

            hits = response
            if (hits is not None):
                hits = hits.get('hits', None)
            if (hits is not None):
                hits = hits.get('hits', None)
            if (hits is not None):
                for (ind, hit) in enumerate(hits):
                    indFromOne = ind + 1
                    source = hit.get('_source', None)
                    if (source is None):
                        self._writeLine(handle, '{ind:2d}:  Null entry'.format(
                                        ind=indFromOne))
                        continue
                    sourceId   = self._getFromSource(source, 'productId', '<NO_ID>'  )
                    sourceName = self._getFromSource(source, 'name'     , '<NO_NAME>')
                    sourceSKU  = self._getFromSource(source, 'sku'      , None       )
                    if (sourceSKU is None):
                        sourceSKU = '<NO_SKU>'
                    elif (skuSet):
                        if (sourceSKU in skuSet):
                            sourceSKU += '(    in most clicked)'
                        else:
                            sourceSKU += '(not in most clicked)'
                    self._writeLine(handle, '{ind:2d}:  ID: {i:s}  SKU: {s:s}  Name: {n:s}'.format(
                                    ind=indFromOne, i=sourceId,
                                    s=sourceSKU, n=sourceName))
    # End of log().

    @staticmethod
    def _isStreamAtBeginning(handle):
        '''
        Returns whether or not the stream is at the beginning of its
        output.  If the stream is not seekable, there is no way to
        determine, so this returns a default value.
        '''
        pos = None
        try:
            pos = handle.tell()
        except (IOError, OSError):
            # Leave pos as None.
            pass
        if (pos is None):
            # Unseekable streams are likely to be like stdout or stderr,
            # and probably already have had output written to them.  Treat
            # that as not the beginning.
            return False
        return (0 >= pos)
    # End of _isStreamAtBeginning().

    @staticmethod
    def _writeLine(handle, line=None):
        '''
        Frontend to handle.write(line) that adds an EOL.
        Just writes the EOL if line is None.
        '''
        if (line is not None):
            handle.write(line)
        handle.write(os.linesep)
    # End of _writeLine().

    @staticmethod
    def _getFromSource(source, field, default=None):
        '''
        Attempts to get the first entry for the given source field.
        Returns default if nothing is found.
        '''
        if (source is None):
            return default
        value = source.get(field, None)
        if (not value):
            return default
        return value[0]
    # End of _getFromSource().

    _path = None
    @property
    def path(self):
        '''
        Returns the path used for this instance.  None if not set.
        '''
        return self._path
    # End of path property.
# End of QueryLogger class.


# Provide a global instance for logging.
queryLogger = QueryLogger(_defaultPath)
