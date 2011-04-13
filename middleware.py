import bottle
from bottle import request
app = bottle.app()

import logging
log = logging.getLogger('middleware')
log.setLevel(logging.DEBUG)

# Tripsplit middleware
import models

def TripsplitMiddleware(app):
    def wrapper(environ, start_response):
        # Add session
        session = environ['beaker.session']
        request.session = session

        # Add user
        user_key = session.get('user_key')
        if user_key:
            request.user = models.User.get(user_key)
        else:
            request.user = None
        
        return app(environ, start_response)
    return wrapper
app = TripsplitMiddleware(app)

# Facebook
import cgi
from Cookie import SimpleCookie
import md5
from config import facebook as facebook_cfg

def FacebookMiddleware(app):
    def wrapper(environ, start_response):
        request.fb_params = None
        log.debug(environ)
        fb_cookie = SimpleCookie(environ['HTTP_COOKIE']).get('fbs_%s' % facebook_cfg.APP_ID)
        if fb_cookie:
            param_lst = cgi.parse_qsl(fb_cookie.value.strip('"'))
            params = dict(param_lst)
            base_str = ''.join('%s=%s' % (k, v) for k, v in sorted(param_lst) if k != 'sig')
            if md5.md5(base_str + facebook_cfg.APP_SECRET) == params.get('sig', ''):
                request.fb_params = params
        return app(environ, start_response)
    return wrapper
app = FacebookMiddleware(app)

# Session middleware        
from beaker.middleware import SessionMiddleware

app = SessionMiddleware(app, {
        'session.auto': True,
        'session.type': 'ext:google',
        })
