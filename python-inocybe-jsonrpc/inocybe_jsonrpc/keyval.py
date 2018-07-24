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


'''A `JSON-RPC 2.0`_ asynchronous key/value store service.

   .. _JSON-RPC 2.0: http://www.jsonrpc.org/specification
'''

from inocybe_jsonrpc.jsonrpc import Service as BaseService

class Service(BaseService):
    '''A `JSON-RPC 2.0`_ asynchronous key/value store service.'''
    def __init__(self):
        super().__init__()
        self.methods = {
            'set': self.sync_set,
            'del': self.sync_del,
        }
        self.methods_async = {
            'get': self.async_get,
        }
        self._store = {}
        self._watch = {}
    def sync_set(self, key, val):
        '''Set `val` at `key`.'''
        self._store[key] = val
        try:
            handles = self._watch[key]
            del self._watch[key]
        except KeyError:
            pass
        else:
            for async_ in handles:
                self.result_async(async_, val)
    def sync_del(self, key):
        '''Delete any value at `key`.'''
        try:
            del self._store[key]
        except KeyError:
            pass
    def async_get(self, async_, key):
        '''Get the value at `key`.'''
        try:
            val = self._store[key]
        except KeyError:
            try:
                self._watch[key].append(async_)
            except KeyError:
                self._watch[key] = [async_]
        else:
            self.result_async(async_, val)
