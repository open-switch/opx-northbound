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


'''The Earth is Flat. At least according to OpenSwitch.
This module contains functions needed to flatten dicts and
other data structures so that they can be passed to the CPS
API.
'''

import re
from inocybe_tree.pathmap import PathMap
from inocybe_tree.pathmap import no_mayhem_pop

PATH_SPLITTER = re.compile("\/")
PREF_SPLITTER = re.compile(":")

def build_list_item(item):
    '''Flatten a dict so it can be used as a cps argument
       returns an array where each row has two items -
       1. Representation of the path to an item (as a list)
       2. The actual item value
       It will barf if given a list anywhere, that's intended
       as CPS API does not allow for list nesting
    '''
    result = [] # list of two element arrays - first is an
                # array representation of the path
    for (key, value) in item.items():
        flat = []
        if isinstance(value, dict):
            for (flattened, value) in build_list_item(value):
                flat = [[key], value]
                flat[0].extend(flattened)
        else:
            flat = [[key], value]
        result.append(flat)
    return result

def _build_path(path):
    '''Build an ugly reduced semantics path'''
    if len(path) == 0:
        return {}
    key = path.pop(0)
    return {key:_build_path(path)}

def build_result(cps_result, template_pathmap):
    '''Rewrite CPS result as pathmap data
       cps returns a result as a list of key-value pairs
       where the key is a [augentation/]module/path.
    '''
    for item in cps_result:
        path = PATH_SPLITTER.split(item[0])
        while len(path) > 0:
            z = _build_path(list(path))
            result = template_pathmap.mapnode(z)
            if result is not None:
                result.data = item[1]
                break
            path.pop(0)

    return template_pathmap.to_data()
