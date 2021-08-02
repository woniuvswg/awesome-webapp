#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '

__author__ = 'Josef Luo'
__version__ = 'v0.1'

from models import User, Comment, Blog, next_id
from corweb import get, post
import asyncio, re, time, hashlib, logging
from config import configs
from apierror import APIValueError, APIResourceNotFoundError
from aiohttp import web

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

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def user2cookie(user, max_age):
    '''
    Generate cookie str by user
    '''
    # build cookie string by: id-expires-sha1
    expires = str(time.time() + max_age)
    s = '%s-%s-%s-%s' % (user.id, user.password, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)
    
async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.password.expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.password = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None
        
@get('/register')
def register():
    return {
        '__template__': 'register.html'
}

@get('/signin'):
def signin():
    return {
        '__template__': 'signin.html'
}

@post('/api/authenticate')
async def authenticate(*, email, password):
    if not email:
        raise APIValueError('email,', 'Invalid email.')
    if not password:
        raise APIValueError('password', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not found.')
    user = users[0]
    # check password
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(password.encode('utf-8'))
    if user.password != sha1.hexdigest():
        raise APIValueError('password', 'Invalid password.')
    # authenticate ok, set cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponlu=True)
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r
    
@get('/signout')
def signout(request):
    refer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-delectd-', max_age=0, httponly=True)
    logging.info('user signed out')
    return r
    
_RE_EMAIL= re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1, 4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
    
@post('/api/users')
async def api_refister_user(*, email, name, password):
    pass
