import lib # Inits sys.path

import bottle
from bottle import route
from bottle import request
from bottle import view
from bottle import validate

import models

@route('/')
def index():
    return 'index'

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

@route('/add_participant', method='POST')
def add_participant():
	user_id = request.POST.get('user')
	trip_id = request.POST.get('trip')
	user = models.User.get_by_id(int(user_id))
	trip = models.Trip.get_by_id(int(trip_id))
	print trip, user
	participant = models.Participant(user=user, trip=trip)
	participant.put()
	print participant

@route('/list_expenses/:trip_id')
@validate(trip_id=int)
@view('list_expenses')
def list_expenses(trip_id):
	trip = models.Trip.get_by_id(trip_id)
	expenses = models.Expense.all().filter('trip =', trip)
	participants = models.Participant.all().filter('trip =', trip)
	users = models.User.all()
	return dict(expenses=expenses, trip=trip, participants=participants, users=users)

@route
def session_test():
    request.session.setdefault('test', 0)
    request.session['test'] += 1
    return {'test': request.session['test']}
        
        
# Run server
from middleware import app
bottle.debug()
bottle.run(app=app, server=bottle.AppEngineServer)
