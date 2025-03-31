import pygame

from pygame.locals import *
import random

import copy

import numpy as np

import functools
import asyncio


def indexOf(lst, val):
	for i in range(len(lst)):
		if lst[i] == val:
			return i





def encode(i):
	return i*30




def generateHamiltonianPath(boardMatrix, curNodeArray, curNum):
	if curNum == len(curNodeArray):
		if boardMatrix[curNodeArray[-1]][0] == 1:
			return [True, curNodeArray]

		else:

			return None

	newNodeLst = [i for i in range(0, len(boardMatrix))]

	random.shuffle(newNodeLst)

	for i in newNodeLst:
		if i not in curNodeArray and boardMatrix[curNodeArray[curNum - 1]][i] == 1:
			testCurNodeArray = curNodeArray.copy()

			testCurNodeArray[curNum] = i

			nextVal = generateHamiltonianPath(boardMatrix, testCurNodeArray, curNum + 1)

			if nextVal != None:
				return nextVal



def generateHamiltonianMatrix(boardSize):
	boardMatrix = list(np.zeros((boardSize * boardSize, boardSize * boardSize)))# [[0]*(boardSize * boardSize)]*(boardSize * boardSize)

	for i in range(boardSize*boardSize):
		if i % boardSize != 0:
			boardMatrix[i][i - 1] = 1

		if i % boardSize != boardSize - 1:
			boardMatrix[i][i + 1] = 1

		if i >= boardSize:
			boardMatrix[i][i - boardSize] = 1

		if i < boardSize * boardSize - boardSize:
			
			boardMatrix[i][i + boardSize] = 1



	return boardMatrix



def generateHamiltonianPathForBoard(boardSize):
	sequence = []

	numbers = np.zeros((boardSize, boardSize))
	for x in range(boardSize):
		for y in range(boardSize):
			# print(boardSize * x + y, x, y)
			numbers[y][x] = boardSize * x + y


	


	for i in range(int(boardSize/2)):
		i = i*2
		for num in range((boardSize * i) + 1, boardSize * (i + 1)):
			sequence.append(num)


		for num in range((boardSize * (i + 2)) - 1, boardSize * (i + 1), -1):
			sequence.append(num)


	for num in range(boardSize * boardSize - boardSize, -1, -boardSize):
		sequence.append(num)


	return sequence





def createApple(playerPositions):

	x = playerPositions[0][0]

	y = playerPositions[0][1]

	while [x, y] in playerPositions:
		x = random.randint(0, 19)
		y = random.randint(0, 19)
	return [x, y]
	# board[y][x] = 'A'

def showPlayer(playerPositions, screen):

	for i in range(len(playerPositions)):
		pygame.draw.rect(screen, (0, 255, 0), (encode(playerPositions[i][0]), encode(playerPositions[i][1]), 30, 30))
	
def getNext(curAvailable, curHead):

	failCount = 0

	curAvailable[curHead[1]][curHead[0]] = 'A'

	# for row in curAvailable:
	# 	print(row)

	# print('\n')
	aCount = 0




	end = True

	for i in curAvailable:
		for j in i:
			if j == 'O':
				end = False

			if j == 'A':
				aCount += 1


	if end:
		return aCount




	




	numUp = 0
	numRight = 0
	numLeft = 0
	numDown = 0

	try:
		if curHead[1] - 1 != -1 and curAvailable[curHead[1] - 1][curHead[0]] == 'O':
			# availableCopy = copy.deepcopy(curAvailable)
			curAvailable[curHead[1] - 1][curHead[0] ] = 'A'
			numUp = getNext(curAvailable, [curHead[0], curHead[1] - 1])
		else:
			numUp = 0
			failCount += 1

	except IndexError:
		failCount += 1

	try:


		if curHead[1] + 1 != 20 and curAvailable[curHead[1] + 1][curHead[0]] == 'O':
			# availableCopy = copy.deepcopy(curAvailable)
			curAvailable[curHead[1] + 1][curHead[0]] = 'A'
			numDown = getNext(curAvailable, [curHead[0], curHead[1] + 1])
		else:
			numDown = 0
			failCount += 1

	except IndexError:
		failCount += 1
		

	try:
		if curHead[0] - 1 != -1 and curAvailable[curHead[1]][curHead[0] - 1] == 'O':
			# availableCopy = copy.deepcopy(curAvailable)
			curAvailable[curHead[1]][curHead[0] - 1] = 'A'
			numRight = getNext(curAvailable, [curHead[0] - 1, curHead[1]])
		else:
			numRight = 0
			failCount += 1

	except IndexError:
		failCount += 1


	try:
		if curHead[0] + 1 != 20 and curAvailable[curHead[1]][curHead[0] + 1] == 'O':
			# availableCopy = copy.deepcopy(curAvailable)
			curAvailable[curHead[1]][curHead[0] + 1] = 'A'
			numLeft = getNext(curAvailable, [curHead[0] + 1, curHead[1]])

		else:
			numLeft = 0
			failCount += 1

	except IndexError:
		failCount += 1

	# if failCount == 4:
	# 	return aCount

	return numRight + numLeft + numDown + numUp


