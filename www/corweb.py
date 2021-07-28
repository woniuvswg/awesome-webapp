#!/usr/bin/env python3
# -*- coding:utf-8 -*-


__author__ = 'Josef Luo'
__version__ = 'v0.1'


import functools, os, inspect, logging, asyncio
from urllib import parse
from aiohttp import web

def get(path):
    '''
    Define decorator @get('/path') //http get request handler
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator


def post(path):
    '''
    Define decorator @post('/path') //http post request handler
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


'''
Request function args handler
@param: fn --> Request function
'''
def get_required_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)
    
def get_named_kw_args(fn):
    args = []
    params = inspect.signature(fn).parameters
    for name, param in params.item():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)
    
def has_named_kw_args(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.item():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True
            
def has_var_kw_arg(fn):
    params = inspect.signature(fn).parameters
    for name, param in params.item():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items(0):
        if name == 'request':
            found = True
            continue
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError(' request must be the last named parameter in function: %s%s' % (fn.__name__, str(sig)))
            
    return found
            

class RequestHandler(object):
    def __init__(self, app, fn):
        self._app = app
        self._fn = fn
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_named_kw_args = has_named_kw_args(fn)
        self._named_kw_args = get_named_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)
        
    def __call__(self, request):
    
    def
