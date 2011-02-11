import sys
sys.path.insert(0, 'bottle')

import bottle
from bottle import route

@route('/')
def index():
    return 'index'


bottle.debug()
bottle.run(server=bottle.AppEngineServer)
