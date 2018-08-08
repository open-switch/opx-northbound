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


'''Yang Data mapper for openswitch
'''

import uuid
from inocybe_tree.pathmap import PathMap
from inocybe_tree.pathmap import no_mayhem_pop
from inocybe_jsonrpc.jsonrpc import Service as BaseService
from inocybe_openswitch.cps_parse import Transaction
import cps_parse
import cps_utils

MAP = [('base-ip/ipv4/address/ip', "ipv4"),
    ('base-acl/entry/match/SRC_MAC_VALUE/addr', "mac"),
    ('base-acl/entry/match/SRC_MAC_VALUE/mask', "mac"),
    ('base-acl/entry/match/DST_MAC_VALUE/addr', "mac"),
    ('base-acl/entry/match/DST_MAC_VALUE/mask', "mac"),
    ('base-acl/entry/match/SRC_IPV4_VALUE/addr', "ipv4"),
    ('base-acl/entry/match/SRC_IPV4_VALUE/mask', "ipv4"),
    ('base-acl/entry/match/DST_IPV4_VALUE/addr', "ipv4"),
    ('base-acl/entry/match/DST_IPV4_VALUE/mask', "ipv4"),
    ('base-acl/entry/match/SRC_IPV6_VALUE/addr', "ipv6"),
    ('base-acl/entry/match/SRC_IPV6_VALUE/mask', "ipv6"),
    ('base-acl/entry/match/DST_IPV6_VALUE/addr', "ipv6"),
    ('base-acl/entry/match/DST_IPV6_VALUE/mask', "ipv6"),
    ('base-acl/entry/action/IP_NEXTHOP_GROUP_VALUE/dest_addr', "ipv4"),
    ('base-acl/entry/action/NEW_SRC_MAC_VALUE', "mac"),
    ('base-acl/entry/action/NEW_DST_MAC_VALUE', "mac"),
    ('base-acl/entry/action/NEW_SRC_IP_VALUE', "ipv4"),
    ('base-acl/entry/action/NEW_DST_IP_VALUE', "ipv4"),
    ('base-acl/entry/action/NEW_SRC_IPV6_VALUE', "ipv6"),
    ('base-acl/entry/action/NEW_DST_IPV6_VALUE', "ipv6"),
]

REMAP = [({u"ietf-interfaces:interfaces":{}}, {u"dell-base-if-cmn:if":{"interfaces":{}}}),
         ]

class Handler(object):
    '''Operation Handler - for now CPS only'''
    def __init__(self, rewrite=False, strip_path=None, add_path=None):
        self._do_rewrite = rewrite
        self._strip_path = strip_path
        self._add_path = add_path

    def _rewrite(self, path):
        '''Rewrite Path - does not support looking inside lists!!!'''
        if not self._do_rewrite:
            return path

        stripped_path = path
        walk = self._strip_path
        while walk != {} and walk != []:
            (key, walk) = no_mayhem_pop(walk)
            stripped_path = path[key]
        walk = self._add_path
        build_path = {}
        new_path = build_path
        while walk != {} and walk != []:
            (key, walk) = no_mayhem_pop(walk)
            if len(walk) == 0:
                build_path[key] = stripped_path
            else:
                build_path[key] = {}
                build_path = build_path[key]
        return new_path

    def read(self, txn, path):
        '''Read'''
        # we ignore store and entity for the moment
        path = self._rewrite(path)
        return txn.read(path)

    def exists(self, txn, path):
        '''Read'''
        # we ignore store and entity for the moment
        path = self._rewrite(path)
        return txn.exists(path)

    def put(self, txn, path, data):
        '''Put'''
        # we ignore store and entity for the moment
        txn.put(path, self._rewrite(path), data)

    def merge(self, txn, path, data):
        '''Merge'''
        # we ignore store and entity for the moment
        txn.merge(path, self._rewrite(path), data)

    def delete(self, txn, path):
        '''Delete'''
        # we ignore store and entity for the moment
        path = self._rewrite(path)
        txn.delete(path)

class Service(BaseService):
    '''A `JSON-RPC 2.0` openswitch rpc/transaction mapper service.'''
    def __init__(self):
        BaseService.__init__(self)
        self.methods = {
            'read':self.read,
            'put':self.put,
            'merge':self.merge,
            'delete':self.delete,
            'exists':self.exists,
            'commit':self.commit,
            'cancel':self.cancel,
            'txid':self.txid,
            'error':self.error
        }
        for (key, parser) in MAP:
            cps_utils.add_attr_type(key, parser)

        self._pathmap = PathMap()
        self._tx = {}
        self._rtx = Transaction()
        # set default handler
        self._pathmap.metadata({}, Handler())
        for (fr_e, to_e) in REMAP:
            self._pathmap.metadata(fr_e, Handler(rewrite=True, strip_path=fr_e, add_path=to_e))

    def txid(self):
        '''Allocate a new TXID'''
        uu4 = str(uuid.uuid4())
        while self._tx.get(uu4) is not None:
            uu4 = str(uuid.uuid4())
        self._tx[uu4] = Transaction()
        return uu4

    def read(self, store, entity, path):
        '''Read'''
        # we ignore store and entity for the moment
        handler = self._pathmap.metadata(path)
        return handler.read(self._rtx, path)

    def exists(self, store, entity, path):
        '''Read'''
        # we ignore store and entity for the moment
        handler = self._pathmap.metadata(path)
        return handler.exists(self._rtx, path)

    def put(self, txid, store, entity, path, data):
        '''Put'''
        # we ignore store and entity for the moment
        handler = self._pathmap.metadata(path)
        handler.put(self._tx[txid], path, data)

    def merge(self, txid, store, entity, path, data):
        '''Merge'''
        # we ignore store and entity for the moment
        handler = self._pathmap.metadata(path)
        handler.merge(self._tx[txid], path, data)

    def delete(self, txid, store, entity, path):
        '''Delete'''
        # we ignore store and entity for the moment
        handler = self._pathmap.metadata(path)
        handler.delete(self._tx[txid], path)

    def commit(self, txid):
        '''Commit tx'''
        return self._tx[txid].commit()

    def cancel(self, txid):
        '''Delete transaction - effectively cancel it'''
        del self._tx[txid]
        return True

    def error(self, txid):
        '''Extended Error - not yet implemented'''
        raise NotImplementedError("Extended Error not implemented")
