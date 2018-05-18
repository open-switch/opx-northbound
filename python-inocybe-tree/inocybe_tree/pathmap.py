#!/usr/bin/env python

'''Path mapper

YANG modeled JSON RPC 2.0 semantics.

Paths are expressed as:
    {"level1":{"level2":{}}} for containers. {} signifies the end.

If a container contains:
    {"level1":{"level2":1,"level2-more":2}} the above path will
address 1.

A path of {"level1":{}} will address {"level2":1,"level2-more":2}

Each node in the path map has two "slots" to store "things" on it
"data" and "meta".

Meta is intended to store schema related information such as
instances of classes responsible for mapping operations
onto actual device operations.

Data is intended to store actual data when the schema tree is used
as a temporary scratchpad in data operations.

'''

class MetaMixin(object):
    '''Metadata and Data base mixin for yang tree'''
    def __init__(self):
        self._metadata = None
        self._data = None
        self._validator = None

    @property
    def validator(self):
        '''Get metadata'''
        return self._validator

    @validator.setter
    def validator(self, val):
        '''metadata setter'''
        self._validator = val

    @property
    def meta(self):
        '''Get metadata'''
        return self._metadata

    @meta.setter
    def meta(self, val):
        '''metadata setter'''
        self._metadata = val

    @property
    def data(self):
        '''Get data'''
        return self._data

    @data.setter
    def data(self, val):
        '''Data setter'''
        if self._validator is not None:
            self._data = self._validator(val)
        else:
            self._data = val

class PathMapContainerElement(dict, MetaMixin):
    '''Dict with metadata'''
    def __init__(self, val):
        dict.__init__(self, {})
        for (key, value) in val.items():
            if isinstance(value, dict):
                self[key] = PathMapContainerElement(value)
            elif isinstance(value, list):
                self[key] = PathMapListElement(value)
            else:
                self[key] = value

        MetaMixin.__init__(self)

class PathMapListElement(list, MetaMixin):
    '''Yang List with metadata and a known key. Key is a tuple of
       fields used for indexing (normal yang list semantics)'''
    def __init__(self, val, key_fields=None):
        MetaMixin.__init__(self)
        list.__init__(self, [])
        self._key_fields = key_fields
        self._index = {}
        for nested in val:
            if len(nested) > 0:
                self.append(PathMapContainerElement(nested))

    def set_key(self, key_fields):
        '''Set an index after the fact not at construction'''
        self._key_fields = key_fields
        self._index = {}
        for item in self:
            self._add_to_index(item)

    def _form_key(self, val):
        '''Create a key-value tupple which we can hash on'''
        result = []
        for key in self._key_fields:
            result.append(key)
            result.append(val[key])
        return tuple(result)

    def _add_to_index(self, val):
        '''Add an element to the index'''
        if self._key_fields is not None:
            if self._form_key(val) in self._index:
                raise KeyError("Duplicate Key")
            else:
                self._index[self._form_key(val)] = val

    def _del_from_index(self, val):
        '''Delete element to the index'''
        if self._key_fields is not None:
            del self._index[self._form_key(val)]

    def append(self, val):
        '''Index aware append version'''
        self._add_to_index(val)
        return super(PathMapListElement, self).append(val)

    def extend(self, val):
        '''Index aware extend version'''
        for item in val:
            self._add_to_index(item)
        return super(PathMapListElement, self).extend(val)

    def insert(self, i, pos):
        '''Index aware insert version'''
        self._add_to_index(i)
        return super(PathMapListElement, self).insert(i, pos)

    def remove(self, pos):
        '''Index aware remove version'''
        self.pop(pos)

    def pop(self, pos=0):
        '''Index aware pop version'''
        result = super(PathMapListElement, self).pop(pos)
        self._del_from_index(result)
        return result

    def _brute_force_lookup(self, val):
        '''Lookup for the case where index is unavailable'''
        for item in self:
            found = True
            for key in val.keys():
                if item.get(key) != val[key]:
                    found = False
                    break
            if found:
                return item
        return None

    def lookup(self, val):
        '''Lookup an element by key'''
        if self._key_fields is not None:
            return self._index[self._form_key(val)]
        else:
            return self._brute_force_lookup(val)

