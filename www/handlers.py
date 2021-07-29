#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '

__author__ = 'Josef Luo'
__version__ = 'v0.1'

from models import User, Comment, Blog, next_id, time
from corweb import get, post
import asyncio

@get('/')
async def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
         Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
         Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
         Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }

@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at DESC')
    for u in users:
        u.password = '******'
    return dict(users=users)
