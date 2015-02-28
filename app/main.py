import bottle
import json

class rectangle():
	def __init__(self):
		self.Width = 0
		self.Height = 0
	def initialize(self, width, height):
		self.Width = width
		self.Height = height

gBoard = rectangle()
myName = 'flaming-torpedo'

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

def calcArea(board, currentLoc, initDirection, direction):
	print ""
	print "calcArea"
	print "currentLoc: ", currentLoc
	print "initDirection: ", initDirection
	print "direction: ", direction
	
	#Base Case
	if currentLoc[0] < 0 or currentLoc[1] < 0:
		print "Base Case Exit: 0 Walls"
		return 0
	if currentLoc[0] >= gBoard.Width or currentLoc[1] >= gBoard.Height:
		print "Base Case Exit: End Walls"
		return 0
	boardTyle = board[currentLoc[0]][currentLoc[1]]
	if boardTyle["state"] == "head" or boardTyle["state"] == "body":
		print "Base Case: Snake"
		return 0
	
	#Local Variables
	up = [currentLoc[0], currentLoc[1] - 1]
	down = [currentLoc[0], currentLoc[1] + 1]
	right = [currentLoc[0] + 1, currentLoc[1]]
	left = [currentLoc[0] - 1, currentLoc[1]]
	partialArea = 1
	
	#Logic / Recursive Calls
	if initDirection == 'up':
		if direction == 'up':
			partialArea += calcArea(board, left, 'up', 'left', partialArea) #Go left
			partialArea += calcArea(board, right, 'up', 'right', partialArea) #Go right
			partialArea += calcArea(board, up, 'up', 'up', partialArea) #Go up
			return partialArea
		elif direction == 'right':
			partialArea += calcArea(board, right, 'up', 'right', partialArea) #Go right
			return partialArea
		elif direction == 'left':
			partialArea += calcArea(board, left, 'up', 'left', partialArea) #Go left
			return partialArea
			
	elif initDirection == 'down':
		if direction == 'down':
			partialArea += calcArea(board, left, 'down', 'left', partialArea) #Go left
			partialArea += calcArea(board, right, 'down', 'right', partialArea) #Go right
			partialArea += calcArea(board, down, 'down', 'down', partialArea) #Go down
			return partialArea
		elif direction == 'right':
			partialArea += calcArea(board, right, 'down', 'right', partialArea) #Go right
			return partialArea
		elif direction == 'left':
			partialArea += calcArea(board, left, 'down', 'left', partialArea) #Go left
			return partialArea
			
	elif initDirection == 'right':
		if direction == 'right':
			partialArea += calcArea(board, up, 'right', 'up', partialArea) #Go up
			partialArea += calcArea(board, down, 'right', 'down', partialArea) #Go down
			partialArea += calcArea(board, right, 'right', 'right', partialArea) #Go right
			return partialArea
		elif direction == 'up':
			partialArea += calcArea(board, up, 'right', 'up', partialArea) #Go up
			return partialArea
		elif direction == 'down':
			partialArea += calcArea(board, down, 'right', 'down', partialArea) #Go down
			return partialArea
			
	elif initDirection == 'left':
		if direction == 'left':
			partialArea += calcArea(board, up, 'left', 'up', partialArea) #Go up
			partialArea += calcArea(board, down, 'left', 'down', partialArea) #Go down
			partialArea += calcArea(board, left, 'left', 'left', partialArea) #Go left
			return partialArea
		elif direction == 'up':
			partialArea += calcArea(board, up, 'left', 'up', partialArea) #Go up
			return partialArea
		elif direction == 'down':
			partialArea += calcArea(board, down, 'left', 'down', partialArea) #Go down
			return partialArea
	
	else: 
		return -100000 #in case we get invalid input

