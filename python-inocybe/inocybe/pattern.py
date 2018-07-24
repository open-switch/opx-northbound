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


'''A mixed bag of pattern implementations.'''

from argparse import ArgumentTypeError
from importlib import import_module

class ArgModuleAttribute(object): ### pylint: disable=too-few-public-methods
    '''Call an instance of this class to import a module attribute as specified
       by an input string. `default` specifies the attribute name to use when
       the input string only specifies the module.
    '''
    def __init__(self, default=None):
        self._default = default
    def __call__(self, string):
        try:
            module = import_module(string)
        except ImportError:
            parts = string.split('.')
            try:
                module = import_module('.'.join(parts[:-1]))
            except ImportError:
                reason = 'failed to import module {}'
                raise ArgumentTypeError(reason.format(string))
            else:
                attr = parts[-1]
        else:
            if self._default is None:
                reason = '{} does not include an attribute name'
                raise ArgumentTypeError(reason.format(string))
            attr = self._default
        try:
            return getattr(module, attr)
        except AttributeError:
            reason = '{} does not have an attribute named "{}"'
            raise ArgumentTypeError(reason.format(module.__name__, attr))
