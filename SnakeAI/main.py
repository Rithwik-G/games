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



async def mainAI():

	pygame.init()

	screen = pygame.display.set_mode((600, 600))

	pygame.display.set_caption("Snake AI")


	global red, green
	red = (255, 0, 0)

	green = (0, 255, 255)

	moves = 0

	lastResort = []

	playerPositions = [[15, 15], [15, 16], [15, 17]]

	playerHeadNum = (playerPositions[0][0]) * 20 + playerPositions[0][1]

	moveNums = [((playerPositions[0][0] + 1) * 20) + playerPositions[0][1], ((playerPositions[0][0] - 1) * 20) + playerPositions[0][1], ((playerPositions[0][0]) * 20) + (playerPositions[0][1] + 1), ((playerPositions[0][0]) * 20) + (playerPositions[0][1] - 1)]

	nextPath = None

	path = generateHamiltonianPathForBoard(20)

	pathInd = 0

	for i in range(len(path)):
		if path[i] == ((playerPositions[0][0] + 1) * 20) + playerPositions[0][1]:
			pathInd = i + 1
			break


	# print(path)

	direction = 'Up'

	running = True

	applePostion = createApple(playerPositions)

	applePosNum = (20 * applePostion[0]) + applePostion[1]

	applePathInd = indexOf(path, applePosNum)


	playerHeadInd = indexOf(path, playerHeadNum)





	clock = pygame.time.Clock()

	while running:

	
		clock.tick(60)


	

		playerHeadNum = (playerPositions[0][0]) * 20 + playerPositions[0][1]

		playerHeadInd = indexOf(path, playerHeadNum)
		for i in range(len(path)):
			if path[i] == ((playerPositions[0][0]) * 20) + playerPositions[0][1]:
				pathInd = i
				break




		# squares = [1000, 1000, 10000, 10000]# getAllSquares(playerPositions, 20)

		# print(squares)

		moveNums = []# [((playerPositions[0][0] + 1) * 20) + playerPositions[0][1], ((playerPositions[0][0] - 1) * 20) + playerPositions[0][1], ((playerPositions[0][0]) * 20) + (playerPositions[0][1] + 1), ((playerPositions[0][0]) * 20) + (playerPositions[0][1] - 1)]

		if not playerHeadNum % 20 == 0:

			# if not [(playerHeadNum - 1) // 20, (playerHeadNum - 1) % 20] in playerPositions:
			# 	lastResort.append(playerHeadNum - 1)
			

			# 	if squares[0] >= ((400 - len(playerPositions)) * 1)/3:
			moveNums.append(playerHeadNum - 1)


		if not playerHeadNum % 20 == 19:
			# if not [(playerHeadNum + 1) // 20, (playerHeadNum + 1) % 20] in playerPositions:
			# 	lastResort.append(playerHeadNum + 1)
			# 	if squares[1] >= ((400 - len(playerPositions)) * 1)/3:
			moveNums.append(playerHeadNum + 1)

		if playerHeadNum >= 20:
			# if not [(playerHeadNum - 20) // 20, (playerHeadNum - 20) % 20] in playerPositions:
			# 	lastResort.append(playerHeadNum - 20)
			# 	if squares[2] >= ((400 - len(playerPositions)) * 1)/3:
			moveNums.append(playerHeadNum - 20)

		if playerHeadNum < 20 * 20 - 20:
			# if not [(playerHeadNum + 20) // 20, (playerHeadNum + 20) % 20] in playerPositions:
			# 	lastResort.append(playerHeadNum + 20)
			# 	if squares[3] >= ((400 - len(playerPositions)) * 1)/3:
				
			moveNums.append(playerHeadNum + 20)



		 #lastResort = copy.deepcopy(moveNums)

		# print(lastResort)

		# if forward:
		# for i in moveNums:
		# 	if indexOf(path, i) < playerHeadInd:
		# 		moveNums.remove(i)

		# else:
		# 	for i in moveNums:
		# 		if indexOf(path, i) > playerHeadInd:
		# 			moveNums.remove(i)


		

			



		# for i in moveNums:
		# 	pygame.draw.rect(screen, green, (encode(i // 20),  encode(i % 20), 29, 29))
		

		# if (len(playerPositions) > 375):
		pygame.display.update()


		screen.fill((0,0,0))

		# print(moveNums)

	

		# pathInd += 1



		pathInd = pathInd%400

		if playerPositions[0] in playerPositions[1:]:
			print('himself')
			print(playerPositions[0], playerPositions[1:])
			# print("First")
			break

		elif playerPositions[0][0] in [-1, 20] or playerPositions[0][1] in [-1, 20]:
			print("Wall")
			break

		

		# for i in range(len(path)):
		# 	if path[i] == playerHeadPathNum:
		# 		print(i)
		# 		# print(path[i], path[i + 1])
		# 		if i == len(path) - 1:
		# 			# print(i)
		# 			i = -1



				# newHead = [path[i + 1] // 20,  path[i + 1] % 20]
		

		# if [path[(pathInd + 1) % 400] // 20, path[(pathInd + 1) % 400] % 20] not in playerPositions: # forward
		curBest = [path[(pathInd + 1) % 400], 1]

		# else:
		# 	if [path[pathInd - 1] // 20, path[pathInd - 1] % 20] not in playerPositions:
		# 		curBest = [path[pathInd - 1], 1]

		# 	else:
		# 		if [path[(pathInd + 1) % 400] // 20, path[(pathInd + 1) % 400] % 20] not in playerPositions:

		# 			curBest = [path[(pathInd + 1) % 400], float('-inf')]

		# 		else:
		# 			curBest = [None, float('-inf')]

		# if applePathInd > pathInd and [path[(pathInd + 1) % 400] // 20, path[(pathInd + 1) % 400] % 20] not in playerPositions and path[(pathInd + 1) % 400] not in playerHistory: # and [path[pathInd + 1] // 20,  path[pathInd + 1] % 20] not in applePosTaken: # and [path[pathInd + 1] // 20, path[pathInd + 1] % 20] not in playerPositions:
		# 	print([path[(pathInd + 1) % 400] // 20, path[(pathInd + 1) % 400] % 400], playerPositions)
		# 	curBest = [path[(pathInd + 1) % 400], 1]

		# else:
		# 	if (400 - pathInd) + applePathInd > applePathInd - pathInd and [path[pathInd - 1] // 20, path[pathInd - 1] % 20] not in playerPositions and path[(pathInd - 1)] not in playerHistory: # and [path[pathInd - 1] // 20, path[pathInd - 1] % 20] not in playerPositions:
		# 		curBest = [path[pathInd - 1], 1]
		# 		print([path[pathInd] // 20, path[pathInd] % 20], playerPositions)
		# 	else:
		# 		if [path[(pathInd + 1) % 400] // 20, path[(pathInd + 1) % 400] % 20] not in playerPositions and path[(pathInd + 1) % 400] not in playerHistory:
		# 			curBest = [path[(pathInd + 1) % 400], 1]

		# 		else:
		# 			if [path[pathInd - 1] // 20, path[pathInd - 1] % 20] not in playerPositions and path[(pathInd - 1)] not in playerHistory:
		# 				curBest = [path[pathInd - 1], 1]

		# 			else:
		# 				if [path[pathInd - 1] // 20, path[pathInd - 1] % 20] not in playerPositions: 
		# 					curBest = [path[pathInd - 1], float('-inf')]

		# 				elif [path[pathInd + 1] // 20, path[pathInd + 1] % 20] not in playerPositions:
		# 					curBest = [path[pathInd + 1], float('-inf')]

		# 				else:
		# 					curBest = [None, float('-inf')]




		# if [curBest[0] // 20, curBest[0] % 20] in playerPositions:
		# 	curBest[1] = float('-inf')

		for i in moveNums:


			if i > 0 and i < 400 and [i // 20, i % 20] not in playerPositions: # and [i // 20,  i % 20] not in applePosTaken:
				# print("History", i in playerHistory, i, playerHistory)

				indInLst = indexOf(path, i)

				tailInLst = indexOf(path, (playerPositions[-1][0] * 20) + playerPositions[-1][1])
				# for j in range(len(path)):
				# 	if path[j] == j:
				# 		indInLst = i
				# 		break



				# print(i, applePosNum)



				# if i == applePosNum:
				# 	curBest = [i, float('Inf')]

				# elif pathInd > indInLst:
				# 	skipped = list(range(indInLst, pathInd, 1))

				# 	for k in skipped:
				# 		if k in skippedInds:
				# 			skipped.remove(k)
				# 		else:
				# 			skippedInds.append(k)


				# 	if not (applePosNum > indInLst and applePosNum < pathInd) and [i // 20,  i % 20] not in playerPositions and i // 20 not in [-1, 20] and i % 20 not in [-1, 20]:
				# 		if len(skipped) > curBest[1]:
				# 			curBest = [i, len(skipped)]

				# elif pathInd < indInLst:
				# 	skipped = list(range(pathInd, indInLst, 1))



				# 	for k in skipped:
				# 		if k in skippedInds:
				# 			skipped.remove(k)
				# 		else:
				# 			skippedInds.append(k)




				# 	if not (applePosNum < indInLst and applePosNum > pathInd) and [i // 20,  i % 20] not in playerPositions and i // 20 not in [-1, 20] and i % 20 not in [-1, 20]:
				# 		if len(skipped) > curBest[1]:
				# 			curBest = [i, len(skipped)]


				# if forward:
				if indInLst > pathInd: 
					if not (applePathInd < indInLst and applePathInd > pathInd) and not (tailInLst <= indInLst and tailInLst >= pathInd):
						if curBest[1] < indInLst - pathInd:
							curBest = [i, indInLst - pathInd]

				else:
					if (not (applePathInd > pathInd) and not (applePathInd < indInLst)) and (not (tailInLst >= pathInd) and not (tailInLst <= indInLst)):
						if curBest[1] < (400 - pathInd) + indInLst:
							curBest = [i, (400 - pathInd) + indInLst]

				# else:
				# if not (applePathInd >= indInLst and applePathInd <= pathInd) and not (tailInLst >= indInLst and tailInLst <= pathInd):
				# 	if curBest[1] < pathInd - indInLst:
				# 		curBest = [i, pathInd - indInLst]


		# if curBest[1] == float('-inf'):
		# 	curBest[0] = path[pathInd + 1]


		# print(curBest)
		# print(lastResort, moveNums)

		# if curBest[0] == None:
		# 	# print(lastResort)
		# 	for i in lastResort:
		# 		indInLst = indexOf(path, i)
		# 		# print(i, indInLst)
		# 		if forward:
		# 			if indInLst - pathInd > curBest[1]:
		# 				curBest = [i, indInLst - pathInd]


		# 		else:
		# 			if curBest[1] < pathInd - indInLst:
		# 				curBest = [i, pathInd - indInLst]

			# if curBest[0] == 0:
			# 	print(curBest)
		newHead = [curBest[0] // 20,  curBest[0] % 20]

		# applePosTaken.append(newHead)

		# playerHistory.append(curBest[0])

		# print(playerHistory)






		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		# 	if event.type == pygame.KEYDOWN:
		# 		if event.key == K_UP:
		# 			if direction == 'Right' or direction == 'Left':
		# 				# turns.append([[playerX[0], playerY[0]], 2])
		# 				direction = 'Up'
		# 		if event.key == K_DOWN:
		# 			if direction == 'Right' or direction == 'Left':
		# 				# turns.append([[playerX[0], playerY[0]], 4])
		# 				direction = 'Down'
		# 		if event.key == K_RIGHT:
		# 			if direction == 'Down' or direction == 'Up':
		# 				# turns.append([[playerX[0], playerY[0]], 1])
		# 				direction = 'Right'
		# 		if event.key == K_LEFT:
		# 			if direction == 'Down' or direction == 'Up':
		# 				# turns.append([[playerX[0], playerY[0]], 3])
		# 				direction = 'Left'

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








		# if direction == 'Up':
		# 	playerPositions.insert(0, [playerPositions[0][0], playerPositions[0][1] - 1])
		# elif direction == 'Down':
		# 	playerPositions.insert(0, [playerPositions[0][0], playerPositions[0][1] + 1])

		# elif direction == 'Left':
		# 	playerPositions.insert(0, [playerPositions[0][0] - 1, playerPositions[0][1]])

		# elif direction == 'Right':

		playerPositions.insert(0, newHead)


		if playerPositions[0] == applePostion:
			if len(playerPositions) == 400:
				running = False
				break
			applePostion = createApple(playerPositions)
			applePosNum = (20 * applePostion[0]) + applePostion[1]
			# for i in range(len(path)):
			# 	if path[i] == applePosNum:
			# 		applePathInd = i
			# 		break

			applePathInd = indexOf(path, applePosNum)

			applePosTaken = []

			applePathInd = applePathInd%400

			# skippedInds = []

			# playerHistory = []

			# forwardDistance = None

			# if playerHeadInd < applePathInd:
			# 	forwardDistance = applePathInd - playerHeadInd

			# else:
			# 	forwardDistance = (400 - playerHeadInd) + applePathInd


			# backwardDistance = None

			# if playerHeadInd > applePathInd:
			# 	backwardDistance = playerHeadInd - applePathInd

			# else:
			#	backwardDistance = playerHeadInd + (400 - applePathInd)


			# if playerHeadInd > applePathInd:
			# 	forward = False

			# else:

			# 	forward = True

			# forward = True if forwardDistance < backwardDistance else False

		else:
			playerPositions.pop(-1)





		# if len(playerPositions) >= 10:
		showPlayer(playerPositions, screen)
		pygame.draw.rect(screen, (255,0,0), (encode(applePostion[0]) + 1, encode(applePostion[1]) + 1, 29, 29))
		# pygame.time.wait(100)

		# pygame.display.update()


		moves += 1
		
		
		# print(moves)
		await asyncio.sleep(0)


	return moves


asyncio.run(mainAI())
