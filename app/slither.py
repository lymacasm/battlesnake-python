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
