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


'''A `JSON-RPC 2.0`_ math service.

   .. _JSON-RPC 2.0: http://www.jsonrpc.org/specification
'''

from inocybe_jsonrpc.jsonrpc import Service as BaseService

class Service(BaseService):
    '''A `JSON-RPC 2.0`_ math service.'''
    def __init__(self):
        BaseService.__init__(self)
        self.methods = {
            'add': lambda a, b: a + b,
            'subtract': lambda a, b: a - b,
            'min': min,
            'max': max,
        }
