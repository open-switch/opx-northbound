'''Test cases for inocybe_tree.jsonrpc.'''

from nose.tools import assert_equal
from nose.tools import raises

from inocybe_tree.jsonrpc import (DataRead, DataWrite)

class TestDataRead(DataRead): ### pylint: disable=abstract-method
    '''Test :class:`DataRead` method interface.'''
    def __init__(self):
        self.methods = {}
        DataRead.__init__(self)
    def test_methods(self):
        '''Test inocybe_tree.jsonrpc.DataRead registers expected methods'''
        assert_equal(self.methods, {
            'exists': self.exists,
            'read': self.read,
        })
    @raises(NotImplementedError)
    def test_exists(self):
        '''Test inocybe_tree.jsonrpc.DataRead.exists() method is abstract'''
        self.exists(0, 'foo', {})
    @raises(NotImplementedError)
    def test_read(self):
        '''Test inocybe_tree.jsonrpc.DataRead.read() method is abstract'''
        self.read(0, 'foo', {})

class TestDataWrite(DataWrite): ### pylint: disable=abstract-method
    '''Test :class:`DataWrite` method interface.'''
    def __init__(self):
        self.methods = {}
        DataWrite.__init__(self)
    def test_methods(self):
        '''Test inocybe_tree.jsonrpc.DataWrite registers expected methods'''
        assert_equal(self.methods, {
            'txid': self.txid,
            'put': self.put,
            'merge': self.merge,
            'delete': self.delete,
            'commit': self.commit,
            'cancel': self.cancel,
            'error': self.error,
        })
    @raises(NotImplementedError)
    def test_txid(self):
        '''Test inocybe_tree.jsonrpc.DataWrite.txid() method is abstract'''
        self.txid()
    @raises(NotImplementedError)
    def test_put(self):
        '''Test inocybe_tree.jsonrpc.DataWrite.put() method is abstract'''
        self.put('my txid', 0, 'foo', {}, 'bar')
    @raises(NotImplementedError)
    def test_merge(self):
        '''Test inocybe_tree.jsonrpc.DataWrite.merge() method is abstract'''
        self.merge('my txid', 0, 'foo', {}, 'bar')
    @raises(NotImplementedError)
    def test_delete(self):
        '''Test inocybe_tree.jsonrpc.DataWrite.delete() method is abstract'''
        self.delete('my txid', 0, 'foo', {})
    @raises(NotImplementedError)
    def test_commit(self):
        '''Test inocybe_tree.jsonrpc.DataWrite.commit() method is abstract'''
        self.commit('my txid')
    @raises(NotImplementedError)
    def test_cancel(self):
        '''Test inocybe_tree.jsonrpc.DataWrite.cancel() method is abstract'''
        self.cancel('my txid')
    @raises(NotImplementedError)
    def test_error(self):
        '''Test inocybe_tree.jsonrpc.DataWrite.error() method is abstract'''
        self.error('my txid')
