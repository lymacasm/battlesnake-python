from shapes import *
from safety import *

class spacing():
	def __init__(self):
		self.board = []
		self.snakes = []
		self.head = []
		self.gBoard = rectangle()
		
	def initialize(self, data, Head, boardsize):
		self.board = data["board"]
		self.snakes = data["snakes"]
		self.head = Head
		self.gBoard = boardsize

	def calcArea(self, currentLoc, initDirection, direction):
	
		#Base Case
		if currentLoc[0] < 0 or currentLoc[1] < 0:
			return 0
		if currentLoc[0] >= self.gBoard.Width or currentLoc[1] >= self.gBoard.Height:
			return 0
		boardTyle = self.board[currentLoc[0]][currentLoc[1]]
		if boardTyle["state"] == "head" or boardTyle["state"] == "body":
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
				partialArea += calcArea(left, 'up', 'left') #Go left
				partialArea += calcArea(right, 'up', 'right') #Go right
				partialArea += calcArea(up, 'up', 'up') #Go up
				return partialArea
			elif direction == 'right':
				partialArea += calcArea(right, 'up', 'right') #Go right
				return partialArea
			elif direction == 'left':
				partialArea += calcArea(left, 'up', 'left') #Go left
				return partialArea
			
		elif initDirection == 'down':
			if direction == 'down':
				partialArea += calcArea(left, 'down', 'left') #Go left
				partialArea += calcArea(right, 'down', 'right') #Go right
				partialArea += calcArea(down, 'down', 'down') #Go down
				return partialArea
			elif direction == 'right':
				partialArea += calcArea(right, 'down', 'right') #Go right
				return partialArea
			elif direction == 'left':
				partialArea += calcArea(left, 'down', 'left') #Go left
				return partialArea
			
		elif initDirection == 'right':
			if direction == 'right':
				partialArea += calcArea(up, 'right', 'up') #Go up
				partialArea += calcArea(down, 'right', 'down') #Go down
				partialArea += calcArea(right, 'right', 'right') #Go right
				return partialArea
			elif direction == 'up':
				partialArea += calcArea(up, 'right', 'up') #Go up
				return partialArea
			elif direction == 'down':
				partialArea += calcArea(down, 'right', 'down') #Go down
				return partialArea
			
		elif initDirection == 'left':
			if direction == 'left':
				partialArea += calcArea(up, 'left', 'up') #Go up
				partialArea += calcArea(down, 'left', 'down') #Go down
				partialArea += calcArea(left, 'left', 'left') #Go left
				return partialArea
			elif direction == 'up':
				partialArea += calcArea(up, 'left', 'up') #Go up
				return partialArea
			elif direction == 'down':
				partialArea += calcArea(down, 'left', 'down') #Go down
				return partialArea
	
		else: 
			return -100000 #in case we get invalid input

	def calculateArea(self, start, direction):
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
		return calcArea(pos, direction, direction)
		
	def chooseSpaceDirection(self):
	
		#Check direction fields
		rightSpace = calculateArea(self.board, self.head, 'right', gBoard)
		leftSpace = calculateArea(self.board, self.head, 'left', gBoard)
		upSpace = calculateArea(self.board, self.head, 'up', gBoard)
		downSpace = calculateArea(self.board, self.head, 'down', gBoard)
	
		rightCol = checkCollision(self.head, self.board, self.snakes, 'right', gBoard)
		leftCol = checkCollision(self.head, self.board, self.snakes, 'left', gBoard)
		upCol = checkCollision(self.head, self.board, self.snakes, 'up', gBoard)
		downCol = checkCollision(self.head, self.board, self.snakes, 'down', gBoard)
	
		rightSafe = isSafe(self.head, self.board, self.snakes, 'right', gBoard)
		leftSafe = isSafe(self.head, self.board, self.snakes, 'left', gBoard)
		upSafe = isSafe(self.head, self.board, self.snakes, 'up', gBoard)
		downSafe = isSafe(self.head, self.board, self.snakes, 'down', gBoard)
	
		right = rightSafe and rightCol
		left = leftSafe and leftCol
		up = upSafe and upCol
		down = downSafe and downCol
	
		#Local variables
		maximumValue = max(rightSpace, leftSpace, upSpace, downSpace)
	
		#Logic
		while True:
			if maximumValue <= 0:
				if right:
					return json.dumps({
						'move':'right',
						'taunt':'Right default'
					})
				elif left:
					return json.dumps({
						'move':'left',
						'taunt':'Left default'
					})
				elif up:
					return json.dumps({
						'move':'up',
						'taunt':'Up default'
					})
				elif down:
					return json.dumps({
						'move':'down',
						'taunt':'Down default'
					})
				elif rightSafe:
					return json.dumps({
						'move':'right',
						'taunt':'Right is safe default'
					})
			
				elif leftSafe:
					return json.dumps({
						'move':'left',
						'taunt':'Left is safe default'
					})
				elif upSafe:
					return json.dumps({
						'move':'up',
						'taunt':'Up is safe default'
					})
				else:
					return json.dumps({
						'move':'down',
						'taunt':'Down by default'
					})
			elif maximumValue == rightSpace:
				if right:
					return json.dumps({
						'move':'right',
						'taunt':'You\'re all a bunch of pudding brains'
					})
				else:
					rightSpace = 0
					maximumValue = max(rightSpace, leftSpace, upSpace, downSpace)
			elif maximumValue == leftSpace:
				if left:
					return json.dumps({
						'move':'left',
						'taunt':'One of us is lying about our basic programming'
					})
				else:
					leftSpace = 0
					maximumValue = max(rightSpace, leftSpace, upSpace, downSpace)
			elif maximumValue == upSpace:
				if up:
					return json.dumps({
						'move':'up',
						'taunt':'Don\'t be lasagna!'
					})
				else:
					upSpace = 0
					maximumValue = max(rightSpace, leftSpace, upSpace, downSpace)
			elif maximumValue == downSpace:
				if down:
					return json.dumps({
						'move':'down',
						'taunt':'I\'ll hit you with my shoe'
					})
	
