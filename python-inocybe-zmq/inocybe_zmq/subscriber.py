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


'''A command line tool for running a ZMQ SUB socket.

   Print each multipart message published on the specified topic by the single connected ZMQ PUB
   socket to stdout.
'''

from __future__ import print_function

from argparse import ArgumentParser

import zmq
from inocybe_zmq.uri import Uri

def main():
    '''Print each multipart message received from a single connected ZMQ PUB socket to stdout.'''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('-t', '--topic', default='')
    aparser.add_argument('uri', type=Uri.arg)
    args = vars(aparser.parse_args())
    topic = args['topic']
    context = zmq.Context()
    sub = context.socket(zmq.SUB) # pylint: disable=no-member
    sub.connect(args['uri'])
    sub.setsockopt(zmq.SUBSCRIBE, topic) # pylint: disable=no-member
    loop = True
    while loop:
        try:
            (topic, message) = sub.recv_multipart()
        except KeyboardInterrupt:
            loop = False
        else:
            prefix = '<({})'.format(topic) if topic else '<'
            print(prefix, message)
    sub.close()

if __name__ == '__main__':
    main()
