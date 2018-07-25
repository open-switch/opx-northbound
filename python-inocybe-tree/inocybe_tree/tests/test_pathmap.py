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

from inocybe_tree.pathmap import PathMap
from inocybe_tree.pathmap import PathMapListElement

from nose.tools import ok_ as assert_
from nose.tools import raises
from nose.tools import assert_equal
from nose.tools import assert_is_none

TEST_LIST = [
        {"key":1, "value":"a"},
        {"key":2, "value":"b"},
        {"key":3, "value":"c"},
        {"key":4, "value":"d"},
        {"key":5, "value":"e"},
        {"key":6, "value":"f"},
        {"key":7, "value":"g"},
        {"key":8, "value":"h"},
        {"key":9, "value":"i"},
        {"key":10, "value":"j"}
]

def test_list_element():
    '''Test the accelerated list functionality'''
    pl = PathMapListElement([])
    pl.extend(TEST_LIST)
    lk = pl.lookup({"key":9})
    assert_equal(lk["value"], "i")
    assert_equal(lk["key"], 9)
    pl.set_key(("key",))
    assert_equal(lk["value"], "i")
    assert_equal(lk["key"], 9)

def test_container_path():
    '''Basic container path mapping'''
    pm = PathMap()
    # basic set - simple two level path, get back the metadata upon creation
    # set to 1
    assert_equal(pm.metadata({"level1":{"level2":{}}}, 1), 1)
    # basic get - double check the metadata for same path a step later
    # set to 1 in previous step
    assert_equal(pm.metadata({"level1":{"level2":{}}}), 1)
    # basic failed get
    # we have no higher level inherited value and we give a wrong path - should
    # get none
    assert_is_none(pm.metadata({"level1":{"level2-wrong":{}}}))
    # basic inherited get
    # we now try a "wrong" (actually inexistent path) under a level where we
    # have something set
    import sys
    sys.stderr.write("EXPORT {} DATA {}".format(pm.export(), pm.to_data()))
    assert_equal(pm.metadata({"level1":{"level2":{"level3":{}}}}), 1)

def test_list_path():
    '''Basic list path mapping'''
    pm = PathMap()
    # basic set of metadata for whole list
    assert_equal(pm.metadata({"level1":[{}]}, 1), 1)
    # basic get of metadata for whole list
    assert_equal(pm.metadata({"level1":[{}]}), 1)
    # basic failed get - for whole list
    assert_is_none(pm.metadata({"level1-wrong":[{}]}))
    # basic inherited get - we have something set for whole list, 
    # an element should inherit it
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value"}]}), 1)

def test_list_item_path():
    '''list path mapping - item level'''
    pm = PathMap()
    # basic set to a list item
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value"}]}, 1), 1)
    # basic get for a list item
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value"}]}), 1)
    # basic get - nothing set at the to list level, we have messed only with
    # elements
    assert_is_none(pm.metadata({"level1":[{}]}))
    # basic inherited get
    # we have set metadata for {"level1":[{"level2":"level2-value"}]} to 1, subelements
    # inherit so a path under this will have 1 until we change to otherwise
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value", "content":{}}]}), 1)
    # wrong key failed get
    assert_is_none(pm.metadata({"level1":[{"level2":"level3-value"}]}))
    # wrong key look in depth failed get
    assert_is_none(pm.metadata({"level1":[{"level2":"level3-value", "content":{}}]}))

def test_list_item_complex_map ():
    '''list path mapping - item level, multiple items present'''
    # same as above, just a more complex use case where there are multiple list
    # items
    pm = PathMap()
    # basic set
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value1"}]}, 1), 1)
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value2"}]}, 2), 2)
    # basic get 1
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value1"}]}), 1)
    # basic get 2
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value2"}]}), 2)
    # basic failed get
    assert_is_none(pm.metadata({"level1":[{}]}))
    # basic inherited get
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value1", "content":{}}]}), 1)
    # basic inherited get
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value2", "content":{}}]}), 2)
    # wrong key failed get
    assert_is_none(pm.metadata({"level1":[{"level2":"level3-value"}]}))
    # wrong key look in depth failed get
    assert_is_none(pm.metadata({"level1":[{"level2":"level3-value", "content":{}}]}))

def test_list_item_complex_map_take_2 ():
    '''list path mapping - item level, multiple items present, metadata on list'''
    pm = PathMap()
    # same as above, just a more complex use case where there are multiple list
    # items and inheritance into the mix
    assert_equal(pm.metadata({"level1":[{}]}, "list"), "list")
    assert_equal(pm.metadata({"level1":[{}]}), "list")
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value1"}]}, 1), 1)
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value2"}]}, 2), 2)
    # basic get 1
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value1"}]}), 1)
    # basic get 2
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value2"}]}), 2)
    # basic failed get
    # basic inherited get
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value1", "content":{}}]}), 1)
    # basic inherited get
    assert_equal(pm.metadata({"level1":[{"level2":"level2-value2", "content":{}}]}), 2)
    # wrong key failed get
    assert_equal(pm.metadata({"level1":[{"level2":"level3-value"}]}), "list")
    # wrong key look in depth failed get
    assert_equal(pm.metadata({"level1":[{"level2":"level3-value", "content":{}}]}), "list")

def test_list_item_multiple_elements():
    '''list path mapping - item level, multiple items present, details for elements'''
    pm = PathMap()
    # same as above, use direct access to verify member content
    pm.create({"level1":[{"level2":"level3-value", "content":{}}]})
    pm.mapnode({"level1":[{"level2":"level3-value", "content":{}}]}).meta = "list"
    assert_equal(pm.metadata({"level1":[{"level2":"level3-value", "content":{}}]}), "list")
    assert_equal(pm.mapnode({"level1":[{"level2":"level3-value", "content":{}}]}), {})
    assert_equal(pm.mapnode({"level1":[{"level2":"level3-value"}]})["level2"], "level3-value")
    assert_equal(pm.mapnode({"level1":[{"level2":"level3-value"}]})["content"], {})


#def test_data_mapping():
#    # use the pathmap to stash data and ask for data back instead of pathmap or metadata
#    pm = PathMap()
#    pm.create({"level1":[{"level2":"level3-value", "content":{}}]})
#    pm.mapnode({"level1":[{"level2":"level3-value", "content":{}}]}).meta = "list"
#    assert_equal(pm.to_data()['level1'][0]['content'], "list")
#    assert_equal(pm.to_data()['level1'][0]['level2'], "level3-value")
