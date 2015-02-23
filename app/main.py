import bottle
import json

myName = 'flaming-torpedo'
bWidth = 0
bHeight = 0

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
	return

def findSnake(snakes, name):
	for x in range(len(snakes)):
		if snakes[x]["name"] == name:
			return snakes[x]
	return None
	
def calcDistance(pos1, pos2):
	xdist = pos2[0] - pos1[0]
	if xdist < 0:
		xdist *= -1
	ydist = pos2[1] - pos1[1]
	if ydist < 0:
		ydist *= -1
	return xdist + ydist	
		
def findClosestFood(food, head):	
	distances = []
	minIndex = 0
	if not food:
		return head
	else:
		distances.append(calcDistance(head,food[0]))
		for s in range(1,len(food)):
			distances.append(calcDistance(head,food[s]))
			if distances[s] < distances[minIndex]:
				minIndex = s
		return food[minIndex]	

def isSafe(head, board, direction):
	if direction == 'up':
		newPos = [head[1], head[0] - 1]
	elif direction == 'down':
		newPos = [head[1], head[0] + 1]
	elif direction == 'right':
		newPos = [head[1] + 1, head[0]]
	elif direction == 'left':
		newPos = [head[1] - 1, head[0]]
	boardState = board[newPos[0]][newPos[1]]["state"]
	if newPos[0] < 0:
		return False
	if newPos[1] < 0:
		return False
	if newPos[0] >= bWidth:
		return False
	if newPos[1] >= bHeight:
		return False
	if boardState == "body":
		return False
	if boardState == "head":
		return False
	return True
		
def chooseDirection(food,head,board):
	right = isSafe(head,board,'right')
	left = isSafe(head,board,'left')
	up = isSafe(head,board,'up')
	down = isSafe(head,board,'down')
	xdist = food[1] - head[1]
	ydist = food[0] - head[0]
	if xdist >= ydist:
		if ( xdist > 0 ) and right:
			return json.dumps({
				'move':'right',
				'taunt':'I am always right'
			})
		if ( xdist < 0 ) and left:
			return json.dumps({
				'move':'left',
				'taunt':'To the left, to the left'
			})
		if ( ydist > 0 ) and down:
			return json.dumps({
				'move':'down',
				'taunt':'Down we go'
			})
		if ( ydist < 0 ) and up:
			return json.dumps({
				'move':'up',
				'taunt':'Upwards and onwards'
			})
	elif ydist > xdist:
		if ( ydist > 0 ) and down:
			return json.dumps({
				'move':'down',
				'taunt':'Down we go'
			})
		if ( ydist < 0 ) and up:
			return json.dumps({
				'move':'up',
				'taunt':'Upwards and onwards'
			})
		if ( xdist > 0 ) and left:
			return json.dumps({
				'move':'left',
				'taunt':'To the left, to the left'
			})
		if ( xdist < 0 ) and right:
			return json.dumps({
				'move':'right',
				'taunt':'I am always right'
			})
	if down:
		return json.dumps({
				'move':'down',
				'taunt':'Down we go'
			})
	if up:
		return json.dumps({
				'move':'up',
				'taunt':'Upwards and onwards'
			})
	if right:
		return json.dumps({
				'move':'right',
				'taunt':'I am always right'
			})
	return json.dumps({
				'move':'left',
				'taunt':'To the left, to the left'
			})
	
def gotoFood(data):
	board = data["board"]
	mySnake = findSnake(data["snakes"], myName)
	coords = mySnake["coords"]
	food = data["food"]
	for x in range(len(coords)):
		if board[(coords[x][0])][(coords[x][1])]["state"] == "head":
			head = coords[x]
		closestFood = findClosestFood(food,head)
	return chooseDirection(closestFood,head,board)


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
    bWidth = data["width"]
    bHeight = data["height"]

    return json.dumps({
        'name': myName,
        'color': '#ff6600',
        'head_url': 'http://fast-spire-5995.herokuapp.com',
        'taunt': 'Get ready to feel my heat!'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json
	response = gotoFood(data)
	
    return response


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
