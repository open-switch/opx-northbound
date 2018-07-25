#!/usr/bin/env python3
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



'''Method interfaces and implementations for `JSON-RPC 2.0`_ data tree services.

   .. _JSON-RPC 2.0: http://www.jsonrpc.org/specification
'''

class DataRead(object):
    '''A method interface for implementing YANG RPCs for reading data specified in OpenDaylight
       YANG module `opendaylight-jsonrpc-data`.
    '''
    def __init__(self):
        self.methods.update({ ### pylint: disable=no-member
            'exists': self.exists,
            'read': self.read,
        })
    def exists(self, store, entity, path):
        '''Method definition for opendaylight-jsonrpc-data RPC `exists`.'''
        raise NotImplementedError()
    def read(self, store, entity, path):
        '''Method definition for opendaylight-jsonrpc-data RPC `read`.'''
        raise NotImplementedError()

class DataWrite(object):
    '''A method interface for implementing YANG RPCs for writing data specified in OpenDaylight
       YANG module `opendaylight-jsonrpc-data`.
    '''
    def __init__(self):
        self.methods.update({ ### pylint: disable=no-member
            'txid': self.txid,
            'put': self.put,
            'merge': self.merge,
            'delete': self.delete,
            'commit': self.commit,
            'cancel': self.cancel,
            'error': self.error,
        })
    def txid(self):
        '''Method definition for opendaylight-jsonrpc-data RPC `txid`.'''
        raise NotImplementedError()
    def put(self, txid, store, entity, path, data): ### pylint: disable=too-many-arguments
        '''Method definition for opendaylight-jsonrpc-data RPC `put`.'''
        raise NotImplementedError()
    def merge(self, txid, store, entity, path, data): ### pylint: disable=too-many-arguments
        '''Method definition for opendaylight-jsonrpc-data RPC `merge`.'''
        raise NotImplementedError()
    def delete(self, txid, store, entity, path):
        '''Method definition for opendaylight-jsonrpc-data RPC `delete`.'''
        raise NotImplementedError()
    def commit(self, txid):
        '''Method definition for opendaylight-jsonrpc-data RPC `commit`.'''
        raise NotImplementedError()
    def cancel(self, txid):
        '''Method definition for opendaylight-jsonrpc-data RPC `cancel`.'''
        raise NotImplementedError()
    def error(self, txid):
        '''Method definition for opendaylight-jsonrpc-data RPC `error`.'''
        raise NotImplementedError()
