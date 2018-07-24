# Inocybe ZMQ

This package provides ZMQ tools.

## Pre-requisites

For Python 2:

- python
- zmq (`apt-get install python-zmq` or `pip install zmq`)

For Python 3:

- python3
- zmq (`apt-get install python3-zmq` or `pip3 install zmq`)

## Demo

First set your PYTHONPATH to pick up dependencies.

    $ export PYTHONPATH=$PYTHONPATH:python3-inocybe/:python3-inocybe-zmq/:python3-inocybe-jsonrpc/

In the following instructions $PYTHON is either `python` (for Python 2) or `python3` (for Python 3).

Now run the JSON-RPC 2.0 echo service on a ZMQ REP socket bound at zmq://0.0.0.0:4444/ (tcp).

    $ $PYTHON -minocybe_zmq.jsonrpc zmq://0.0.0.0:4444/ inocybe_jsonrpc.echo.Service

Finally, in a different terminal, set your PYTHONPATH and run a ZMQ REQ client to send lines of text from its stdin to the connected REP.

    $ $PYTHON -minocybe_zmq.requester zmq://localhost:4444 <<EOF
    {"jsonrpc": "2.0",
    {"jsonrpc": "2.0"}
    {"jsonrpc": "2.0", "id": 9, "method": "echo", "params": ["foo", "bar", "baz"]}
    {"jsonrpc": "2.0", "id": {}, "method": "ECHO", "params": {"foo": "bar"}}
    EOF

The four lines of text are:

# a broken line of JSON
# a bad request (missing method)
# a call by position to the echo method
# a call by name to the ECHO method

(All method names resolve to the same function implementation.)
