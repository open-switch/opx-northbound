'''Test cases for inocybe_tree.select.'''
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



from nose.tools import assert_equal
from nose.tools import raises

from inocybe_tree.select import Selector

def test_selector_bad_path():
    '''Test :class:`Selector` rejects bad path.'''
    for bad in (None, False, True, -7, 0, -3.2, 'foo', ['not a selector']):
        func = raises(ValueError)(lambda b=bad: Selector.path(b))
        fmt = 'Test inocybe_tree.select.Selector.path() rejects path {}'
        func.description = fmt.format(bad)
        yield func

class _TestPath(object): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with valid path.'''
    ### the path to test
    path = None
    ### a sequence of 2-tuples (input data, output selected)
    selects = ()
    def __init__(self):
        ### always turn on the odl_kludge: TestOdl* classes exercise the kludge
        self._selector = Selector.path(self.path, odl_kludge=True)
    def test_selects(self):
        '''Test Selector.select for input/output pairs in :attr:`selects`.'''
        for (input_, output) in self.selects:
            func = lambda s=self._selector, i=input_, o=output: assert_equal(o, s.select(i))
            fmt = 'Test inocybe_tree.select.Selector() with path {} selects {} from {}'
            func.description = fmt.format(self.path, output, input_)
            yield func

class TestDictGoal(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with dict path for select goal.'''
    path = {}
    selects = (
        (None, None),
        (False, False),
        (True, True),
        (-7, -7),
        (0, 0),
        (-3.2, -3.2),
        ('foo', 'foo'),
        ([], []),
        (['foo', 'bar'], ['foo', 'bar']),
        ({}, {}),
        ({'foo': 'bar'}, {'foo': 'bar'}),
    )

class TestDictMatch(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with dict path for select match.'''
    path = {'foo': 'bar'}
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ({}, None),
        ({'foo': 'quux'}, None),
        ({'foo': 'bar'}, {'foo': 'bar'}),
        ({'baz': 'quux'}, None),
        ({'foo': 'bar', 'baz': 'quux'}, {'foo': 'bar', 'baz': 'quux'}),
    )

class TestDictSingle(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with dict path for select single pair value.'''
    path = {'foo': {}}
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ({}, None),
        ({'foo': 'bar'}, 'bar'),
    )

class TestDictMultiple(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with dict path for select multiple pair values.'''
    path = {'foo': {}, 'bar': {}, 'baz': {}}
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ({}, None),
        ({'foo': 'wibble'}, {'foo': 'wibble'}),
        ({'foo': 'wibble', 'quux': 'thud'}, {'foo': 'wibble'}),
        ({'bar': 'xyxxz', 'baz': 'thud'}, {'bar': 'xyxxz', 'baz': 'thud'}),
        ({'wibble': 'thud'}, None),
    )

class TestDictMatchSingle(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with dict path for select match and single pair value.'''
    path = {'foo': 'bar', 'baz': {}}
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ({}, None),
        ({'foo': 'bar'}, None),
        ({'baz': 'quux'}, None),
        ({'foo': 'bar', 'baz': 'quux'}, 'quux'),
    )

class TestDictMatchMultiple(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with dict path for select match and select multiple pair values.'''
    path = {'foo': 'bar', 'baz': {}, 'quux': {}}
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ({}, None),
        ({'baz': 'thud'}, None),
        ({'baz': 'thud', 'quux': 'wibble'}, None),
        ({'foo': 'bar'}, None),
        ({'foo': 'bar', 'xyxxz': 'quuz'}, None),
        ({'foo': 'bar', 'baz': 'thud'}, {'baz': 'thud'}),
        ({'foo': 'bar', 'baz': 'thud', 'quux': 'wibble'}, {'baz': 'thud', 'quux': 'wibble'}),
    )

class TestListGoal(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with list path for select goal.'''
    path = []
    selects = (
        (None, None),
        (False, False),
        (True, True),
        (-7, -7),
        (0, 0),
        (-3.2, -3.2),
        ('foo', 'foo'),
        ([], []),
        (['foo', 'bar'], ['foo', 'bar']),
        ({}, {}),
        ({'foo': 'bar'}, {'foo': 'bar'}),
    )

class TestListSingleWhole(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with list path to select a single whole item.'''
    path = [{'foo': 'bar'}]
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ([{}], None),
        ([{'baz': 'quuz'}], None),
        ([{'foo': 'bar', 'baz': 'quuz'}, {'foo': 'bar'}], {'foo': 'bar', 'baz': 'quuz'}),
        ({}, None),
        ({'foo': 'bar'}, None),
    )

class TestListSingle(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with list path to select a single item pair value.'''
    path = [{'foo': 'bar', 'baz': {}}]
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ([{}], None),
        ([{'baz': 'quuz'}], None),
        ([{'foo': 'bar', 'baz': 'quuz'}, {'foo': 'bar'}], 'quuz'),
        ({}, None),
        ({'foo': 'bar'}, None),
    )

class TestListMultiple(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with list path to select multiple items.'''
    path = [{'foo': 'bar'}, {'foo': 'bar', 'baz': {}}]
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ([{}], None),
        ([{'baz': 'quuz'}], None),
        ([{'foo': 'bar', 'baz': 'quuz'}, {'foo': 'bar'}], [
            {'foo': 'bar', 'baz': 'quuz'}, {'foo': 'bar'}, 'quuz',
        ]),
        ({}, None),
        ({'foo': 'bar'}, None),
    )

class TestOdlList(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with ODL list path.'''
    path = {'foo:bar': {'bar': [{'baz': 'quux', 'wibble': {}}]}}
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ({}, None),
        ({'foo': 'bar'}, None),
        ({'foo:bar': {'bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}}, None),
        ({'bar': {'bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}}, None),
        ({'foo:bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}, None),
        ({'bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}, 'xyxxz'),
        ({'foo:bar': [{'foo': 'bar'}, {'baz': 'quux', 'wibble': 'xyxxz'}]}, None),
        ({'bar': [{'foo': 'bar'}, {'baz': 'quux', 'wibble': 'xyxxz'}]}, 'xyxxz'),
    )

class TestOdlNestedList(_TestPath): ### pylint: disable=too-few-public-methods
    '''Test :class:`Selector` with ODL nested list path.'''
    path = {
        'foo:bar': {
            'bar': [{
                'baz': 'quux',
                'wibble': [{
                    'quuz': 'xyxxz',
                    'thud': {},
                }]
            }],
        },
    }
    selects = (
        (None, None),
        (False, None),
        (True, None),
        (-7, None),
        (0, None),
        (-3.2, None),
        ('foo', None),
        ([], None),
        (['foo', 'bar'], None),
        ({}, None),
        ({'foo': 'bar'}, None),
        ({'foo:bar': {'bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}}, None),
        ({'bar': {'bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}}, None),
        ({'foo:bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}, None),
        ({'bar': [{'baz': 'quux', 'wibble': 'xyxxz'}]}, None),
        ({'foo:bar': [{'baz': 'quux', 'wibble': [{'quuz': 'xyxxz', 'thud': True}]}]}, None),
        ({'bar': [{'baz': 'quux', 'wibble': [{'quuz': 'xyxxz', 'thud': True}]}]}, True),
        ({'bar': [
            {'foo': 'bar'}, {'baz': 'quux', 'wibble': [
                {'foo': 'bar'}, {'quuz': 'xyxxz', 'thud': 99},
            ]},
        ]}, 99),
    )
