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


'''A command line tool for running a JSON-RPC 2.0 service on a ZMQ REP socket.'''

import logging

from argparse import (ArgumentParser, ArgumentTypeError)
import zmq
from inocybe.pattern import ArgModuleAttribute

from inocybe_zmq.uri import Uri

def zmq_uri(string):
    '''Return a normalized ZMQ URI from command line arg `string`.'''
    try:
        return str(Uri(string))
    except ValueError as exc:
        raise ArgumentTypeError(str(exc))

def main():
    '''Run a JSON-RPC 2.0 service on a ZMQ REP socket.'''
    logging.basicConfig(level=logging.INFO)
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('uri', type=zmq_uri, help='the URI at which to bind a ZMQ REP socket')
    aparser.add_argument('service', type=ArgModuleAttribute('Service'), help=', '.join((
        'the service to run on the socket',
        'specified as a Python class implementing inocybe_jsonrpc.jsonrpc.Service',
        'or a Python module with a Service attribute',
    )))
    aparser.add_argument('args', nargs='*', help='string args to create `service` instance with')
    args = vars(aparser.parse_args())
    context = zmq.Context()
    rep = context.socket(zmq.REP) # pylint: disable=no-member
    rep.bind(args['uri'])
    try:
        service = args['service'](*args['args'])
    except TypeError as exc:
        aparser.error('failed to create service instance, ' + str(exc))
    loop = True
    while loop:
        try:
            input_ = rep.recv_string()
        except KeyboardInterrupt:
            loop = False
        else:
            logging.info('> %s', input_)
            output = service.handle_request(input_)
            rep.send_string(output)
            logging.info('< %s', output)
    rep.close()

if __name__ == '__main__':
    main()
