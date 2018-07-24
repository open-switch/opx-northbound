#!/bin/sh

LD_LIBRARY_PATH=/usr/lib/opx:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/usr/lib:/lib
PYTHONPATH=/usr/lib/opx:/usr/lib/x86_64-linux-gnu/opx:/opt/pycnoporus/python3-inocybe-zmq/:/opt/pycnoporus/python3-inocybe-jsonrpc/:/opt/pycnoporus/python3-inocybe-tree:/opt/pycnoporus/python3-inocybe-openswitch:/opt/pycnoporus/python3-inocybe:/opt/pycnoporus/python3-inocybe-finder:/opt/pycnoporus/python3-inocybe-yang
export LD_LIBRARY_PATH
export PYTHONPATH

setsid python -minocybe_zmq.jsonrpc zmq://0.0.0.0:4569/ inocybe_openswitch.openswitch_data.Service >/dev/null 2>&1 &
setsid python -minocybe_zmq.jsonrpc zmq://0.0.0.0:4570/ inocybe_openswitch.openswitch_rpc.Service >/dev/null 2>&1 &

cd /opt/pycnoporus/python3-inocybe-openswitch/models/

setsid python -minocybe_zmq.jsonrpc zmq://0.0.0.0:4568/ inocybe_yang.library.Service >/dev/null 2>&1 &
