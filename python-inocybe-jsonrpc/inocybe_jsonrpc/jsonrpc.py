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


'''`JSON-RPC 2.0`_ message and service implementation.

   A service may be implemented with synchronous methods (as per the JSON-RPC 2.0 specification),
   asynchronous methods (as per the extension defined below), or a mixture.

   Asynchronous methods are constructed on top of JSON-RPC 2.0 Request Response exchanges. A client
   may indicate a preference for asynchronous execution of a method by including an extension, a
   'metadata' object with an 'async' property with a truthy value, in a Request. If the server does
   not support asynchronous execution of the specified method then the call is always executed
   synchronously. Otherwise if the client indicates a preference for asynchronous execution and the
   server supports asynchronous execution of the specified method, then the call is executed
   asynchronously.

   Asynchronous execution of a method firstly requires assignment of a unique call handle. If the
   'async' value specified by the client is 'true', then the server allocates a call handle which
   is unique within the scope of the server. Otherwise, the 'async' value specified by the client
   is used. After allocation of the handle, the method is invoked. If the method implementation
   immediately reports a result or error condition, then a Response or Error is returned (the call
   completes as a synchronous call). Otherwise, a Response is returned including the 'metadata'
   extension, with the call handle as the 'async' property value. The client may poll for a final
   Response or Error by sending a Request including the 'metadata' object from the first Response.
   If the call has not completed, then a Response is again sent with the 'metadata' object from the
   first Response.

   .. _JSON-RPC 2.0: http://www.jsonrpc.org/specification
   .. _Request: http://www.jsonrpc.org/specification#request_object
   .. _Response: http://www.jsonrpc.org/specification#response_object
   .. _Error: http://www.jsonrpc.org/specification#error_object
'''

import json
from uuid import uuid4

class JsonRpcError(Exception):
    '''An exception specifying an `Error`_ to include in a `Response`_.'''
    def __init__(self, code, message, data=None):
        Exception.__init__(self)
        self._error = {'code': code, 'message': message}
        if data is not None:
            self._error['data'] = data
    @property
    def error(self):
        '''Return the `Error`_ for this exception.'''
        return dict(self._error)
    @classmethod
    def parse_error(cls, data=None):
        '''Return a :class:`JsonRpcError` for a Parse `Error`_.'''
        return cls(-32700, 'Parse error', data)
    @classmethod
    def invalid_request(cls, data=None):
        '''Return a :class:`JsonRpcError` for an Invalid Request `Error`_.'''
        return cls(-32600, 'Invalid Request', data)
    @classmethod
    def method_not_found(cls, data=None):
        '''Return a :class:`JsonRpcError` for a Method not found `Error`_.'''
        return cls(-32601, 'Method not found', data)
    @classmethod
    def invalid_params(cls, data=None):
        '''Return a :class:`JsonRpcError` for an Invalid params `Error`_.'''
        return cls(-32602, 'Invalid params', data)
    @classmethod
    def internal_error(cls, message, data=None):
        '''Return a :class:`JsonRpcError` for an Internal `Error`_.'''
        return cls(-32603, 'Internal error: {}'.format(message), data)

# pylint: disable=too-few-public-methods
class ValueType(object):
    '''A base class for value types.'''
    @staticmethod
    def form(value):
        '''If `value` is a valid lexical representation of a value of this type, then return the
           canonical value. Raise :class:`ValueError` otherwise.
        '''
        raise ValueError(value)

class TypeAny(ValueType):
    '''A value type accepting any value.'''
    @staticmethod
    def form(value):
        return value

class TypeInteger(ValueType):
    '''A value type accepting an integer.'''
    @staticmethod
    def form(value):
        if isinstance(value, int):
            return value
        raise ValueError(value)

class TypeString(ValueType):
    '''A value type accepting a string.'''
    @staticmethod
    def form(value):
        if isinstance(value, str):
            return value
        raise ValueError(value)

class TypeVersion(ValueType):
    '''A value type for validating `JSON-RPC 2.0`_ version.'''
    @staticmethod
    def form(value):
        if value in ('2.0', 2.0, '2', 2):
            return '2.0'
        raise ValueError(value)

class TypeMethod(ValueType):
    '''A value type for validating `JSON-RPC 2.0`_ method.'''
    @staticmethod
    def form(value):
        try:
            if not value.startswith('rpc.'):
                return value
        except AttributeError:
            pass
        raise ValueError(value)

class TypeParams(ValueType):
    '''A value type for validating `JSON-RPC 2.0`_ params.'''
    @staticmethod
    def form(value):
        if isinstance(value, (dict, list, tuple)):
            return value
        raise ValueError(value)

