# -*- coding: utf-8 -*-

from collections import namedtuple

class Category(namedtuple('Category', ('ID', 'name'))):
    '''
    ID/name tuple, for specifying initial Category information.
    '''
    # Empty class to make the docstring more apparent.
    pass
# End of Category class.

class TreeError(Exception):
    '''
    Special exception class for errors pertaining to violating the tree
    structure maintained by a CategoryTree instance.
    '''
    pass
# End of TreeError.

class CategoryTree(object):
    '''
    A class for building and accessing categories in a category tree.
    '''

    class CategoryNode(object):
        '''
        Contains information about a single category in a CategoryTree.
        '''

        def __init__(self, category):
            '''
            Sets the name and ID to those given in a Category instance.
            '''
            self._category     = category
            self._childrenDict = dict()
        # End of __init__().

        def _addChild(self, category):
            '''
            Generates a new CategoryNode instance using the information in
            category (usually a Category tuple), adds it as a child of this
            instance, and returns it.
            As a special case, if category is already a CategoryNode
            instance, then add it as a child of this instance (but the
            CategoryNode instance needs to be a root node, or this will
            raise TreeError).
            Raises TreeError if the ID is already a child.
            '''
            if (isinstance(category, CategoryTree.CategoryNode)):
                if (category._parent is not None):
                    raise TreeError('Cannot insert non-root ID {ID:s} as child'.format(
                                    ID=category.ID))
                childNode = category
            else:
                childNode = type(self)(category)
            childNode._parent = self
            child = self._childrenDict.setdefault(childNode.ID, childNode)
            if (child is not childNode):
                raise TreeError('Cannot re-add ID {ID:s} as child'.format(
                                ID=childNode.ID))
            return childNode
        # End of _addChild().

        _category = None
        @property
        def category(self):
            '''
            A Category with the ID and name for this instance.
            '''
            return self._category
        # End of category property.

        @property
        def name(self):
            '''
            The category name.
            '''
            return self._category.name
        # End of name property.

        @property
        def ID(self):
            '''
            The category ID.
            '''
            return self._category.ID
        # End of ID property.

        _parent = None
        @property
        def parent(self):
            '''
            The parent CategoryNode (None for a root node).
            '''
            return self._parent
        # End of parent property.

        _childrenDict = None
        @property
        def childrenDict(self):
            '''
            Returns a dictionary mapping ID to the children of this
            category.
            '''
            # Copy, so the original cannot be modified through this
            # property.
            return self._childrenDict.copy()
        # End of childrenDict property.

        @property
        def path(self):
            '''
            The path to this CategoryNode, starting with the root and ending
            with this node.
            '''
            ret  = list()
            node = self
            while (node is not None):
                ret.append(node)
                node = node._parent
            return tuple(reversed(ret))
        # End of path property.
    # End of CategoryNode class.

    def __init__(self):
        '''
        Initializes an empty tree.
        '''
        self._categoryDict = dict()
    # End of __init__().

    def __del__(self):
        '''
        Remove the parent and children references of all CategoryNode
        instances, so they do not form reference loops.
        '''
        for category in self._categoryDict.values():
            category._parent   = None
            category._children = dict()
    # End of __del__().

    def __getitem__(self, ID):
        '''
        Same as self.categoryDict[ID].
        '''
        # Access directly, to avoid a copy:
        return self._categoryDict[ID]
    # End of __getitem__().

    def get(self, ID, default=None):
        '''
        Same as self.categoryDict.get(ID, default=None).
        '''
        # Access directly, to avoid a copy:
        return self._categoryDict.get(ID, default)
    # End of get().

    def add(self, path):
        '''
        path should be an ordered iterable of items (may be CategoryNode
        instances, Category tuples, or IDs), each the parent of the next
        item in the iterable.  This will generate the CategoryNode
        instances if appropriate, and add them to the tree.
        Raises TreeError if an ID is duplicated, or a name does not match,
        or something violates the tree structure.
        '''
        parNode = None
        for p in path:
            ID       = None
            category = None
            if (isinstance(p, self.CategoryNode)):
                ID = p.ID
                # Do not use an external CategoryNode, because all
                # CategoryNode instances in this tree should be created and
                # owned by this instance.  Just use the Category portion.
                category = p.category
            elif (isinstance(p, Category)):
                ID       = p.ID
                category = p
            else:
                ID = p
            curNode = self._categoryDict.get(ID, None)
            if (curNode is None):
                if (category is None):
                    raise TreeError('Cannot add node ID {ID:s} without name'.format(
                                    ID=ID))
                if (parNode is None):
                    # Create a new root node.
                    curNode = self.CategoryNode(category)
                else:
                    # Create a new child node.
                    curNode = parNode._addChild(category)
                self._categoryDict[ID] = curNode
            elif (curNode.ID != ID):
                raise TreeError('ID mismatch ({ID1:s} != {ID2:s})'.format(
                                ID1=curNode.ID, ID2=ID))
            elif (category is not None and curNode.name != category.name):
                raise TreeError('Cannot mention ID {ID:s} with different name ({n1:s} != {n2:s})'.format(
                                ID=ID, n1=curNode.name, n2=category.name))
            if (curNode._parent is not parNode):
                if (parNode is None):
                    # Somebody might have decided to just specify the tail
                    # end of a path.  Allow jumping in to the middle like
                    # this.
                    pass
                elif (curNode._parent is None):
                    # Apparently a root node was added because somebody
                    # decided to add a new path without specifying the full
                    # path.  Insert this.
                    parNode._addChild(curNode)
                else:
                    # All other cases, treat as an error.
                    raise KeyError('Path does not match up with existing tree')
            parNode = curNode
    # End of add().

    _categoryDict = None
    @property
    def categoryDict(self):
        '''
        Returns a dictionary of all of the CategoryNode instances, keyed by
        ID.
        '''
        # Copy, so the original cannot be modified through this property.
        return self._categoryDict.copy()
    # End of categoryDict property.
# End of CategoryTree class.
