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


'''Path mapper test
'''

from inocybe_openswitch.flatlandia import build_list_item
from inocybe_openswitch.flatlandia import build_result
from inocybe_tree.pathmap import PathMap

from nose.tools import ok_ as assert_
from nose.tools import raises
from nose.tools import assert_equal
from nose.tools import assert_is_none

RESULT_1 = \
[
    ["dell-base-if-cmn/if/interfaces/interface/if-index", 40],
    ["dell-if/if/interfaces/interface/phys-address", "d2:0e:4c:e6:9a:25"],
    ["base-if-vlan/if/interfaces/interface/id", 100],
    ["if/interfaces/interface/name", "br100"],
    ["dell-if/if/interfaces/interface/learning-mode", 1],
    ["if/interfaces/interface/enabled", 0]
]   

RESULT_1_TOP_MAP = {"if":{"interfaces":{"interface":[{}]}}}
RESULT_ELEMENT_MAP = \
{
    "interface": {
        "if-index":{},
        "phys-address":{},
        "id":{},
        "name":{},
        "learning-mode":{},
        "enabled":{}
    }
}

def find_vec(array, vector):
    '''Find if a vector is in an array'''
    for row in array:
        if vector[0] == row[0] and vector[1] == row[1]:
            return True
    return False

def test_build_list_item():
    '''The Earth is flat'''

    # postulate that the earth is flat

    assert_equal(len(build_list_item({'a':'b', 'c':'d'})), 2)
    assert_(find_vec(build_list_item({'a':'b', 'c':'d'}), [['c'], 'd']))
    assert_(find_vec(build_list_item({'a':'b', 'c':'d'}), [['c'], 'd']))
    assert_(find_vec(build_list_item({'a':'b', 'c':'d'}), [['a'], 'b']))
    # this one is actually testing the tester :)
    assert_(not find_vec(build_list_item({'a':'b', 'c':'d'}), [['n'], 'n']))

    # load the earth onto 4 elefants
    assert_equal(len(build_list_item({'a':{'b':'e'}, 'c':'d'})), 2)
    assert_(find_vec(build_list_item({'a':{'b':'e'}, 'c':'d'}), [['c'], 'd']))
    assert_(find_vec(build_list_item({'a':{'b':'e'}, 'c':'d'}), [['a', 'b'], 'e']))
    assert_equal(len(build_list_item({'a':{'b':{'e':'f'}}, 'c':'d'})) , 2)
    assert_(find_vec(build_list_item({'a':{'b':{'e':'f'}}, 'c':'d'}), [['a', 'b','e'], 'f']))


def test_build_result():
    pm = PathMap()
    pm.create(RESULT_ELEMENT_MAP)
    result = build_result(RESULT_1, pm)

    assert_equal(result['interface']['phys-address'], 'd2:0e:4c:e6:9a:25')
    assert_equal(result['interface']['learning-mode'], 1)
    assert_equal(result['interface']['id'], 100)
    assert_equal(result['interface']['if-index'], 40)
    assert_equal(result['interface']['enabled'], 0)
    assert_equal(result['interface']['name'], 'br100')