class TypeStructuredDict(ValueType):
    '''A value type for validating a dict's `mandatory` pairs and `optional` pairs, where
       `mandatory` and `optional` map pair keys to a :class:`ValueType` instance which forms a
       pair value.
    '''
    def __init__(self, mandatory=(), optional=()):
        ValueType.__init__(self)
        self._mandatory = dict(mandatory)
        self._optional = dict(optional)
    def form(self, value):
        if not isinstance(value, dict):
            raise ValueError(value)
        formed = {}
        for key in value:
            if key in self._mandatory:
                value_type = self._mandatory[key]
            elif key in self._optional:
                value_type = self._optional[key]
            else:
                raise ValueError(value)
            try:
                formed[key] = value_type.form(value[key])
            except ValueError:
                raise ValueError(value)
        if frozenset(self._mandatory) - frozenset(formed):
            raise ValueError(value)
        return formed

class TypeMetadata(TypeStructuredDict):
    '''A value type for validating metadata extension.'''
    def __init__(self):
        TypeStructuredDict.__init__(self, optional={'async': TypeAny})

class TypeRequestObject(TypeStructuredDict):
    '''A function for validating a `Request`_.'''
    def __init__(self):
        TypeStructuredDict.__init__(self, mandatory={
            'jsonrpc': TypeVersion,
            'method': TypeMethod,
        }, optional={
            'params': TypeParams,
            'id': TypeAny,
            'metadata': TypeMetadata(),
        })
    @classmethod
    def parse(cls, string):
        '''Parse and return a `Request`_ from JSON-encoded `string`. Otherwise raise
           :class:`JsonRpcError`.'''
        try:
            request = json.loads(string)
        except (TypeError, ValueError):
            raise JsonRpcError.parse_error()
        try:
            return cls().form(request)
        except ValueError:
            raise JsonRpcError.invalid_request()

class TypeResponseObject(TypeStructuredDict):
    '''A function for validating a `Response`_.'''
    def __init__(self):
        TypeStructuredDict.__init__(self, mandatory={
            'jsonrpc': TypeVersion,
            'id': TypeAny,
        }, optional={
            'result': TypeAny,
            'error': TypeErrorObject(),
            'metadata': TypeMetadata(),
        })
    @classmethod
    def result(cls, id_, result):
        '''Return a result `Response`_ for `id_` and `result`.'''
        return cls().form({
            'jsonrpc': '2.0',
            'id': id_,
            'result': result,
        })
    @classmethod
    def error(cls, id_, error):
        '''Return an error `Response`_ for `id_` and `error`.'''
        return cls().form({
            'jsonrpc': '2.0',
            'id': id_,
            'error': error,
        })
    @classmethod
    def async_(cls, id_, async_):
        '''Return a `Response`_ for `id_` indicating that the `Request`_ has been invoked and the
           result can be collected with `async_` handle.
        '''
        return cls().form({
            'jsonrpc': '2.0',
            'id': id_,
            'metadata': {
                'async': async_,
            },
        })

class TypeErrorObject(TypeStructuredDict):
    '''A function for validating a `Error`_.'''
    def __init__(self):
        TypeStructuredDict.__init__(self, mandatory={
            'code': TypeInteger(),
            'message': TypeString(),
        }, optional={
            'data': TypeAny(),
        })

