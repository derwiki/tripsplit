import bottle
app = bottle.app()

# Tripsplit middleware
import models

def TripsplitMiddleware(app):
    def wrapper(environ, start_response):
        request = bottle.request
        
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


# Session middleware        
from beaker.middleware import SessionMiddleware

app = SessionMiddleware(app, {
        'session.auto': True,
        'session.type': 'ext:google',
        })
