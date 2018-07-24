# Inocybe Finder

This package provides a file finder.

## Pre-requisites

For Python 2:

- python

For Python 3:

- python3

## Demo

First set your PYTHONPATH to pick up dependencies.

    $ export PYTHONPATH=$PYTHONPATH:python3-inocybe-finder/

In the following instructions $PYTHON is either `python` (for Python 2) or `python3` (for Python 3).

Run the finder as a module:
* the -p/--pattern option specifies a regular expression to match filenames;
* the path specifies the directory tree to search for matching files.

    $ $PYTHON -minocybe_finder.finder -p '^open' yang.git/

...snip...
{"path": "vendor/cisco/xr/622/openconfig-platform.yang", "base": "/home/david/yang.git"}
{"path": "vendor/cisco/xr/622/openconfig-types.yang", "base": "/home/david/yang.git"}
{"path": "vendor/cisco/xr/622/openconfig-if-ethernet.yang", "base": "/home/david/yang.git"}
...snip...
