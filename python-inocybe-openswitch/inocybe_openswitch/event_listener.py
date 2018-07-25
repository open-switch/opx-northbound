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


'''A notification mapper for openswitch
'''

from multiprocessing import Process
import uuid

import cps
import cps_parse
import cps_utils

from inocybe_tree.pathmap import PathMap


class Handler(object):
    '''A Pathnode handler for DCN notifications'''
    def __init__(self, path, notify):
        self._uuid = uuid.uuid4()
        self._path = path
        self._notify = notify
        self._refcount = 0

    def topic(self):
        '''Topic to be used by listeners'''
        return str(self._uuid)

    def inc_refcount(self):
        '''Increment refcount'''
        if self._refcount == 0:
            self._start()
        self._refcount = self._refcount + 1

    def dec_refcount(self):
        '''Decrement refcount'''
        if self._refcount <= 0:
            raise RuntimeError("Cannot decrease refcount under zero")
        if self._refcount == 1:
            self._destroy()
        self._refcount = self._refcount - 1

    def _start(self):
        '''Start event loop'''
        self._event_loop = Process(target=self.run, args=(self._path, self.topic(), self._notify))
        self._event_loop.daemon = True
        self._event_loop.start()

    def _destroy(self):
        '''Stop the event loop'''
        self._event_loop.terminate()
        self._event_loop.join()

    @staticmethod
    def run(path, method, notify):
        '''Run the event loop'''
        handle = cps.event_connect()
        (yin_form, data) = cps_parse.yin_path(path)
        if yin_form is None:
            return
        cps_obj = cps_utils.CPSObject(yin_form, data=data, qual="observed")
        cps.event_register_object(handle, cps_obj.get())
        import traceback
        while True:
            result = cps.event_wait(handle)
            try:
                event_path = cps_parse.prep_path(yin_form, result)
                if result['data'].get("cps/object-group/return-code") is not None:
                    del result['data']["cps/object-group/return-code"]
                parsed = cps_parse.convert_result(
                    event_path,
                    result
                )
                notify(method, parsed)
            except KeyError:
                pass
            except AttributeError:
                pass

class Listener(object):
    '''A `JSON-RPC 2.0` openswitch notification mapper service.'''
    def __init__(self, notify):
        self._pathmap = PathMap()
        self._notify = notify # notify callback

    def addpath(self, path):
        '''Add a path and a method to use in a JSON RPC Notification'''
        handler = self._pathmap.mapnode(path)
        if handler is None:
            handler = self._pathmap.metadata(path, Handler(path, self._notify))
        else:
            handler = self._pathmap.metadata(path)
        handler.inc_refcount()
        return handler.topic()
        
    def delpath(self, path):
        '''Add a path and a method to use in a JSON RPC Notification'''
        handler = self._pathmap.mapnode(path)
        if handler is None:
            return
        self._pathmap.metadata(path).dec_refcount()
