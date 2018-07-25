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


'''A command line tool for running a ZMQ REQ socket.

   Each line of text from stdin is sent as a separate message to a single connected ZMQ REP socket.
'''

from __future__ import print_function

from argparse import ArgumentParser
from sys import stdin

import zmq
from inocybe_zmq.uri import Uri

def main():
    '''Send each line of text received on stdin as a separate message to a single ZMQ REP socket.'''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('uri', type=Uri.arg)
    args = vars(aparser.parse_args())
    context = zmq.Context()
    req = context.socket(zmq.REQ) # pylint: disable=no-member
    req.connect(args['uri'])
    loop = True
    while loop:
        try:
            line = stdin.readline().strip()
        except KeyboardInterrupt:
            loop = False
        else:
            if line == '':
                loop = False
            else:
                print('>', line)
                req.send_string(line)
                print('<', req.recv_string())
    req.close()

if __name__ == '__main__':
    main()