def getAllSquares(playerPositions, boardSize):
	curAvailableUp = []# list(np.zeros((boardSize * boardSize, boardSize * boardSize)))# list(np.zeros((boardSize * boardSize, boardSize * boardSize)))
	curAvailableDown = []# list(np.zeros((boardSize * boardSize, boardSize * boardSize)))
	curAvailableLeft = []# list(np.zeros((boardSize * boardSize, boardSize * boardSize)))
	curAvailableRight = []# list(np.zeros((boardSize * boardSize, boardSize * boardSize)))
	




	for i in range(boardSize):
		append = []
		for j in range(boardSize):
			append.append('O')

		curAvailableUp.append(append)
		curAvailableDown.append(append)
		curAvailableLeft.append(append)
		curAvailableRight.append(append)


	# for y in range(len(curAvailable)):
	# 	for x in range(len(curAvailable[y])):
	# 		print(x, y)
	# 		if [x, y] in playerPositions:
	# 			curAvailable[y][x] == 'X'


	for i in playerPositions:
		curAvailableUp[i[1]][i[0]] = 'X'
		curAvailableDown[i[1]][i[0]] = 'X'
		curAvailableRight[i[1]][i[0]] = 'X'
		curAvailableLeft[i[1]][i[0]] = 'X'


	# for row in curAvailable:
	# 	print(row)

	# print('\n')

	numUp = 0
	numDown = 0
	numLeft = 0
	numRight = 0

	if [playerPositions[0][0], playerPositions[0][1] - 1] not in playerPositions and playerPositions[0][1] - 1 != -1 and curAvailableUp[playerPositions[0][1] - 1][playerPositions[0][0]] == 'O':
		# print("Up")
		numUp = getNext(copy.deepcopy(curAvailableUp), [playerPositions[0][0], playerPositions[0][1] - 1])

	if [playerPositions[0][0], playerPositions[0][1] + 1] not in playerPositions and playerPositions[0][1] + 1 != 20 and curAvailableDown[playerPositions[0][1] + 1][playerPositions[0][0]] == 'O':
		# print("Down")
		numDown = getNext(copy.deepcopy(curAvailableDown), [playerPositions[0][0], playerPositions[0][1] + 1])

	if [playerPositions[0][0] - 1, playerPositions[0][1]] not in playerPositions and playerPositions[0][0] - 1 != -1 and curAvailableRight[playerPositions[0][1]][playerPositions[0][0] - 1] == 'O':
		# print("Left")
		numRight = getNext(copy.deepcopy(curAvailableLeft), [playerPositions[0][0] - 1, playerPositions[0][1]])

	if [playerPositions[0][0] + 1, playerPositions[0][1]] not in playerPositions and playerPositions[0][0] + 1 != 20 and curAvailableLeft[playerPositions[0][1]][playerPositions[0][0] + 1] == 'O':
		# print("Right")
		numLeft = getNext(copy.deepcopy(curAvailableRight), [playerPositions[0][0] + 1, playerPositions[0][1]])

	return [numUp, numDown, numLeft, numRight]



async def main():

	pygame.init()

	screen = pygame.display.set_mode((600, 600))

	pygame.display.set_caption("Snake AI")


	global red, green

	playerPositions = [[15, 15], [15, 16], [15, 17]]

	direction = 'Up'

	running = True

	applePostion = createApple(playerPositions)

	clock = pygame.time.Clock()

	while running:

		clock.tick(10)


		screen.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == K_UP:
					if direction == 'Right' or direction == 'Left':
						# turns.append([[playerX[0], playerY[0]], 2])
						direction = 'Up'
				if event.key == K_DOWN:
					if direction == 'Right' or direction == 'Left':
						# turns.append([[playerX[0], playerY[0]], 4])
						direction = 'Down'
				if event.key == K_RIGHT:
					if direction == 'Down' or direction == 'Up':
						# turns.append([[playerX[0], playerY[0]], 1])
						direction = 'Right'
				if event.key == K_LEFT:
					if direction == 'Down' or direction == 'Up':
						# turns.append([[playerX[0], playerY[0]], 3])
						direction = 'Left'

		# for turn in turns:
		# 	for location in range(len(playerX)):
		# 		if turn[0][0] == playerX[location] and turn[0][1] == playerY[location]:
		# 			directionBySquare[location] = turn[1]

		# for location in range(len(playerX)):
		# 	if directionBySquare[location] == 2:
		# 		playerY[location] -= 1
		# 	if directionBySquare[location] == 4:
		# 		playerY[location] += 1
		# 	if directionBySquare[location] == 1:
		# 		playerX[location] += 1
		# 	if directionBySquare[location] == 3:
		# 		playerX[location] -= 1

		# print(applePostion, playerPositions[0])

		
			# print(appleX, appleY)

		# applePostion = createApple()








		if direction == 'Up':
			playerPositions.insert(0, [playerPositions[0][0], playerPositions[0][1] - 1])
		elif direction == 'Down':
			playerPositions.insert(0, [playerPositions[0][0], playerPositions[0][1] + 1])

		elif direction == 'Left':
			playerPositions.insert(0, [playerPositions[0][0] - 1, playerPositions[0][1]])

		elif direction == 'Right':
			playerPositions.insert(0, [playerPositions[0][0] + 1, playerPositions[0][1]])


		if playerPositions[0] == applePostion:
			applePostion = createApple(playerPositions)

		else:
			playerPositions.pop(-1)


		if playerPositions[0] in playerPositions[1:] or playerPositions[0][0] in [-1, 20] or playerPositions[0][1] in [-1, 20]:
			break




		showPlayer(playerPositions, screen)
		pygame.draw.rect(screen, (255,0,0), (encode(applePostion[0]) + 1, encode(applePostion[1]) + 1, 29, 29))
		# pygame.time.wait(100)
		pygame.display.update()
		await asyncio.sleep(0)

asyncio.run(main())
