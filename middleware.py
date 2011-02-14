from lib import bottle
app = bottle.app()


# Tripsplit middleware
def TripsplitMiddleware(app):
    def wrapper(environ, start_response):
        # Add session
        bottle.request.session = environ['beaker.session']
        return app(environ, start_response)
    return wrapper
app = TripsplitMiddleware(app)


# Session middleware        
from lib.beaker.middleware import SessionMiddleware

app = SessionMiddleware(app, {
        'session.auto': True,
        'session.type': 'ext:google',
        })
