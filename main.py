import json

import lib # Inits sys.path

import bottle
from bottle import route
from bottle import request
from bottle import view
from bottle import validate

import models

@route('/')
def index():
    if request.user:
        return 'Welcome %s' % request.user.username
    return 'index'

@route('/login/:username')
def login(username):
    user = models.User.all().filter('username =', username).get()
    if user:
        request.session['user_key'] = str(user.key())
        return {'status': 'success'}
    else:
        return {'status': 'failure', 'reason': 'Not found'}

@route('/create_expense', method='GET')
@view('create_expense')
def create_expense_get():
	trips = models.Trip.all()
	return dict(trips=trips)

def data_from_post(request, *keys):
	return dict((key, request.POST.get(key)) for key in keys)

@route('/create_expense', method='POST')
def create_expense_post():
	print ''
	data = data_from_post(request, 'amount', 'description', 'notes', 'trip')
	data['amount'] = float(data['amount'])
	data['trip'] = models.Trip.get_by_id(int(data['trip']))
	expense = models.Expense(**data)
	expense.put()
	print expense

#TODO @ajax
@route('/add_participant', method='POST')
def add_participant():
	user_id = request.POST.get('user')
	trip_id = request.POST.get('trip')
	user = models.User.get_by_id(int(user_id))
	trip = models.Trip.get_by_id(int(trip_id))
	#TODO enforce uniqueness constraint
	already_participant = models.Participant.all().filter('trip =', trip).filter('user =', user)
	if already_participant.fetch(1):
		return json.dumps(dict(success=False, error='%s is already participating on %s' % (user, trip)))
	participant = models.Participant(user=user, trip=trip)
	participant.put()
	return json.dumps(dict(success=True, username=user.username, email=user.email))

@route('/trip_details/:trip_id')
@validate(trip_id=int)
@view('trip_details')
def trip_details(trip_id):
	loggedin_user = request.user
	trip = models.Trip.get_by_id(trip_id)
	expenses = models.Expense.all().filter('trip =', trip)
	participants = models.Participant.all().filter('trip =', trip)

	# exclude users who are already a part of this trip
	#TODO is there a more better way to do this?
	participating_user_ids = set(part.user.key().id() for part in participants)
	users = [user for user in models.User.all() if user.key().id() not in participating_user_ids]

	return dict(expenses=expenses, trip=trip, participants=participants, users=users, loggedin_user=request.user)

@route('/list_trips')
@view('list_trips')
def list_trips():
	return dict(
		trips=models.Trip.all(),
	)

@route
def session_test():
    request.session.setdefault('test', 0)
    request.session['test'] += 1
    return {'test': request.session['test']}

# Run server
from middleware import app
bottle.debug()
bottle.run(app=app, server=bottle.AppEngineServer)
