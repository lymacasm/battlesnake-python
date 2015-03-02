from shapes import *
from safety import *

class foods():
	def __init__(self):
		self.head = []
		self.closestFood = []
		self.gBoard = rectangle()
		self.snakes = []
		self.board = []
		
	def calcDistance(self, pos1, pos2):
		xdist = pos2[0] - pos1[0]
		if xdist < 0:
			xdist *= -1
		ydist = pos2[1] - pos1[1]
		if ydist < 0:
			ydist *= -1
		return xdist + ydist	
		
	def findClosestFood(self, food):	
		distances = []
		minIndex = 0
		if not food:
			return self.head
		else:
			distances.append(self.calcDistance(self.head,food[0]))
			for s in range(1,len(food)):
				distances.append(self.calcDistance(self.head,food[s]))
				if distances[s] < distances[minIndex]:
					minIndex = s
			return food[minIndex]	
			
	def initialize(self, Head, data, BoardDim):
		self.head = Head
		self.closestFood = self.findClosestFood(data["food"])
		self.gBoard = BoardDim
		self.snakes = data["snakes"]
		self.board = data["board"]
			
	def chooseFoodDirection(self):
		right = isSafe(self.head, self.board, self.snakes, 'right', self.gBoard)
		left = isSafe(self.head, self.board, self.snakes, 'left', self.gBoard)
		up = isSafe(self.head, self.board, self.snakes, 'up', self.gBoard)
		down = isSafe(self.head, self.board, self.snakes, 'down', self.gBoard)
		xdist = self.closestFood[0] - self.head[0]
		ydist = self.closestFood[1] - self.head[1]
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
			if ( xdist > 0 ) and right and checkCollision(self.head,self.board,self.snakes,'right', self.gBoard):
				return json.dumps({
					'move':'right',
					'taunt':'I checked for collision'
				})
			if ( xdist < 0 ) and left and checkCollision(self.head,self.board,self.snakes,'left', self.gBoard):
				return json.dumps({
					'move':'left',
					'taunt':'I checked for collision'
				})
			if ( ydist > 0 ) and down and checkCollision(self.head,self.board,self.snakes,'down', self.gBoard):
				return json.dumps({
					'move':'down',
					'taunt':'I checked for collision'
				})
			if ( ydist < 0 ) and up and checkCollision(self.head,self.board,self.snakes,'up', self.gBoard):
				return json.dumps({
					'move':'up',
					'taunt':'I checked for collision'
				})
		elif yabs > xabs:
			if ( ydist > 0 ) and down and checkCollision(self.head,self.board,self.snakes,'down', self.gBoard):
				return json.dumps({
					'move':'down',
					'taunt':'I checked for collision'
				})
			if ( ydist < 0 ) and up and checkCollision(self.head,self.board,self.snakes,'up', self.gBoard):
				return json.dumps({
					'move':'up',
					'taunt':'I checked for collision'
				})
			if ( xdist > 0 ) and left and checkCollision(self.head,self.board,self.snakes,'left', self.gBoard):
				return json.dumps({
					'move':'left',
					'taunt':'I checked for collision'
				})
			if ( xdist < 0 ) and right and checkCollision(self.head,self.board,self.snakes,'right', self.gBoard):
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

