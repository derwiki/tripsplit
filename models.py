from google.appengine.ext import db

def gae_breakpoint(self):
	import sys
	for attr in ('stdin', 'stdout', 'stderr'):
		setattr(sys, attr, getattr(sys, '__%s__' % attr))
	import pdb
	pdb.set_trace()

class StandardModel(db.Expando):
	def __str__(self):
		values = ', '.join('%s=\'%s\'' % (key, getattr(self, key)) for key in self.properties().keys())
		return '%s(%s)' % (self.__class__.__name__, values)

class User(StandardModel):
	username = db.StringProperty()
	email = db.StringProperty()
	gae_user = db.UserProperty()

class Trip(StandardModel):
	creator = User()
	name = db.StringProperty()
	description = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)

class Expense(StandardModel):
	payer = User()
	amount = db.FloatProperty()
	description = db.StringProperty()
	notes = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	trip = db.ReferenceProperty(reference_class=Trip)

class Participant(StandardModel):
	user = db.ReferenceProperty(reference_class=User)
	trip = db.ReferenceProperty(reference_class=Trip)


