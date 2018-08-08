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


'''ZMQ URIs.'''

from argparse import ArgumentTypeError

try:
    # Python 3
    from urllib.parse import (urlsplit, urlunsplit)
except ImportError:
    # Python 2
    # pylint: disable=wrong-import-order,import-error
    from urlparse import (urlsplit, urlunsplit)

class Uri(object):
    '''A ZMQ URI, stored as an original specification and normalized value.

       When working with :mod:`zmq`, use the normalized value.
    '''
    def __init__(self, string):
        (protocol, authority, path, query, fragment) = urlsplit(string)
        parts = self._normalize(protocol, authority, path, query, fragment)
        self._original = string
        self._normalized = urlunsplit(parts)
    @staticmethod
    def _normalize(protocol, authority, path, query, fragment):
        '''Normalize and return URI elements. Raise :class:`ValueError` if any element is not
           supported.
        '''
        errors = []
        if protocol in ('zmq', 'tcp'):
            protocol = 'tcp'
        else:
            errors.append(('protocol', protocol))
        if not authority:
            errors.append(('authority', authority))
        if path in ('', '/'):
            path = ''
        else:
            errors.append(('path', path))
        if query:
            errors.append(('query', query))
        if fragment:
            errors.append(('fragment', fragment))
        if errors:
            raise ValueError('bad values for {}'.format(
                ', '.join('{} ({})'.format(_[0], _[1]) for _ in errors)
            ))
        return (protocol, authority, path, query, fragment)
    def __str__(self):
        '''Return the normalized URI.'''
        return self.normalized
    @property
    def original(self):
        '''Return the original URI.'''
        return self._original
    @property
    def normalized(self):
        '''Return the normalized URI.'''
        return self._normalized
    @classmethod
    def arg(cls, string):
        '''Return a normalized ZMQ URI from command line arg `string`. If a normalized URI cannot be
           formed from `string`, raise :class:`ArgumentTypeError`.
        '''
        try:
            return str(cls(string))
        except ValueError as exc:
            raise ArgumentTypeError(str(exc))
