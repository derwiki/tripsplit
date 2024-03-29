import json
import logging
import traceback

import bottle
from bottle import request

import models

log = logging.getLogger('servlet')
log.setLevel(logging.DEBUG)

def data_from_post(*keys):
    return dict((key, request.POST.get(key)) for key in keys)

def ajax(*args, **kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                log.debug('Calling %s via AJAX' % func.__name__)
                res = func(*args, **kwargs)
                res.setdefault('success', True)
                json_res = json.dumps(res)
                log.debug('Finished %s, returning %s' % (func.__name__, json_res))
                return json_res
            except Exception, e:
                log.error('*** Caught Exception in AJAX call ***')
                log.error(traceback.format_exc())
                log.error(e)
                json_res = json.dumps(dict(sucess=False, error=str(e)))
                log.error('*** Returning %s ***' % json_res)
                return json_res
        return wrapper
    return decorator

#TODO we need transactional integrity -- if the method crashes after the put()
# the JS handler might crash but the back end has been reflected. Can we
# either defer the put() or do something like a rollback() ?
@ajax
@bottle.route('/add_expense', method='POST')
def add_expense():
    data = data_from_post('amount', 'description', 'notes', 'trip', 'payer')
    data['amount'] = float(data['amount'])
    log.debug('add_expense data: %s' % data)
    data['trip'] = models.Trip.get_by_id(int(data['trip']))
    data['payer'] = models.User.get_by_id(int(data['payer']))
    log.debug('data: %s' % data)
    expense = models.Expense(**data)
    expense.put()
    log.debug('expense: %s' % expense)
    log.debug('user: %s' % request.user)
    log.debug('request: %s' % request)
    trip = data['trip']
    return dict(
        success=True,
        trip=trip.key().id(),
        created=expense.created.strftime('%Y-%m-%d'),
        expense_id=expense.key().id(),
        amount=data.pop('amount'),
        description=data.pop('description'),
        payer=data.pop('payer').name
    )

@ajax
@bottle.route('/add_participant', method='POST')
def add_participant():
    user_id = request.POST.get('user')
    trip_id = request.POST.get('trip')
    name = request.POST.get('name')
    profile_photo_url = request.POST.get('profile_photo_url')

    log.debug('add_participant, user_id:trip_id::%s:%s' % (user_id, trip_id))
    user = models.User.get_by_id(int(user_id))
    if not user:
        user = models.User(facebook_user_id=int(user_id), name=name, facebook_profile_photo_url=profile_photo_url)
        user.put()

    trip = models.Trip.get_by_id(int(trip_id))
    log.debug('add_participant, user:trip::%s:%s' % (user, trip))
    #TODO enforce uniqueness constraint
    already_participant = models.Participant.all().filter('trip =', trip).filter('user =', user)
    if already_participant.fetch(1):
        return dict(success=False, error='%s is already participating on %s' % (user, trip))
    data = dict(user=user, trip=trip)
    log.debug('add_participant, data: %s' % data)
    participant = models.Participant(**data)
    participant.put()
    return dict(name=name, user_id=int(user_id), participant_id=participant.key().id(), facebook_profile_photo_url=profile_photo_url, success=True)

@ajax
@bottle.route('/remove_participant', method='POST')
def remove_participant():
    participant_id = request.POST.get('participant');
    participant = models.Participant.get_by_id(int(participant_id))
    user_id = participant.user.key().id()
    user_name = participant.user.username
    participant.delete()
    return dict(success=True, user_id=user_id, username=user_name)

@ajax
@bottle.route('/remove_expense', method='POST')
def remove_expense():
    expense_id = request.POST.get('expense');
    expense = models.Expense.get_by_id(int(expense_id))
    expense.delete()
    return dict(success=True)

@ajax
@bottle.route('/add_trip', method='POST')
def add_trip():
    data = data_from_post('tripname', 'description', 'notes')
    data['creator'] = models.User.get_by_id(request.user.key().id())
    data['name'] = data.pop('tripname')
    log.info('add_trip: %s' % data)
    trip = models.Trip(**data)
    trip.put()
    log.info("trip_id: %s" % trip.key().id())
    return dict(trip_id=trip.key().id(), success=True)

@ajax
@bottle.route('/json/users')
def json_users():
    return dict((
        user.email, {'id': user.key().id(), 'username': user.username}
    ) for user in models.User.all() if user.email is not None)

@ajax
@bottle.validate(trip_id=int)
@bottle.route('/settle_up/:trip_id', method='GET')
def settle_up(trip_id):
    trip = models.Trip.get_by_id(int(trip_id))
    # this is a bit of a hack to get around lazy loading
    all_expenses = models.Expense.all().filter('trip =', trip)
    all_participants = [p for p in models.Participant.all().filter('trip =', trip)]
    names = dict((p.user.facebook_user_id, p.user.name) for p in all_participants)

    total_expense = sum(expense.amount for expense in all_expenses)
    each_share = total_expense / len(all_participants)

    owes = dict((participant.user.facebook_user_id, each_share) for participant in all_participants)
    for expense in all_expenses:
       owes[expense.payer.facebook_user_id] -= expense.amount

    sorted_owes = [dict(uid=uid, amount=int(amount*100)) for uid, amount in sorted(owes.items(), key=lambda x: x[1], reverse=True)]

    txns = []
    def add_txn(message):
        txns.append(message)
        log.info(message)

    def format_amount(amount):
        return '$%.2f' % (int(amount) / 100.0)

    add_txn('Total trip cost $%s, each shares $%s' % (total_expense, each_share))
    most_indebted = -1
    for unsettled in sorted_owes:
        add_txn('%s owes %s' % (names[unsettled['uid']], format_amount(unsettled['amount'])))
        while unsettled['amount'] > 0:
            receiver = sorted_owes[most_indebted]
            if unsettled['amount'] >= receiver['amount'] * -1:
                transfer_amount = receiver['amount'] * -1
            else:
                transfer_amount = unsettled['amount']
            receiver['amount'] += transfer_amount
            unsettled['amount'] -= transfer_amount
            add_txn('%(payer)s paid %(amount)s to %(recipient)s who is still owed %(outstanding_balance)s' % dict(
                payer=names[unsettled['uid']],
                amount=format_amount(transfer_amount),
                recipient=names[sorted_owes[most_indebted]['uid']],
                outstanding_balance=format_amount(sorted_owes[most_indebted]['amount'] * -1))
            )
            if receiver['amount'] == 0:
                add_txn('%s has been paid back in full' % names[receiver['uid']])
                most_indebted -= 1 # most indebted is paid off

    return json.dumps(txns)

