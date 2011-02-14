from google.appengine import api

import bottle

import models

def auth_login(redirect_url=None):
    """Return a (maybe registered) User, or redirect to authenticate"""
    
    if redirect_url is None:
        redirect_url = bottle.request.url
    
    gae_user = api.users.get_current_user()
    if gae_user:
        user = models.User.all().filter('gae_user =', gae_user).get()
        if user is None:
            user = models.User(gae_user=gae_user)
        return user
    else:
        bottle.redirect(api.users.create_login_url(redirect_url))

def auth_logout(redirect_url='/'):
    if api.users.get_current_user():
        bottle.request.session.pop('user_key', None)
        bottle.redirect(api.users.create_logout_url(redirect_url))
    
