# Inocybe JSON-RPC 2.0

This package provides a JSON-RPC 2.0 message and service implementation.

## Pre-requisites

For Python 2:

- python

For Python 3:

- python3

## Demo

First set your PYTHONPATH to pick up dependencies.

    $ export PYTHONPATH=$PYTHONPATH:python3-inocybe/:python3-inocybe-jsonrpc/

In the following instructions $PYTHON is either `python` (for Python 2) or `python3` (for Python 3).

Now run the JSON-RPC 2.0 echo service under a minimal HTTPd on the default port (8080/tcp). We will present the 'echo' service (`inocybe_jsonrpc.echo.Service`) at URL path `/echo`. (Note that a trailing slash is considered optional in both the specification of the path and in the request. A service path specified as `/echo` or `/echo/` will handle requests for URL path `/echo` and `/echo/`.)

    $ $PYTHON -minocybe_jsonrpc.httpd /echo echo

We can access the service using curl. If you invoke the HTTP request correctly, you will get a status 200 response.

    $ curl -X POST -H 'Content-Type: application/json' -d @- http://localhost:8080/echo <<EOF
    {"jsonrpc": "2.0", "id": 1, "method": "echo", "params": {"foo": ["bar", "baz"]}}
    EOF
    {"jsonrpc": "2.0", "id": 1, "result": {"foo": ["bar", "baz"]}}

Note that status 200 only means that your JSON-RPC 2.0 Request was invoked: it does not mean that it worked! The JSON-RPC 2.0 Response contains the result or error, as appropriate. For example, if we pass broken JSON:

    $ curl -X POST -H 'Content-Type: application/json' -d @- http://localhost:8080/echo/ <<EOF
    {"jsonrpc": "2.0", "id": 1, "method": "echo
    EOF
    {"jsonrpc": "2.0", "id": null, "error": {"message": "Parse error", "code": -32700}}

If you specify a bad path, you will get status 404.

    $ curl -X POST http://localhost:8080/bad
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
            "http://www.w3.org/TR/html4/strict.dtd">
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Error response</title>
        </head>
        <body>
            <h1>Error response</h1>
            <p>Error code: 404</p>
            <p>Message: Not Found.</p>
            <p>Error code explanation: 404 - Nothing matches the given URI.</p>
        </body>
    </html>

The Content-Type must be `application/json`, if it is not then you will get status 415.

    $ curl -X POST -H 'Content-Type:application/xml' http://localhost:8080/echo
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
            "http://www.w3.org/TR/html4/strict.dtd">
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Error response</title>
        </head>
        <body>
            <h1>Error response</h1>
            <p>Error code: 415</p>
            <p>Message: Unsupported Media Type.</p>
            <p>Error code explanation: 415 - Entity body in unsupported format.</p>
        </body>
    </html>

The Content-Length must be provided, if it is not you will get status 411.

    $ curl -X POST -H 'Content-Type:application/json' -H 'Content-Length:' http://localhost:8080/echo
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
            "http://www.w3.org/TR/html4/strict.dtd">
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Error response</title>
        </head>
        <body>
            <h1>Error response</h1>
            <p>Error code: 411</p>
            <p>Message: Length Required.</p>
            <p>Error code explanation: 411 - Client must specify Content-Length.</p>
        </body>
    </html>
