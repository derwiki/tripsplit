import sys
sys.path.insert(0, 'lib')
sys.path.insert(0, 'lib/beaker')
sys.path.insert(0, 'lib/bottle')
sys.path.insert(0, 'lib/gaema')

import json
import logging
import traceback

import bottle
from bottle import route
from bottle import request
from bottle import view
from bottle import validate

import auth
import models

log = logging.getLogger('servlet')
log.setLevel(logging.DEBUG)

@bottle.route('/')
def index():
    log.info('user: %s' % (request.user))
    return bottle.template('home', dict(user=request.user))

@bottle.route('/details/:trip_id')
@validate(trip_id=int)
@view('details')
def details(trip_id):
    trip = models.Trip.get_by_id(trip_id)
    participants = models.Participant.all().filter('trip =', trip)

    # exclude users who are already a part of this trip
    #TODO is there a more better way to do this?
    participating_user_ids = set(part.user.key().id() for part in participants if part.user)
    log.debug('Participants for trip_id %d: %s' % (trip_id, participating_user_ids))
    users = [user for user in models.User.all() if user.key().id() not in participating_user_ids]

    return dict(
        expenses=models.Expense.all().filter('trip =', trip),
        trip=trip,
        trips=models.Trip.all(),
        participants=participants,
        users=users,
        loggedin_user=request.user
    )

@bottle.route('/login')
@bottle.route('/login/:username')
def login(username=None):
    if username:
        user = models.User.all().filter('username =', username).get()
    else:
        user = auth.auth_login()

    if user:
        if user.is_saved():
            request.session['user_key'] = str(user.key())
            return {'status': 'success'}
        else:
            return {'status': 'failure', 'reason': 'Not registered'}
    else:
        return {'status': 'failure', 'reason': 'Not found'}

@bottle.route('/logout')
def logout():
    log.debug('entering logout')
    auth.auth_logout()
    return {'status': 'success'}

@bottle.route('/register/:username')
def register(username):
    user = auth.auth_login()

    if user.is_saved():
        return {'status': 'failure', 'reason': 'Already registered as %r' % user.username}

    user.username = username
    user.put()

    return {'status': 'success'}

@bottle.route
def session_test():
    request.session.setdefault('test', 0)
    request.session['test'] += 1
    return {'test': request.session['test']}

# Run server
@bottle.error()
def errors(err):
    import sys
    sys.stderr.write(err.traceback)
    return repr(err)

#TODO we could explicitly name imports, but it seems appropriate to keep JSON
# API calls separate for actual URLs that get served
from ajaxapi import *

from middleware import app
bottle.debug()
bottle.run(app=app, server=bottle.AppEngineServer)
