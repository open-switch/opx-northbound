# Inocybe YANG

This package provides:
* a YANG module finder;
* a YANG module library service for JSON RPC (for integrating with OpenDaylight).

## Pre-requisites

For Python 2:

- python

For Python 3:

- python3

## Demo: YANG module finder

First set your PYTHONPATH to pick up dependencies.

    $ export PYTHONPATH=$PYTHONPATH:python3-inocybe-yang/:python3-inocybe-finder/

In the following instructions $PYTHON is either `python` (for Python 2) or `python3` (for Python 3).

Run the finder as a module:
* the -n/--name option specifies an unanchored regular expression to match module/submodule names;
* the -r/--revision option specifies an unanchored regular expression against to match module/submodule revisions;
* the path specifies the directory tree to search for matching files.

    $ $PYTHON -minocybe_yang.finder -n 'opendaylight.*' yang.git/

...snip...
{"path": "experimental/odp/opendaylight-queue-types.yang", "base": "/home/david/yang.git", "name": "opendaylight-queue-types", "revision": null}
{"path": "experimental/odp/opendaylight-md-sal-dom.yang", "base": "/home/david/yang.git", "name": "opendaylight-md-sal-dom", "revision": null}
{"path": "experimental/odp/opendaylight-group-statistics.yang", "base": "/home/david/yang.git", "name": "opendaylight-group-statistics", "revision": null}
...snip...

    $ $PYTHON -minocybe_yang.finder -n 'ietf-inet-types' ~/yang.git/
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": "2013-07-15", "path": "standard/ietf/RFC/ietf-inet-types@2013-07-15.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xr/622/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xr/631/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xr/621/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xr/534/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xr/613/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xr/612/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xr/602/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/nx/7.0-3-I6-2/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/nx/7.0-3-I7-1/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/nx/7.0-3-I7-2/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/nx/7.0-3-I6-1/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/nx/7.0-3-I5-2/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/nx/7.0-3-I5-1/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xe/1662/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xe/1671/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xe/1651/ietf-inet-types.yang"}
{"base": "/home/david/yang.git", "name": "ietf-inet-types", "revision": null, "path": "vendor/cisco/xe/1661/ietf-inet-types.yang"}

    $ $PYTHON -minocybe_yang.finder -n 'ietf-inet-types' -r '2013.*' ~/yang.git/
{"base": "/home/david/yang.git", "revision": "2013-07-15", "name": "ietf-inet-types", "path": "standard/ietf/RFC/ietf-inet-types@2013-07-15.yang"}

### Demo: YANG module library service

The service must currently be run at the root directory from which you want to serve modules.

First set your PYTHONPATH to pick up dependencies.

    $ export PYTHONPATH=$PYTHONPATH:python3-inocybe-jsonrpc/:python3-inocybe-zmq/:python3-inocybe/:python3-inocybe-yang/:python3-inocybe-finder/

In the following instructions $PYTHON is either `python` (for Python 2) or `python3` (for Python 3).

Run the service:

    $ $PYTHON -minocybe_zmq.jsonrpc zmq://0.0.0.0:4321/ inocybe_yang.library

To test the service, fetch a module source text:

    $ $PYTHON -minocybe_zmq.requester zmq://localhost:4321/
    {"jsonrpc": "2.0", "id": "foo", "method": "source", "params": {"module": "ietf-inet-types"}}
    > {"jsonrpc": "2.0", "id": "foo", "method": "source", "params": {"module": "ietf-inet-types"}}
    < {"jsonrpc": "2.0", "id": "foo", "result": "module ietf-inet-types {\n\n  namespace \"urn:ietf:params:xml:ns:yang:ietf-inet-types\"; ...snip...
