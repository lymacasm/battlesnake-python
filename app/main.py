import bottle
import json


@bottle.get('/')
def index():
    return """
        <a href="https://github.com/lymacasm/battlesnake-python">
            battlesnake-python
        </a>
    """


@bottle.post('/start')
def start():
    data = bottle.request.json

    return json.dumps({
        'name': 'battlesnake-python',
        'color': '#ff6600',
        'head_url': 'http://fast-spire-5995.herokuapp.com',
        'taunt': 'battlesnake-python!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json
    down = 'down'
    
    return json.dumps({
        'move': down,
        'taunt': 'battlesnake-python!'
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
