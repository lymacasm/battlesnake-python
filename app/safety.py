from slither import *
from shapes import *

def checkCollision(head, board, snakes, direction, gBoard):
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
	mySnakeSize = sizeOfSnake(snakes,gBoard.Name)

	if boardRight != None and boardRight["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardRight["snake"]):
		return False
	if boardLeft != None and boardLeft["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardLeft["snake"]):
		return False
	if boardUp != None and boardUp["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardUp["snake"]):
		return False
	if boardDown != None and boardDown["state"] == "head" and mySnakeSize <= sizeOfSnake(snakes,boardDown["snake"]):
		return False
	return True

def isSafe(head, board, snakes, direction, gBoard):
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
		return False
	return True
