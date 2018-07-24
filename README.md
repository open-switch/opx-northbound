# opx-jsonrpc
This repository contains the OPX JSON RPC2.0 Northbound Application

The opx jsonrpc bridge maps yang modelled JSON RPC (as described in draft-yang-json-rpc) to CPS and vice versa. While the mapping has been tested only with OpenDaylight, other draft-yang-json-rpc
compliant implementations should be supported as well.

- Data is supported. Due to the semantic differences between ODL put/merge and CPS create/set some operations are retried using either method. That may result in some issues in rare corner cases
where the upstream is trying to create multiple list elements in one transaction (not presently supported by ODL).
- RPCs are "supported". While the code is sound and will produce a RPC request, CPS RPC is not yang compliant. The definitions lack the required argument and result details for ODL 
or another upstream YANG based system to parse the results. In fact, as the RPCs are invoked within a data tree context they are more akeen to YANG 1.1 actions, not RPCs.

## Principles of operation

The mapper accepts data and path from northbound in the form of JSON objects as described in draft-yang-json-rpc. It rewrites the request as a CPS request which is a list of key-value pairs, 
where the key is the yin representation of a path to an individual element and the value is a conversion of the json value to a CPS form. The conversion presently uses a set of fixed key-value
pair maps to map all CPS enums to their numeric values and back. Similarly, ip addresses are mapped from text (upstream) to binary (CPS) form and booleans are mapped from booleans to integers.

The mapper itself is NOT model aware. It has only whatever minimal yang model awareness can be provided by the CPS backend. This also allows it to use a **different** models upstream and
downstream. The reason for this is that the binary representations for IP addresses, MACs, etc used by CPS while more efficient do not match any of the representations in use in an
upstream system. Additionally, upstream systems do not provide any special meaning to the yang prefix statement and use the module statement instead. 

We hope that **different** models in use for the northbound presentation will one day become obsolete as CPS own models move from "internal" representation towards a "developer-centric"
representation.

The mapper is transport agnostic, needs to be loaded into a JSON RPC Service wrap and will operate using whatever transport is provided by the service wrap. Presently, the norhtbound ODL plugin
supports Zero MQ, HTTP and WebSockets as transports. The openswitch portion at present supports ZMQ and http (only ZMQ has been seen extensive testing). Other transports will be added in future releases.

## ODL Integration specifics

While the mapper itself does not need detailed schema information, ODL and the JSON-RPC 2.0 plugin in ODL does. This information is supplied via the so called library service. It provides all yang models
required to mount a resource. There is a minimal library service supplied as a part of the OPX northbound distribution. This service will will only supply models and does not support other additional
functionality from the library service specification. It is invoked in the top directory of the model tree as follows:
`setsid python -minocybe_zmq.jsonrpc zmq://0.0.0.0:4568/ inocybe_yang.library.Service >/dev/null 2>&1 &`

The port should be the same as specified in the OpenDaylight Configuration and all models including any models that are referenced should be specified in the configuration. By default, ODL JSON-RPC2.0 plugin
starts unconfigured. Once loaded it should be initialized once (the config persists) by issuing a PUT to the following URL: `http://127.0.0.1:8181/restconf/config/jsonrpc:config/` with the following contents:
```json
{
	"config":{
		"governance-root":"zmq://127.0.0.1:4568",
		"configured-endpoints":[
			{
				"name":"openswitch-1",
				"modules":[
                                    "base-common",
                                    "ietf-interfaces",
                                    "ietf-yang-types",
                                    "iana-if-type",
                                    "base-interface-common",
                                    "base-if-fc",
                                    "base-if-lag",
                                    "base-if-linux",
                                    "base-if-mgmt",
                                    "base-if-phy",
                                    "base-if-vlan",
                                    "base-ip",
                                    "base-platform-common",
                                    "dell-extensions",
                                    "dell-yang-types",
                                    "ietf-inet-types",
                                    "base-if-common",
                                    "dell-interface",
                                    "base-acl"
                                 ],
				"data-config-endpoints": [{
					"path":"{}",
					"endpoint-uri":"zmq://192.168.97.135:4569"
				}],
				"data-operational-endpoints": [{
					"path":"{}",
					"endpoint-uri":"zmq://192.168.97.135:4569"
				}]

			}
		]
	}
}
```

Explanation for this configuration:
  * Globals: library/model service is at `zmq://localhost:4658` - it can be hosted anywhere and does not need to be hosted on any of the managed devices 
  * Device called openswitch-1
    * Long list of yang modules to form the schema
    * Yang Config Data for all paths (`{}`) is at `zmq://192.168.97.135:4569`
    * Yang Oper Data for all paths (`{}`) is at the same URI

A PUT for this configuration via ODL restconf to `http://127.0.0.1:8181/restconf/config/jsonrpc:config/` will create a mountpoint called openswitch-1 which can be accessed via (example URIs to GET info on port e101-002-0)
  * RESTCONF early draft-bierman (v2) under http://127.0.0.1:8181/restconf/config/jsonrpc:config/configured-endpoints/openswitch-1/yang-ext:mount/ietf-interfaces:interfaces/interface/e101-002-0
  * RFC8040 RESTCONF under http://127.0.0.1:8181/rests/data/jsonrpc:config/configured-endpoints=openswitch-1/yang-ext:mount/ietf-interfaces:interfaces/interface=e101-002-0?content=config

Two example RESTCONF Collections (legacy restconf and RFC8040) are available in the examples directory

## API documentation
The mapper is compliant to draft-yang-json-rpc and will interact with ODL as described in the examples section.

## Packages

TODO

### Invocation 
The mapper is invoked using a service wrapper which provides it with appropriate json rpc transport binding. The PYTHONPATH should include all modules in the northbound tree as well as the CPS modules.

`python -minocybe_zmq.jsonrpc zmq://0.0.0.0:4569/ inocybe_openswitch.openswitch_data.Service`

(c) 2018 Inocybe Technologies
