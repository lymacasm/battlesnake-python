import bottle
import json
from shapes import *
from space import *
from slither import *
from food import *

gBoard = rectangle()
gSpace = spacing()
myName = 'the doctor'
hungerPoint = 20
sizePoint = 10
			
def findHead(data):
	board = data["board"]
	mySnake = findSnake(data["snakes"], gBoard.Name)
	coords = mySnake["coords"]
	head = None
	for x in range(len(coords)):
		if board[(coords[x][0])][(coords[x][1])]["state"] == "head":
			head = coords[x]
	return head
	
def gotoFood(data):
	foodClass = foods()
	foodClass.initialize(findHead(data), data["food"], gBoard, data["snakes"], data["board"])
	return foodClass.chooseFoodDirection()

def gotoSpace(data):
	spaceClass = spacing()
	spaceClass.initialize(data, findHead(data), gBoard)
	return spaceClass.chooseSpaceDirection()

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
        'name': myName,
        'color': '#ff6600',
        'head_url': 'http://img1.wikia.nocookie.net/__cb20131126020959/tardis/images/4/44/EyesOfTwelve.jpg',
        'taunt': 'These are attack eyebrows'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json
    gBoard.initialize(len(data["board"]),len(data["board"][0]), myName)
    
    response = gotoFood(data)
	
    return response


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
