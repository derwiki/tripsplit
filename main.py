import sys


sys.path.insert(0, 'lib/bottle')
import bottle
from bottle import route
from bottle import request
from bottle import view

import models

@route('/')
def index():
    return 'index'

@route('/create_expense', method='GET')
@view('create_expense')
def create_expense_get():
	return dict()

def data_from_post(request, *keys):
	return dict((key, request.POST.get(key)) for key in keys)

@route('/create_expense', method='POST')
def create_expense_post():
	print ''
	data = data_from_post(request, 'amount', 'description', 'notes')
	data['amount'] = float(data['amount'])
	expense = models.Expense(**data)
	print expense

@route
def session_test():
    request.session.setdefault('test', 0)
    request.session['test'] += 1
    return {'test': request.session['test']}
        
        
# Run server
from middleware import app
bottle.debug()
bottle.run(app=app, server=bottle.AppEngineServer)