class PathMap(object):
    '''A class to map a YIId path or JSON RPC Draft path to an actual "fetch"
       function'''
    def __init__(self, inherit=True):
        self._path_map = PathMapContainerElement({})
        self._default_metadata = None
        self._inherit = inherit

    @staticmethod
    def _do_container(path_map, path, create=False, inherit=True):
        '''Dict case for walking a pathmap'''

        key = None
        next_item = None

        try:
            (key, next_item) = no_mayhem_pop(path)
        except TypeError:
            return path_map

        if path_map.get(key) is None:
            # Path does not exist in pathmap
            if create:
                if isinstance(next_item, dict):
                    path_map[key] = PathMapContainerElement(next_item)
                else:
                    path_map[key] = PathMapListElement(next_item)
            else:
                if inherit:
                    return path_map
                else:
                    return None

        result = PathMap._do_element(path_map[key], next_item, create, inherit)
        if (result is None) and inherit:
            return path_map
        return result

    @staticmethod
    def _do_list(path_map, path, create=False, inherit=True):
        '''List case for walking a pathmap'''
        item_key = {}
        next_key = None
        next_item = None
        result = None

        if len(path) == 0:
            return path_map

        for (key, value) in path[0].items():
            if isinstance(value, dict) or isinstance(value, list):
                next_key = key
                next_item = value
            else:
                item_key[key] = value

        if len(item_key) == 0:
            return path_map

        found = path_map.lookup(item_key)
        if found is not None:
            if next_key is None:
                result = found
            else:
                try:
                    result = PathMap._do_element(found[next_key], next_item, create, inherit)
                except KeyError:
                    result = found

        if (not found) and create:
            new_item = PathMapContainerElement(dict(path[0]))
            path_map.append(new_item)
            result = PathMap._do_container(new_item, path[0], create, inherit)

        if (result is None) and inherit:
            return path_map
        else:
            return result

    @staticmethod
    def _do_element(path_map, path, create=False, inherit=True):
        '''Recursively descend down the tree creating it as needed
           and honoring inheritance'''

        # dict case
        result = None
        if isinstance(path, dict):
            result = PathMap._do_container(path_map, path, create, inherit)

        # list case
        if isinstance(path, list):
            result = PathMap._do_list(path_map, path, create, inherit)
        return result

    def mapnode(self, path):
        '''Return the actual underlying node (not honoring inheritance)'''
        return PathMap._do_element(self._path_map, path, inherit=False)

    def mapnode_in_charge(self, path):
        '''Return the actual underlying node - honoring inheritance)'''
        return PathMap._do_element(self._path_map, path, inherit=True)

    def create(self, path):
        '''Return the actual underlying node (not honoring inheritance)'''
        PathMap._do_element(self._path_map, path, inherit=False, create=True)

    def metadata(self, path, metadata=None):
        '''Attach or get a metadata elementto a part of the tree. Honors inheritance.
           There is no restriction on the type of metadata element - it can be code,
           object or a tooth fairy instance - up to the user.'''

        result = PathMap._do_element(self._path_map, path, metadata is not None)
        if result is not None:
            if metadata is not None:
                result.meta = metadata
            return result.meta
        return None

    def export(self):
        '''Dump the map in object only format (no hanlders)'''
        return self._path_map

    @staticmethod
    def _container_to_data(path_map):
        '''Dict case for convert to data'''

        if len(path_map) > 0:
            result = {}
            for (key, next_item) in path_map.items():
                next_level = PathMap._to_data(next_item)
                if (next_level is not None) and (not next_level == {}):
                    result[key] = next_level
            return result
        return path_map.data

    @staticmethod
    def _list_to_data(path_map):
        '''List case for convert to data'''

        result = []
        for next_item in path_map:
            result.append(PathMap._container_to_data(next_item))
        return result

    @staticmethod
    def _to_data(path_map):
        '''Recursively descend down the tree replacing all {} with
           meta in their object if present, deleting otherwise'''

        # dict case
        if isinstance(path_map, dict):
            return PathMap._container_to_data(path_map)

        # list case
        if isinstance(path_map, list):
            return PathMap._list_to_data(path_map)
        return path_map.data


    def to_data(self):
        '''Recursively descend down the tree replacing all {} with
           meta in their object if present, deleting otherwise,
           return the result'''
        return PathMap._to_data(self._path_map)


def no_mayhem_pop(val):
    '''Non-destructive popitem'''
    for (key, value) in val.items():
        return (key, value)
    return None
