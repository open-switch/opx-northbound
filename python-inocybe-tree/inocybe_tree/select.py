#!/usr/bin/env python3

'''Select data from a data tree.'''

class Selector(object):
    '''A selector for selecting data from a data tree, where the tree is composed from structured
       Python values (dicts, lists) with atomic leaf data. A path, which is a similarly structured
       Python value, is used to specify which data to select, starting from a context value of the
       whole data tree:

       * an empty dict or empty list selects the current context value;
       * a non-empty dict whose pair values are all atomic values (a `match`) selects the current
         context value if that value is a dict with a matching pair value for each pair in `match`;
       * a non-empty dict with one pair value which is a structured value changes the context to the
         value of that pair, if the current context is a dict which has a value for that pair; this
         selection can be made conditional by specifying `match` pairs as above;
       * a non-empty dict with more than one pair value which is a structured value selects a dict
         formed by pairs whose values are selected from the current context value by changing the
         context to the value of each such pair, if the current context is a dict which has a value
         for that pair; this selection can be made conditional by specifying `match` pairs as above;
       * a non-empty list with one item which is a structured value changes the context to the value
         of the first item which satisfies the item selection, if the current context is a sequence;
       * a non-empty list with multiple items which are structured values selects a list formed by
         items whose values are selected from the current context value by changing the context to
         the value of each item which satisfies the item selection in turn, if the current context
         is a sequence.

       Use :classmethod:`path` to create an instance from a `path`. Call the :meth:`select` method
       of the instance to select data from a tree.
    '''
    @staticmethod
    def select(data):
        '''Return the data selected by this selector from the current context `data`. If a value
           cannot be selected then return None.

           This method selects and returns the current context `data`.
        '''
        return data
    @classmethod
    def path(cls, path, odl_kludge=False):
        '''Create a selector from `path`. If `odl_kludge` is True, then `path` is assumed to have
           been formed by ODL and any known errors in path formation shall be corrected.
        '''
        if isinstance(path, dict):
            return _SelectorDict.path(path, odl_kludge)
        elif isinstance(path, list):
            return _SelectorList.path(path, odl_kludge)
        else:
            raise ValueError('bad path: {}'.format(path))

class _SelectorDict(Selector):
    def __init__(self, match, select):
        Selector.__init__(self)
        self._match = match
        self._select = select
    def select(self, data):
        for key in self._match:
            try:
                if self._match[key] != data[key]:
                    return None
            except (KeyError, TypeError):
                return None
        if not self._select:
            return data
        selected = {}
        for key in self._select:
            selector = self._select[key]
            try:
                val = data[key]
            except (KeyError, TypeError):
                val = None
            else:
                val = selector.select(val)
            if len(self._select) == 1:
                return val
            elif val is not None:
                selected[key] = val
        if selected:
            return selected
    @classmethod
    def path(cls, path, odl_kludge=False):
        if len(path) == 0:
            return Selector()
        match = {}
        select = {}
        for key in path:
            val = path[key]
            ### if `key` has a module prefix, discard it
            try:
                key = key.split(':', 1)[1]
            except IndexError:
                pass
            try:
                ### ODL misspecifies a list selector by wrapping it in a superfluous object selector
                ### with the same YANG identifier: strip the superfluous selector as required.
                if odl_kludge and isinstance(val[key], list):
                    val = val[key]
            except (KeyError, TypeError):
                pass
            try:
                select[key] = Selector.path(val, odl_kludge)
            except ValueError:
                match[key] = val
        return cls(match, select)

class _SelectorList(Selector):
    def __init__(self, select):
        Selector.__init__(self)
        self._select = select
    def select(self, data):
        selected = []
        for selector in self._select:
            try:
                for val in data:
                    val = selector.select(val)
                    if val is None:
                        continue
                    elif len(self._select) == 1:
                        return val
                    else:
                        selected.append(val)
            except TypeError:
                return None
        if selected:
            return selected
    @classmethod
    def path(cls, path, odl_kludge=False):
        if len(path) == 0:
            return Selector()
        return cls([Selector.path(_) for _ in path])
