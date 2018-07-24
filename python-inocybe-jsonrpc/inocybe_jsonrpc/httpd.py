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


'''A command line tool for running JSON-RPC 2.0 services under a minimal HTTPd.'''

from argparse import (ArgumentParser, ArgumentTypeError)

try:
    # Python 3
    from urllib.parse import urlparse
    from http.server import (HTTPServer, BaseHTTPRequestHandler)
except ImportError:
    # Python 2
    # pylint: disable=wrong-import-order,import-error
    from urlparse import urlparse
    from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseHTTPRequestHandler
    from SocketServer import TCPServer as HTTPServer

from inocybe.pattern import ArgModuleAttribute

def url_path(string):
    '''Return a URL path from `string`. The URL path must not specify a scheme, authority, query or
       fragment.
    '''
    parsed = urlparse(string)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise ArgumentTypeError('bad path: ' + string)
    return parsed.path

class JsonRpcHandler(BaseHTTPRequestHandler):
    '''A HTTP Request handler for JSON-RPC 2.0 method invocation.'''
    def __init__(self, request, client_address, server, services):
        ### for some reason, derived class attributes have to be initialised first...
        self._services = dict((k.rstrip('/'), v) for (k, v) in services)
        self._media_type = 'application/json'
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
    def do_POST(self): ### pylint: disable=invalid-name
        '''Invoke a JSON-RPC 2.0 Request and return the Response:

           - if the HTTP Request URL path does not map to a service, return 404;
           - if the HTTP Request Content-Type header is not application/json, return 415;
           - if the HTTP Request is missing a Content-Length header, return 411;
           - otherwise, decode a UTF-8 string from the Request Content and invoke it against the
             corresponding service, return 200 with the service Response.
        '''
        self.protocol_version = self.request_version
        try:
            service = self._services[self.path.rstrip('/')]
        except KeyError:
            self.send_error(404)
            return
        try:
            if self.headers['Content-Type'] != self._media_type:
                self.send_error(415)
                return
        except KeyError:
            pass
        try:
            length = int(self.headers['Content-Length'])
        except (KeyError, TypeError):
            self.send_error(411)
            return
        request = self.rfile.read(length).decode('utf-8')
        self.log_message('> ' + request)
        response = service.handle_request(request)
        self.log_message('< ' + response)
        response = response.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', self._media_type)
        self.send_header('Content-Length', len(response))
        self.end_headers()
        self.wfile.write(response)

def main():
    '''Run JSON-RPC 2.0 services under a minimal HTTPd.'''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('-b', '--bind', default='')
    aparser.add_argument('-p', '--port', default=8080, type=int)
    aparser.add_argument('path', type=url_path, help='the URL path at which to present `service`')
    aparser.add_argument('service', type=ArgModuleAttribute('Service'), help=', '.join((
        'the service to invoke for any POST request to `path` (with optional trailing "/")',
        'specified as a Python class implementing inocybe_jsonrpc.jsonrpc.Service',
        'or a Python module with a Service attribute',
    )))
    aparser.add_argument('args', nargs='*', help='string args to create `service` instance with')
    args = vars(aparser.parse_args())
    address = (args['bind'], args['port'])
    path = args['path']
    try:
        service = args['service'](*args['args'])
    except TypeError as exc:
        aparser.error('failed to create service instance, ' + str(exc))
    httpd = HTTPServer(address, lambda r, c, s: JsonRpcHandler(r, c, s, [(path, service)]))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()

if __name__ == '__main__':
    main()