def calculateArea(board, start, direction):
	print ""
	print 'calculateArea'
	print 'start: ', start
	if direction == 'up':
		pos = [start[0], start[1] - 1]
		print 'uppos: ', pos
	elif direction == 'down':
		pos = [start[0], start[1] + 1]
		print 'downpos: ', pos
	elif direction == 'right':
		pos = [start[0] + 1, start[1]]
		print 'rightpos: ', pos
	elif direction == 'left':
		pos = [start[0] - 1, start[1]]
		print 'leftpos: ', pos
	return calcArea(board, pos, direction, direction)

def findSnake(snakes, name):
	for x in range(len(snakes)):
		if snakes[x]["name"] == name:
			return snakes[x]
	return None
	
def sizeOfSnake(snakes, name):
	ThisSnake = findSnake(snakes, name)
	if ThisSnake == None:
		return 0
	size = len(ThisSnake["coords"])
	return size

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

def checkCollision(head, board, snakes, direction):
	if direction == 'up':
		right = [head[0] + 1, head[1] - 1]
		left = [head[0] - 1, head[1] - 1]
		up = [head[0], head[1] - 2]
		down = [-10,-10]
	elif direction == 'down':
		right = [head[0] + 1, head[1] + 1]
		left = [head[0] - 1, head[1] + 1]
		up = [-10,-10]
		down = [head[0], head[1] + 2]
	elif direction == 'right':
		right = [head[0] + 2, head[1]]
		left = [-10,-10]
		up = [head[0] + 1, head[1] - 1]
		down = [head[0] + 1, head[1] + 1]
	elif direction == 'left':
		right = [-10,-10]
		left = [head[0] - 2, head[1]]
		up = [head[0] - 1, head[1] - 1]
		down = [head[0] - 1, head[1] + 1]
	print ""
	print "checkCollision"
	print "direction: ", direction
	print "head: ", head
	print "up: ", up
	print "down: ", down
	print "right: ", right
	print "left: ", left
	if right[0] < 0 or right[1] < 0 or right[0] >= gBoard.Width or right[1] >= gBoard.Height:
		boardRight = None
	else:
		boardRight = board[right[0]][right[1]]
	if left[0] < 0 or left[1] < 0 or left[0] >= gBoard.Width or left[1] >= gBoard.Height:
		boardLeft = None
	else:
		boardLeft = board[left[0]][left[1]]
	if up[0] < 0 or up[1] < 0 or up[0] >= gBoard.Width or up[1] >= gBoard.Height:
		boardUp = None
	else:
		boardUp = board[up[0]][up[1]]
	if down[0] < 0 or down[1] < 0 or down[0] >= gBoard.Width or down[1] >= gBoard.Height:
		boardDown = None
	else:
		boardDown = board[down[0]][down[1]]
	mySnakeSize = sizeOfSnake(snakes,myName)
	print "boardRightState: ", boardRight
	print "boardLeftState: ", boardLeft
	print "boradUpState: ", boardUp
	print "boardDownState: ", boardDown
	if boardRight != None and boardRight["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardRight["snake"]):
		print False
		return False
	if boardLeft != None and boardLeft["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardLeft["snake"]):
		print False
		return False
	if boardUp != None and boardUp["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardUp["snake"]):
		print False
		return False
	if boardDown != None and boardDown["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardDown["snake"]):
		print False
		return False
	print True
	return True

def isSafe(head, board, snakes, direction):
	if direction == 'up':
		newPos = [head[0], head[1] - 1]
	elif direction == 'down':
		newPos = [head[0], head[1] + 1]
	elif direction == 'right':
		newPos = [head[0] + 1, head[1]]
	elif direction == 'left':
		newPos = [head[0] - 1, head[1]]
	if newPos[0] < 0:
		return False
	if newPos[1] < 0:
		return False
	if newPos[0] >= gBoard.Width:
		return False
	if newPos[1] >= gBoard.Height:
		return False
	boardState = board[newPos[0]][newPos[1]]
	if boardState["state"] == "body":
		return False
	if boardState["state"] == "head":
		print "isSafe: False"
		return False
	print "isSafe: True"
	return True
	
def chooseDirection(food,head,snakes,board):
	right = isSafe(head,board,snakes,'right')
	left = isSafe(head,board,snakes,'left')
	up = isSafe(head,board,snakes,'up')
	down = isSafe(head,board,snakes,'down')
	xdist = food[0] - head[0]
	ydist = food[1] - head[1]
	xabs = 0
	yabs = 0
	if xdist < 0:
		xabs = -xdist
	else:
		xabs = xdist
	if ydist < 0:
		yabs = -ydist
	else:
		yabs = ydist
	if xabs >= yabs:
		if ( xdist > 0 ) and right and checkCollision(head,board,snakes,'right'):
			return json.dumps({
				'move':'right',
				'taunt':'I checked for collision'
			})
		if ( xdist < 0 ) and left and checkCollision(head,board,snakes,'left'):
			return json.dumps({
				'move':'left',
				'taunt':'I checked for collision'
			})
		if ( ydist > 0 ) and down and checkCollision(head,board,snakes,'down'):
			return json.dumps({
				'move':'down',
				'taunt':'I checked for collision'
			})
		if ( ydist < 0 ) and up and checkCollision(head,board,snakes,'up'):
			return json.dumps({
				'move':'up',
				'taunt':'I checked for collision'
			})
	elif yabs > xabs:
		if ( ydist > 0 ) and down and checkCollision(head,board,snakes,'down'):
			return json.dumps({
				'move':'down',
				'taunt':'I checked for collision'
			})
		if ( ydist < 0 ) and up and checkCollision(head,board,snakes,'up'):
			return json.dumps({
				'move':'up',
				'taunt':'I checked for collision'
			})
		if ( xdist > 0 ) and left and checkCollision(head,board,snakes,'left'):
			return json.dumps({
				'move':'left',
				'taunt':'I checked for collision'
			})
		if ( xdist < 0 ) and right and checkCollision(head,board,snakes,'right'):
			return json.dumps({
				'move':'right',
				'taunt':'I checked for collision'
			})
	if down:
		return json.dumps({
				'move':'down',
				'taunt':'Down default'
			})
	if up:
		return json.dumps({
				'move':'up',
				'taunt':'Up default'
			})
	if right:
		return json.dumps({
				'move':'right',
				'taunt':'Right default'
			})
	return json.dumps({
				'move':'left',
				'taunt':'Left Default'
			})
			
def findHead(data):
	board = data["board"]
	mySnake = findSnake(data["snakes"], myName)
	coords = mySnake["coords"]
	head = None
	for x in range(len(coords)):
		if board[(coords[x][0])][(coords[x][1])]["state"] == "head":
			head = coords[x]
	return head
	
def gotoFood(data):
	board = data["board"]
	food = data["food"]
	head = findHead(data)
	closestFood = findClosestFood(food, head)
	return chooseDirection(closestFood, head, data["snakes"], board)

def gotoSpace(data):
	board = data["board"]
	head = findHead(data)
	print calculateArea(board, head, 'left')
	return json.dumps({
				'move':'down',
				'taunt':'I\'m the smart one, you\'re the potato one'
			})

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
    gBoard.initialize(data["width"], data["height"])

    return json.dumps({
        'name': myName,
        'color': '#ff6600',
        'head_url': 'http://img1.wikia.nocookie.net/__cb20131126020959/tardis/images/4/44/EyesOfTwelve.jpg',
        'taunt': 'These are attack eyebrows'
    })


@bottle.post('/move')
def move():
    data = bottle.request.json
    gBoard.initialize(len(data["board"]),len(data["board"][0]))
    
    response = gotoSpace(data)
	
    return response


@bottle.post('/end')
def end():
    data = bottle.request.json

    return json.dumps({})


# Expose WSGI app
application = bottle.default_app()
