#!/usr/bin/env python
# Copyright (c) 2018 Inocybe Technologies.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
# LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
# FOR A PARTICULAR PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.


'''Mapping of CPS operations onto JSON RPC'''

import re
from inocybe_tree.pathmap import no_mayhem_pop
from inocybe_openswitch.map import GLOBAL_MAP
import cps_utils
import cps
import cps_operations

FIX_MODULE = re.compile(".*:.*?/")

STRIP_MODULE_RE = re.compile(".*:")

PREFIX_MAP = {'ietf-interfaces':'if',
              'base-common':'base-cmn',
              'base-interface-cmn':'base-if',
              'base-platform-common':'platform',
              'dell-extension':'os10-ext',
              'dell-yang-types':'common',
              'iana-if-type':'ianaift',
              'ietf-inet-types':'inet',
              'ietf-yang-types':'yang',
              'base-if-common':'dell-base-if-cmn',
              'dell-interface':'dell-if'}

REV_PREFIX_MAP = {'if':'ietf-interfaces',
                  'base-cmn':'base-common',
                  'base-if':'base-interface-cmn',
                  'platform':'base-platform-common',
                  'os10-ext':'dell-extension',
                  'common':'dell-yang-types',
                  'ianaift':'iana-if-type',
                  'inet':'ietf-inet-types',
                  'yang':'ietf-yang-types',
                  'dell-base-if-cmn':'base-if-common',
                  'dell-if':'dell-interface'}

def _fix_module(key):
    '''Rewrite key from yang proper to CPS:
       1. Remove module:
       2. Map module onto CPS prefix
       3. Add CPS prefix
       Return in a CPS key form
    '''
    try:
        (module, identifier) = key.split(':')
        try:
            return "/".join((PREFIX_MAP[module], identifier))
        except KeyError:
            return "/".join((module, identifier))
    except ValueError:
        return key

def _reverse_mod_map(key):
    '''Map prefix to module - back from CPS'''
    try:
        return REV_PREFIX_MAP[key]
    except KeyError:
        return key

def _fix_n_keep_module(key, pos):
    '''Rewrite data piece from yang proper to CPS:
       map onto a key, value tupple as used in the
       yin_path family of functions
    '''
    try:
        return (PREFIX_MAP[key[:pos]], key[pos+1:])
    except KeyError:
        return (key[:pos], key[pos+1:])

def _fix_module_full(orig_path, key):
    '''Rewrite key from yang proper to CPS and grow CPS key:
    '''
    pos = key.find(":")
    if pos == -1:
        if orig_path is not None:
            return "/".join((orig_path, key))
        else:
            return key

    (prefix, postfix) = _fix_n_keep_module(key, pos)
    if orig_path is not None:
        return "/".join((prefix, orig_path, postfix))
    else:
        return "/".join((prefix, postfix))

def _form_subkey(key, subkey):
    '''key formation helper - very common piece
       of code throughout - join two subkeys one of
       which may be None
    '''
    if subkey is not None and subkey != "":
        if key is not None:
            return "/".join((key, subkey))
        return subkey
    else:
        if key is not None and key != "":
            return key
        return ""

def _vandalize(yin_key, data):
    '''Prepend the current level to the keys in tree so it
       conforms to yin conventions.
    '''
    result = {}
    if data is not None:
        for (key, value) in data.items():
            result[_form_subkey(yin_key, key)] = value
    return result

def _yin_list_path(supplied_path):
    '''List subcase'''
    item_spec = supplied_path[0]
    result = {}
    subkey = None
    for (key, value) in item_spec.items():
        key = _fix_module(key)
        if isinstance(value, dict):
            (subkey, data) = _yin_other_path(value)
            if data is not None:
                result.update(_vandalize(key, data))
            subkey = _form_subkey(key, subkey)
        elif isinstance(value, list):
            (subkey, d_data) = _yin_list_path(value)
            result.update(_vandalize(key, d_data))
            subkey = _form_subkey(key, subkey)
        else:
            result.update({key: value})
    return (subkey, result)

