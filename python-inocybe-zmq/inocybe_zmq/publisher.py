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


'''A command line tool for running a ZMQ PUB socket.

   Publish each line of text from stdin as a multipart message on the specified topic to connected
   ZMQ SUB sockets.
'''

from __future__ import print_function

from argparse import ArgumentParser
from sys import stdin

import zmq
from inocybe_zmq.uri import Uri

def main():
    '''Publish each line of text from stdin as a multipart message to connected ZMQ SUB sockets.'''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('-t', '--topic', default='')
    aparser.add_argument('uri', type=Uri.arg)
    args = vars(aparser.parse_args())
    topic = args['topic']
    prefix = '>({})'.format(topic) if topic else '>'
    context = zmq.Context()
    pub = context.socket(zmq.PUB) # pylint: disable=no-member
    pub.bind(args['uri'])
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
                print(prefix, line)
                pub.send_multipart((topic, line))
    pub.close()

if __name__ == '__main__':
    main()
