#!/usr/bin/env python3

'''A `JSON-RPC 2.0`_ YANG module library service.

   .. _JSON-RPC 2.0: http://www.jsonrpc.org/specification
'''

import os.path

from inocybe_jsonrpc.jsonrpc import Service as BaseService
from inocybe_yang.finder import Finder

class Service(BaseService):
    '''A `JSON-RPC 2.0`_ YANG module library service serving YANG modules under `path`.'''
    def __init__(self, path='.'):
        BaseService.__init__(self)
        self.methods = {
            'source': self.source,
            'governance': self.governance,
        }
        self.path = os.path.abspath(path)
    def source(self, module, revision=None):
        '''Return the source text of YANG `module` at optional `revision`.'''
        for found in Finder(module, revision).find(self.path):
            if revision is None and found['revision']:
                continue
            with open(os.path.join(found['base'], found['path'])) as fid:
                return fid.read()
    @staticmethod
    def governance(store, entity, path):
        '''Return the URI of the service implementing `store` at `path` for `entity`.'''
        pass
