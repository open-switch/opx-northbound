#!/usr/bin/env python3

'''Find files matching a pattern in a directory tree.'''

from __future__ import print_function

from argparse import ArgumentParser

import re
import os
import json

class Finder(object):
    '''A finder of files whose filename matches regular expression `pattern`.'''
    def __init__(self, pattern):
        self._regexp = re.compile(pattern)
    def find(self, path):
        '''Yield information about each file matching this instance's pattern
           as a dict. The dict includes at least pairs:
           - 'base' with value `path`
           - 'path' which is the relative path to the found file under 'base'
        '''
        path = os.path.abspath(path)
        for (dirpath, _, filenames) in os.walk(path):
            for filename in filenames:
                if self._regexp.match(filename):
                    found = os.path.join(dirpath, filename)
                    result = {
                        'base': path,
                        'path': os.path.relpath(found, path),
                    }
                    result.update(
                        self.deconstruct(os.path.basename(found))
                    )
                    yield result
    def deconstruct(self, filename): # pylint: disable=unused-argument,no-self-use
        '''Return a value suitable for updating a dict with Finder-specific
           information.
        '''
        return ()

def main():
    '''Find files matching a `pattern` in the directory tree under `path`.
       Print information about each file in a JSON object on a separate line.
    '''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument(
        '-p', '--pattern', default='.*', help='filename pattern to match, a regular expression',
    )
    aparser.add_argument('path')
    args = vars(aparser.parse_args())
    for found in Finder(args['pattern']).find(args['path']):
        print(json.dumps(found))

if __name__ == '__main__':
    main()