def _yin_other_path(supplied_path):
    '''Container and scalar subcase'''
    try:
        (key, value) = no_mayhem_pop(supplied_path)
        key = _fix_module(key)
        (yin_form, data) = _yin_path(value)
        return (_form_subkey(key, yin_form), _vandalize(key, data))
    except ValueError:
        return (None, None)
    except TypeError:
        return (None, None)

def _yin_path(supplied_path):
    '''Actual path walker for effective path'''
    if isinstance(supplied_path, list):
        return _yin_list_path(supplied_path)
    # container case
    return _yin_other_path(supplied_path)

def _prep_data(orig_path, data):
    '''Set correct encoding on all data elements'''
    if isinstance(data, str):
        return data
    if isinstance(data, unicode):
        return data.encode('ascii')
    result = {}
    for (key, value) in data.items():
        if isinstance(key, unicode):
            key = key.encode('ascii')
        key = _fix_module_full(orig_path, key).encode('ascii')
        if isinstance(value, unicode):
            value = value.encode('ascii')

        if isinstance(value, str):
            pos = value.find(":")
            if pos != -1:
                try:
                    value = ":".join((PREFIX_MAP[value[:pos]], value[pos + 1:]))
                except KeyError:
                    pass

        value = GLOBAL_MAP.to_cps(key, value)

        if isinstance(value, dict):
            result[key] = _prep_data(key, value)
        elif isinstance(value, list):
            nextl = []
            for element in value:
                nextl.append(_prep_data(key, element))
            result[key] = nextl
        else:
            result[key] = value
    return result

CPS_RE = re.compile("^.*?/")

def _is_in_cps(key):
    '''Check if key is in CPS'''
    try:
        return cps.type(key) is not None
    except Exception:
        return False

def _scrub_data(data):
    '''Make sure each key is recognized by CPS
       Our adjustment algorithm tends to add in some cases
       additional module qualifiers (or they are inconsistent),
       dunno...
    '''
    res = {}
    for (key, value) in data.items():
        while key.find("/") != -1:
            if _is_in_cps(key):
                res[key] = value
                break
            key = CPS_RE.sub("", key)

    return res

def yin_path(supplied_path):
    '''YIN has no means to present a path to a list element.
       As a result, instead of presenting key in the path component,
       OpenSwitch uses partially formed data as a selection argument.
       We will walk down the supplied path and isolate the key as a
       "data snippet"
    '''
    (yin_form, data) = _yin_path(supplied_path)
    return (yin_form, _scrub_data(_prep_data(None, data)))

def _do_convert_result(in_path, element_path, value):
    '''Recursive worker for result conversion - returns a key-data pair'''
    regexp = re.compile("(.*)(" + in_path + "/)(.*)")
    cps_type = cps.type(element_path)
    rma = regexp.match(element_path)
    mod_pref = rma.group(1)
    key = rma.group(3)
    if len(mod_pref) > 0:
        key = ":".join((_reverse_mod_map(mod_pref[:-1]), key))
    if cps_type["attribute_type"] == "leaf-list":
        ylist = []
        for element in value:
            list_val = cps_utils.cps_attr_types_map.from_data(element_path, element)
            ylist.append(GLOBAL_MAP.from_cps(element_path, list_val))
        result = {key:ylist}
    elif cps_type["attribute_type"] == "list":
        ylist = []
        for element in value.values():
            list_elem = {}
            for (subkey, subvalue) in element.items():
                list_elem.update(_do_convert_result(element_path, subkey, subvalue))
            ylist.append(list_elem)
        result = {key:ylist}
    elif cps_type["attribute_type"] == "container":
        container = {}
        for (subkey, subvalue) in value.items():
            container.update(_do_convert_result(element_path, subkey, subvalue))
        result = {key:container}
    else:
        final = cps_utils.cps_attr_types_map.from_data(element_path, value)
        result = {key:GLOBAL_MAP.from_cps(element_path, final)}
    return result

