#!/usr/bin/env python3

'''Find YANG modules, optionally matching a module and/or revision pattern
   in a directory tree.
'''

from __future__ import print_function

from argparse import ArgumentParser

import re
import json

from inocybe_finder.finder import Finder as BaseFinder

class Finder(BaseFinder):
    '''A finder of YANG modules or submodules matching `name` and/or `revision`.'''
    _deconstruct = re.compile(r'^([^\@]+)(?:\@(\d{4}-\d{2}-\d{2}))?\.yang$')
    def __init__(self, name=None, revision=None):
        if name is None and revision is None:
            pattern = r'^.+\.yang$'
        elif name is None:
            pattern = r'^[^\@]+\@' + revision + r'\.yang$'
        elif revision is None:
            pattern = r'^' + name + r'(?:\@\d{4}-\d{2}-\d{2})?\.yang$'
        else:
            pattern = r'^' + name + r'\@' + revision + r'\.yang$'
        BaseFinder.__init__(self, pattern)
    def deconstruct(self, filename):
        match = self._deconstruct.match(filename)
        return {
            'name': match.group(1) if match else None,
            'revision': match.group(2) if match else None,
        }

def main():
    '''Find YANG modules or submodules matching optional `name` and `revision` patterns (unanchored
       regular expressions) in the directory tree under `path`. Print information about each file in
       a JSON object on a separate line.
    '''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('-n', '--name', help='module name pattern to match, a regular expression')
    aparser.add_argument('-r', '--revision', help='revision pattern to match, a regular expression')
    aparser.add_argument('path')
    args = vars(aparser.parse_args())
    for found in Finder(args['name'], args['revision']).find(args['path']):
        print(json.dumps(found))

if __name__ == '__main__':
    main()
