import bottle
import json

def spin(data):
	check = data["turn"] % 4
	if check == 0:
		return 'up'
	elif check == 1:
		return 'right'
	elif check == 2:
		return 'down'
	elif check == 3:
		return 'left'

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
    
    return json.dumps({
        'move': spin(data),
        'taunt': 'battlesnake-python!'
    })


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
