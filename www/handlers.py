#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '

__author__ = 'Josef Luo'
__version__ = 'v0.1'

from models import User, Comment, Blog, next_id
from corweb import get, post
import asyncio

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }

