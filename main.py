import json
import logging
import traceback

#TODO this seems messy, importing a library makes the app work?
import lib # Inits sys.path

import bottle
from bottle import route
from bottle import request
from bottle import view
from bottle import validate

import auth
import models

log = logging.getLogger('servlet')
log.setLevel(logging.DEBUG)

def ajax(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                res.setdefault('success', True)
                return json.dumps(res)
            except Exception, e:
                log.error(traceback.format_exc())
                log.error(e)
                return json.dumps(dict(sucess=False, error=str(e)))
        return wrapper
    return decorator

@route('/')
def index():
    return bottle.template('home', dict(user=request.user))

@route('/login')
@route('/login/:username')
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

@route('/logout')
def logout():
    log.debug('entering logout')
    auth.auth_logout()
    return {'status': 'success'}

@route('/register/:username')
def register(username):
    user = auth.auth_login()

    if user.is_saved():
        return {'status': 'failure', 'reason': 'Already registered as %r' % user.username}

    user.username = username
    user.put()

    return {'status': 'success'}


def data_from_post(request, *keys):
    return dict((key, request.POST.get(key)) for key in keys)

@ajax
@route('/add_expense', method='POST')
def add_expense():
    data = data_from_post(request, 'amount', 'description', 'notes', 'trip')
    data['amount'] = float(data['amount'])
    data['trip'] = models.Trip.get_by_id(int(data['trip']))
    data['payer'] = request.user
    log.debug('data: %s' % data)
    expense = models.Expense(**data)
    expense.put()
    log.debug('expense: %s' % expense)
    log.debug('user: %s' % request.user)
    log.debug('request: %s' % request)
    trip = data['trip']
    return dict(
        trip=trip.key().id(),
        created=expense.created.strftime('%Y-%m-%d'),
        expense_id=expense.key().id(),
        amount=data.pop('amount'),
        description=data.pop('description'),
        payer=request.user.username
    )

@ajax
@route('/add_participant', method='POST')
def add_participant():
    user_id = request.POST.get('user')
    trip_id = request.POST.get('trip')
    log.debug('%s, %s' % (user_id, trip_id))
    user = models.User.get_by_id(int(user_id))
    trip = models.Trip.get_by_id(int(trip_id))
    #TODO enforce uniqueness constraint
    already_participant = models.Participant.all().filter('trip =', trip).filter('user =', user)
    if already_participant.fetch(1):
        return json.dumps(dict(success=False, error='%s is already participating on %s' % (user, trip)))
    participant = models.Participant(user=user, trip=trip)
    participant.put()
    return dict(username=user.username, email=user.email, participant=participant.key().id())

@route('/remove_participant', method='POST')
def remove_participant():
    participant_id = request.POST.get('participant');
    participant = models.Participant.get_by_id(int(participant_id))
    user_id = participant.user.key().id()
    user_name = participant.user.username
    participant.delete()
    return json.dumps(dict(success=True, user_id=user_id, username=user_name))

@ajax
@route('/remove_expense', method='POST')
def remove_expense():
    expense_id = request.POST.get('expense');
    expense = models.Expense.get_by_id(int(expense_id))
    expense.delete()
    return {}

@route('/trip_details/:trip_id')
@validate(trip_id=int)
@view('trip_details')
def trip_details(trip_id):
    trip = models.Trip.get_by_id(trip_id)
    participants = models.Participant.all().filter('trip =', trip)

    # exclude users who are already a part of this trip
    #TODO is there a more better way to do this?
    participating_user_ids = set(part.user.key().id() for part in participants)
    users = [user for user in models.User.all() if user.key().id() not in participating_user_ids]

    return dict(
        expenses=models.Expense.all().filter('trip =', trip),
        trip=models.Trip.get_by_id(trip_id),
        trips=models.Trip.all(),
        participants=participants,
        users=users,
        loggedin_user=request.user
    )

@ajax
@route('/add_trip', method='POST')
def add_trip():
    data = data_from_post(request, 'tripname', 'description', 'notes')
    data['creator'] = request.user
    data['name'] = data.pop('tripname')
    trip = models.Trip(**data)
    trip.put()
    log.debug("trip_id: %s" % trip.key().id())
    return dict(trip_id=trip.key().id())

@ajax
@route('/json/users')
def json_users():
    return dict((
        user.email, {'id': user.key().id(), 'username': user.username}
    ) for user in models.User.all())# if user.email is not None))

@route
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

from middleware import app
bottle.debug()
bottle.run(app=app, server=bottle.AppEngineServer)