def prep_path(in_path, element):
    '''Strip one or more elements from the right side of a path
       until is found in one of the keys in the element.
       CPS returns a list of key-value pairs of yin path and
       value. As a result of the prefix being pre-pended to
       the path in yin, the keys need to be pruned from
       the front so that they all start with the same path element.

       An additional complication arises from various "metadata" or
       hints elements in some CPS results. While it is theoretically
       possible to special case all of them, that is quite fragile
       so we eliminate them on the basis of them being "one-off" and
       not fitting the overall key pattern.
    '''

    score = 0
    old_score = 0
    prev_path = in_path

    while in_path.find("/") != -1:
        score = 0
        found = True
        for key in element['data'].keys():
            if key != "cps/key_data" and key != "cps/object-group/return-code" and key.find(in_path) == -1:
                found = False
            else:
                score = score + 1
        if found:
            return in_path

        if score <= old_score:
            # we are returning a path by score. This means there is no perfect match and the result is polluted

            for key in element['data'].keys():
                if key.find(in_path) == -1:
                    del element['data'][key]

            return prev_path
        prev_path = in_path
        old_score = score
        in_path = in_path[in_path.find("/") + 1:]

def convert_result(in_path, element):
    '''Convert an openswitch cps result to a form which can be serialized
       into JSON
    '''
    result = {}

    for (key, value) in element['data'].items():
        if key != 'cps/key_data':
            result.update(_do_convert_result(in_path, key, value))
        else:
            for (kkey, vvalue) in value.items():
                result.update(_do_convert_result(in_path, kkey, vvalue))
    return result

class Transaction(object):
    '''A mapper of JSON RPC to CPS Transactions'''

    def __init__(self):
        self._cps_tx = []
        self._bus_tx = None


    def create(self, txid):
        '''Create a transaction'''
        self._bus_tx = txid

    def read(self, path):
        '''Read - to be mapped on a JSON RPC read for a this entity
           argument is a json rpc path.
        '''
        (yin_form, data) = yin_path(path)

        needs_adjust = True
        cps_obj = None
        try:
            cps_obj = cps_utils.CPSObject(yin_form, data=data)
        except ValueError:
            return None
        k = [cps_obj.get()]
        res_list = []
        cps.get(k, res_list)
        result = []
        for element in res_list:
            if needs_adjust:
                yin_form = prep_path(yin_form, element)
                needs_adjust = False
            result.append(convert_result(yin_form, element))
        cps_type = cps.type(yin_form)
        try:
            if cps_type["attribute_type"] == "list":
                if data != {}:
                    if len(result) == 0:
                        return None
                    else:
                        return result[0]
                else:
                    return result
            return result[0]
        except IndexError:
            return None

    def exists(self, path):
        '''For now just read and check if it is None'''
        return self.read(path) is not None

    def _prep_cps_op(self,  orig_path, path, data):
        '''Shared code for transactional CPS ops'''
        (oyin_form, opath_data) = yin_path(orig_path)
        data = _prep_data(oyin_form, data)

        (yin_form, path_data) = yin_path(path)
        data.update(path_data)

        return cps_utils.CPSObject(yin_form, data=data)

    def put(self, orig_path, path, data):
        '''Put - create a new data element.'''
        self._cps_tx.append({'change':self._prep_cps_op(orig_path, path, data).get(), 'operation': 'create'})

    def rpc(self, orig_path, path, data):
        '''Put - create a new data element.'''
        self._cps_tx.append({'change':self._prep_cps_op(orig_path, path, data).get(), 'operation': 'action'})

    def merge(self, orig_path, path, data):
        '''Set - set value in an existing element.
        '''
        if len(data) == 0:
            return
        self._cps_tx.append({'change':self._prep_cps_op(orig_path, path, data).get(), 'operation': 'set'})

    def delete(self, path):
        '''delete - delete a new data element.
        '''
        (yin_form, path_data) = yin_path(path)
        cps_obj = cps_utils.CPSObject(yin_form, data=path_data)
        self._cps_tx.append({'change':cps_obj.get(), 'operation': 'delete'})


    def commit(self):
        '''Commit - commit the existing transaction list'''
        if len(self._cps_tx) == 0:
            return True
        result = cps.transaction(self._cps_tx)
        if result:
            return True
        # The mapping between set/create in ODL and CPS is not
        # perfect, sometimes CPS needs to be given a set where
        # ODL expects a create. Due to the fact that ODL
        # always checks for existance first this will not give
        # rise to conflicts
        for oper in self._cps_tx:
            if oper['operation'] == 'create':
                oper['operation'] = 'set'
        return cps.transaction(self._cps_tx)