class Service(object):
    '''A `JSON-RPC 2.0`_ service.

       To implement a service, derive from this class.

       Provide a :attr:`methods` attribute, mapping method names to function implementations where
       each function implements a synchronous call. When handling a `Request`_, a function may be
       called by position, if the params were supplied as a list, or called by name, if the params
       were supplied as a dict. The return value of the function is the result for the `Response`_.
       If the function raises an :class:`Exception` then an `Error`_ will be returned.

       Provide a :attr:`methods_async` attribute, mapping method names to function implementations
       where each function implements an asynchronous call. A function implementation must always
       specify it's first argument as an 'async' handle. This is a unique call handle which refers
       to this invocation: when the call result is available (or on failure), the handle is used to
       record the result (or error), in order that a subsequent `Request`_ can collect it. When
       handling a `Request`_, a function may be called by position, if the params were supplied as a
       list, or called by name, if the params were supplied as a dict. The return value of the
       function is ignored. If the function raises an :class:`Exception` then an `Error`_ will be
       returned.
    '''
    methods = {}
    methods_async = {}
    def __init__(self):
        self._active = {}
    def resolve_sync(self, method):
        '''Return a function implementing `method` as a synchronous call. If `method` is not
           supported with synchronous execution, return None.
        '''
        try:
            return self.methods[method]
        except KeyError:
            return None
    def resolve_async(self, method):
        '''Return a function implementing `method` as an asynchronous call. If `method` is not
           supported with asynchronous execution, return None.
        '''
        try:
            return self.methods_async[method]
        except KeyError:
            return None
    def handle_request(self, string):
        '''Handle a JSON-encoded `Request`_ in `string`, calling the method implementation and
           return a JSON-encoded `Response`_.
        '''
        try:
            request = TypeRequestObject.parse(string)
        except JsonRpcError as exc:
            response = TypeResponseObject.error(None, exc.error)
        else:
            response = self.invoke_request(request)
        return json.dumps(response)
    def invoke_request(self, request):
        '''Invoke decoded `Request`_ in `request` and return a decoded `Response`_.'''
        try:
            id_ = request['id']
        except KeyError:
            id_ = None
        method = request['method']
        try:
            params = request['params']
        except KeyError:
            params = None
        try:
            async_ = request['metadata']['async']
        except KeyError:
            async_ = False
        if async_ in self._active:
            return self.collect_async(id_, async_)
        elif async_:
            implementation = self.resolve_async(method)
            if implementation:
                return self.invoke_async(id_, implementation, params, async_)
        implementation = self.resolve_sync(method)
        if implementation:
            return self.invoke_sync(id_, implementation, params)
        error = JsonRpcError.method_not_found().error
        return TypeResponseObject.error(id_, error)
    def invoke_async(self, id_, implementation, params, async_):
        '''Invoke asynchronous method `implementation` with `params` for request `id_`. Use `async_`
           as the asynchronous call handle, unless it is True, in which case allocate a new unique
           asynchronous call handle. Return a `Response`_ which includes the unique call handle in
           the metadata; the call handle is either `async_`, or a UUID4, if `async_` is True. If
           the call immediately fails, return an `Error`_.
        '''
        if async_ is True:
            async_ = str(uuid4())
        self._active[async_] = {}
        try:
            if params is None:
                implementation(async_)
            elif isinstance(params, list):
                implementation(async_, *params)
            else:
                implementation(async_, **params)
        except TypeError as exc:
            error = JsonRpcError.invalid_params(data=str(exc)).error
            self.error_async(async_, error=error)
        except Exception as exc: # pylint: disable=broad-except
            self.error_async(async_, message=str(exc))
        return self.collect_async(id_, async_)
    def result_async(self, async_, result):
        '''The asynchronous call with handle `async_` is reporting `result`.'''
        self._active[async_]['result'] = result
    def error_async(self, async_, error=None, message=None, data=None):
        '''The asynchronous call with handle `async_` is reporting an error either as `error`, or as
           `message` with optional `data`.
        '''
        if not error:
            error = JsonRpcError.internal_error(message, data).error
        self._active[async_]['error'] = error
    def collect_async(self, id_, async_):
        '''If the asynchronous call with handle `async_` has reported a result, then complete the
           call by returning a `Response`_. If the asynchronous call has reported an error, then
           complete the call by returning an `Error`_. Otherwise, return a `Response`_ which
           includes `async_` as the unique call handle in the metadata, indicating that the call
           is still running.
        '''
        ### if error, report error
        try:
            error_ = self._active[async_]['error']
        except KeyError:
            pass
        else:
            del self._active[async_]
            return TypeResponseObject.error(id_, error_)
        ### if result, report result
        try:
            result = self._active[async_]['result']
        except KeyError:
            pass
        else:
            del self._active[async_]
            return TypeResponseObject.result(id_, result)
        ### no error or result
        return TypeResponseObject.async_(id_, async_)
    @staticmethod
    def invoke_sync(id_, implementation, params):
        '''Invoke synchronous method `implementation` with `params` for request `id_`. Return a
           decoded `Response`_ communicating the return result of `implementation`. If the call
           fails, return an `Error`_.
        '''
        try:
            if params is None:
                result = implementation()
            elif isinstance(params, list):
                result = implementation(*params)
            else:
                result = implementation(**params)
        except TypeError as exc:
            error = JsonRpcError.invalid_params(data=str(exc)).error
            return TypeResponseObject.error(id_, error)
        except NotImplementedError:
            error = JsonRpcError.internal_error('method not supported in this service').error
            return TypeResponseObject.error(id_, error)
        except Exception as exc: # pylint: disable=broad-except
            error = JsonRpcError.internal_error(str(exc)).error
            return TypeResponseObject.error(id_, error)
        else:
            return TypeResponseObject.result(id_, result)
