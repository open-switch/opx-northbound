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


'''An RPC mapper for openswitch
'''

from inocybe_jsonrpc.jsonrpc import Service as BaseService
from inocybe_openswitch.cps_parse import Transaction
import cps_parse
import cps_utils

MAP = [('base-ip/ipv4/address/ip', "ipv4")]

class Service(BaseService):
    '''A `JSON-RPC 2.0` openswitch rpc/transaction mapper service.'''
    def __init__(self):
        BaseService.__init__(self)
        self.methods = {
            'if_name_change':self.if_name_change,
            'breakout':self.breakout,
            'set-breakout-mode':self.set_breakout_mode,
            'clear-counters':self.clear_counters,
            'clear-eee-counters':self.clear_eee_counters,
            'if_location_led':self.if_location_led,
        }
        for (key, parser) in MAP:
            cps_utils.add_attr_type(key, parser)
        self._rtx = Transaction()

    def if_name_change(self, **kwargs):
        '''Set interface'''
        self._rtx.rpc({"base-if-mgmt:if_name_change":{}}, {"base-if-mgmt:if_name_change":{}}, {"input":kwargs})
        self._rtx.commit()

    def breakout(self, **kwargs):
        '''Set interface'''
        self._rtx.rpc({"base-if-phy:breakout":{}}, {"base-if-phy:breakout":{}}, {"input":kwargs})
        self._rtx.commit()

    def set_breakout_mode(self, **kwargs):
        '''Set interface breakout mode'''
        self._rtx.rpc({"base-if-phy:set-breakout-mode":{}}, {"base-if-phy:set-breakout-mode":{}}, {"input":kwargs})
        self._rtx.commit()

    def clear_counters(self, **kwargs):
        '''Clear Counters'''
        self._rtx.rpc({"dell-if:clear-counters":{}}, {"dell-if:clear-counters":{}}, {"input":kwargs})
        self._rtx.commit()

    def clear_eee_counters(self, **kwargs):
        '''Clear Counters'''
        self._rtx.rpc({"dell-if:clear-eee-counters":{}}, {"dell-if:clear-eee-counters":{}}, {"input":kwargs})
        self._rtx.commit()

    def if_location_led(self, **kwargs):
        '''Clear Counters'''
        self._rtx.rpc({"dell-if:if-location-led":{}}, {"dell-if:if-location-led":{}}, {"input":kwargs})
        self._rtx.commit()
