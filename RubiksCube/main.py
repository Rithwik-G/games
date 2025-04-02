import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math

import time

import random
import asyncio





class Piece:
	RIGHT = (1, 4, 7, 5)
	LEFT = (0, 2, 6, 3)
	UP = (2, 4, 7, 6)
	DOWN = (0, 1, 5, 3)
	FRONT = (3, 5, 7, 6)
	BACK = (0, 1, 4, 2)
	def __init__(self, sideLength, pieceNum):
		self.sideLength = sideLength
		self.width = 1

		self.x = (pieceNum % sideLength) * self.width
		self.z = math.floor((pieceNum + 0.1)/(sideLength ** 2)) * self.width
		self.y = math.floor(((pieceNum + 0.1) % (sideLength ** 2)) / sideLength) * self.width

		self.even = sideLength % 2 == 0

		self.x -= (math.floor(sideLength/2) + (self.width/2)) if not self.even else math.floor(sideLength/2)
		self.y -= (math.floor(sideLength/2) + (self.width/2)) if not self.even else math.floor(sideLength/2)
		self.z -= (math.floor(sideLength/2) + (self.width/2)) if not self.even else math.floor(sideLength/2)


		self.centerX = (self.x + (self.width/2)) if not self.even else self.x
		self.centerY = (self.y + (self.width/2)) if not self.even else self.y
		self.centerZ = (self.z + (self.width/2)) if not self.even else self.z

		self.originalCenterX = self.centerX
		self.originalCenterY = self.centerY
		self.originalCenterZ = self.centerZ



		# self.centerX, self.centerY, self.centerZ, self.x, self.y, self.z)
		# self.xRotateCenterY = (sideLength * self.width)/2
		# self.xRotateCenterZ = (sideLength * self.width)/2

		# self.yRotateCenterX = (sideLength * self.width)/2
		# self.yRotateCenterZ = (sideLength * self.width)/2

		# self.zRotateCenterX = (sideLength * self.width)/2
		# self.zRotateCenterY = (sideLength * self.width)/2

		# self.outerRadius = ((self.xRotateCenterY ** 2) + (self.xRotateCenterZ ** 2)) ** 0.5

		# self.innerRadius = self.outerRadius - (2 ** 0.5)

		self.vertices = [(self.x, self.y, self.z),
						 (self.x + self.width, self.y, self.z),
						 (self.x, self.y + self.width, self.z),
						 (self.x, self.y, self.z + self.width),
						 (self.x + self.width, self.y + self.width, self.z), 
						 (self.x + self.width, self.y, self.z + self.width),
						 (self.x, self.y + self.width, self.z + self.width),
						 (self.x + self.width, self.y + self.width, self.z + self.width)]
		for i in range(len(self.vertices)):
			self.vertices[i] = list(self.vertices[i])

		self.allEdges = [(0, 1),
					  (0, 2),
					  (0, 3),
					  (1, 4),
					  (1, 5),
					  (2, 6),
					  (2, 4),
					  (3, 5),
					  (3, 6),
					  (4, 7),
					  (5, 7),
					  (6, 7)]





		# self.allSurfacesRight = {self.FRONT : self.UP,
		# 						 self.UP : self.BACK,
		# 						 self.BACK : self.DOWN,
		# 						 self.DOWN : self.FRONT,
		# 						 self.LEFT : self.LEFT,
		# 						 self.RIGHT : self.RIGHT}

		# self.allSurfacesRightPrime = {self.allSurfacesRight[key] : key for key in self.allSurfacesRight}
		self.edges = set()
		self.surfaces = []
		self.colors = []
		self.firstSurfAxis, self.firstSurfSide = None, None



		if self.centerX == ((sideLength - 1) * self.width) - math.floor(sideLength/2):
			self.surfaces.append((1, 4, 7, 5))
		
			self.colors.append(RED)
			if self.firstSurfAxis == None:
				self.firstSurfAxis, self.firstSurfSide = 'x', self.centerX


		if self.centerX == 0 - math.floor(sideLength/2):
			self.surfaces.append((0, 2, 6, 3))

			self.colors.append(ORANGE)
			if self.firstSurfAxis == None:
				self.firstSurfAxis, self.firstSurfSide = 'x', self.centerX

		if self.centerZ == ((sideLength - 1) * self.width) - math.floor(sideLength/2):
			self.surfaces.append((3, 5, 7, 6))

			self.colors.append(GREEN)
			if self.firstSurfAxis == None:
				self.firstSurfAxis, self.firstSurfSide = 'z', self.centerZ

		if self.centerZ == 0 - math.floor(sideLength/2):
			self.surfaces.append((0, 1, 4, 2))
			self.colors.append(BLUE)
			if self.firstSurfAxis == None:
				self.firstSurfAxis, self.firstSurfSide = 'z', self.centerZ

		if self.centerY == ((sideLength - 1) * self.width) - math.floor(sideLength/2):
			self.surfaces.append((2, 4, 7, 6))
			self.colors.append(WHITE)
			if self.firstSurfAxis == None:
				self.firstSurfAxis, self.firstSurfSide = 'y', self.centerY

		if self.centerY == 0 - math.floor(sideLength/2):
			self.surfaces.append((0, 1, 5, 3))
			self.colors.append(YELLOW)
			if self.firstSurfAxis == None:
				self.firstSurfAxis, self.firstSurfSide = 'y', self.centerY

		for surface in range(len(self.surfaces)):
			for ind in range(len(self.surfaces[surface][:-1])):
				self.edges.add((self.surfaces[surface][ind], self.surfaces[surface][ind + 1]))


		self.originalSurfaces = []

		for m in range(len(self.vertices)):
			for j in range(len(self.vertices[m])):
				self.vertices[m][j] = round(self.vertices[m][j] * 10)/10

		for surface in self.surfaces:
			realSurface = []
			for vertex in surface:
				realSurface.append(self.vertices[vertex])

			self.originalSurfaces.append(realSurface)


		self.ignore = False

		if len(self.colors) == 2:
			if not (self.centerX == 0 or self.centerY == 0 or self.centerZ == 0):
				self.ignore = True






	def draw(self):
		glBegin(GL_QUADS)

		for index, surface in enumerate(self.surfaces):
			glColor3fv(self.colors[index])
			for vertex in surface:
				glVertex3fv(self.vertices[vertex])

		glEnd()

		# glBegin(GL_LINES)

		# glColor3fv((0, 0, 0))

		# for edge in self.edges:
		# 	for vertex in edge:
		# 		glVertex3fv(self.vertices[vertex])

		# glEnd()


	def rotate(self, index, x, y, degrees, nonVertex = False):
		degrees = math.radians(degrees)
		if not nonVertex:
			self.vertices[index][x], self.vertices[index][y] = (self.vertices[index][x] * math.cos(degrees)) - (self.vertices[index][y] * math.sin(degrees)), (self.vertices[index][x] * math.sin(degrees)) + (self.vertices[index][y] * math.cos(degrees))
		else:	
			return (x * math.cos(degrees)) - (y * math.sin(degrees)), (x * math.sin(degrees)) + (y * math.cos(degrees))
	def xTurn(self, degrees, xLayer):
		# newSurfs = []
		# for i in self.surfaces:
		# 	newSurfs.append(self.allSurfacesRight[i])
		if self.centerX == xLayer:
			self.centerZ, self.centerY = self.rotate(None, self.centerZ, self.centerY, degrees, nonVertex = True)
			for i in range(0, len(self.vertices)):
				self.rotate(i, 2, 1, degrees)


		# self.surfaces = newSurfs


		# self.vertices[0][1] = self.outerRadius * math.sin(deg)
		# self.vertices[0][2] = self.outerRadius * math.cos(deg)

		# self.vertices[1][1] = self.vertices[0][1]
		# self.vertices[1][2] = self.vertices[0][2]

		# self.vertices[2][1] = 

		# self.vertices[6][1] = self.innerRadius * math.sin(deg)
		# self.vertices[6][2] = self.innerRadius * math.cos(deg)

	def yTurn(self, degrees, yLayer):
		# newSurfs = []
		# for i in self.surfaces:
		# 	newSurfs.append(self.allSurfacesRight[i])
		if self.centerY == yLayer:
			self.centerX, self.centerZ = self.rotate(None, self.centerX, self.centerZ, degrees, nonVertex = True)
			for i in range(0, len(self.vertices)):
				self.rotate(i, 0, 2, degrees)

	def zTurn(self, degrees, zLayer):
		# newSurfs = []
		# for i in self.surfaces:
		# 	newSurfs.append(self.allSurfacesRight[i])
		if self.centerZ == zLayer:
			self.centerY, self.centerX = self.rotate(None, self.centerY, self.centerX, degrees, nonVertex = True)
			for i in range(0, len(self.vertices)):
				self.rotate(i, 1, 0, degrees)
	def xRotation(self, degrees):
		self.xTurn(degrees, self.centerX)

	def yRotation(self, degrees):
		self.yTurn(degrees, self.centerY)


	def zRotation(self, degrees):
		self.zTurn(degrees, self.centerZ)



	def rightTurnPrime(self):
		newSurfs = []
		for i in self.surfaces:
			newSurfs.append(self.allSurfacesRightPrime[i])

		self.surfaces = newSurfs

	def roundCenters(self):
		self.centerX = round(self.centerX)
		self.centerY = round(self.centerY)
		self.centerZ = round(self.centerZ)

		newVertices = []

		for i in self.vertices:
			newVertex = []
			for j in i:
				newVertex.append(round(j * 10)/10)

			newVertices.append(newVertex)

		self.vertices = newVertices

		# for i in self.vertices:
		# 	print(i)


	def findActualSurfaces(self):
		actualSurfaces = []
		for surface in self.surfaces:
			newSurface = []
			for index in surface:
				newSurface.append(self.vertices[index])

			actualSurfaces.append(newSurface)


		return actualSurfaces

	def solved(self):
		# actualSurfaces = self.findActualSurfaces()
		# newSurfs = []
		# for i in self.originalSurfaces:
		# 	newSurf = []
		# 	for vertex in i:
		# 		newVertex = []
		# 		for val in vertex:
		# 			newVertex.append(round(val * 10)/10)

		# 		newSurf.append(newVertex)

		# 	newSurfs.append(newSurf)

		# self.originalSurfaces = newSurfs


		# for i in range(len(actualSurfaces)):
		# 	if actualSurfaces[i] not in self.originalSurfaces:
		# 		print(actualSurfaces[i], self.originalSurfaces)
		# 		return False

		if self.centerX == self.originalCenterX and self.centerY == self.originalCenterY and self.centerZ == self.originalCenterZ and self.findAxisOfSurface(0, math.floor(self.sideLength/2)) == [self.firstSurfAxis, self.firstSurfSide]:
			# for k in range(len(actualSurfaces[i])):
			# 	for l in range(len(actualSurfaces[i][k])):
			# 		if round(actualSurfaces[i][k][l]*10)/10 != round(self.originalSurfaces[i][k][l]*10)/10:
			# 			print(round(actualSurfaces[i][k][l]*10)/10, round(self.originalSurfaces[i][k][l]*10)/10)
			return True	



		return False


	def positioned(self):
		return self.centerX == self.originalCenterX and self.centerY == self.originalCenterY and self.centerZ == self.originalCenterZ

	def findAxisOfSurface(self, index, right):
		surface = self.findActualSurfaces()[index]
		common = {(round(i * 10)/10, ind) : 1 for ind, i in enumerate(surface[0])}
		for i in surface[1:]:
			for ind, j in enumerate(i):
				if (round(j * 10)/10, ind) in common.keys():
					common[(round(j * 10)/10, ind)] += 1

		index = None
		val = None
		for i, ind in common:
			if common[(i, ind)] == 4:
				index = ind
				val = i
				break

		returnTuple = []
		if index == 0:
			returnTuple.append('x')

		elif index == 1:
			returnTuple.append('y')

		else:
			returnTuple.append('z')

		if val > 0:
			returnTuple.append(right)

		else:
			returnTuple.append(-right)

		return returnTuple

xMovement = 0
yMovement = 0
zMovement = 0
posChange = 0.1

def checkMovement():
	global xMovement, yMovement, zMovement, change
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
			break

		if event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_LEFT, pygame.K_d]:
				xMovement = -change

			if event.key in [pygame.K_UP, pygame.K_w]:
				zMovement = change

			if event.key in [pygame.K_RIGHT, pygame.K_a]:
				xMovement = change

			if event.key in [pygame.K_DOWN, pygame.K_s]:
				zMovement = -change

		if event.type == pygame.KEYUP:
			if event.key in [pygame.K_LEFT, pygame.K_d]:
				xMovement = 0

			if event.key in [pygame.K_UP, pygame.K_w]:
				zMovement = 0

			if event.key in [pygame.K_RIGHT, pygame.K_a]:
				xMovement = 0

			if event.key in [pygame.K_DOWN, pygame.K_s]:
				zMovement = 0
			



		glTranslatef(xMovement, yMovement, zMovement)





def turnCubes(cubes, axis, change, row, show = True):
	show = True
	clock = pygame.time.Clock()
	global realChange, xMovement, yMovement, zMovement, posChange, solving

	if solving:
		moveLstForSolved.append([cubes, axis, change, row])
		return
	if change < 0:
		change = -realChange

	else:
		change = realChange

	for i in range(int(90/abs(change))):

		clock.tick(60)
		glEnable(GL_DEPTH_TEST) 
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				break

			if event.type == pygame.KEYDOWN:
				if event.key in [pygame.K_LEFT, pygame.K_d]:
					xMovement = -posChange

				elif event.key in [pygame.K_UP, pygame.K_w]:
					yMovement = posChange

				elif event.key in [pygame.K_RIGHT, pygame.K_a]:
					xMovement = posChange

				elif event.key in [pygame.K_DOWN, pygame.K_s]:
					yMovement = -posChange

			if event.type == pygame.KEYUP:
				if event.key in [pygame.K_LEFT, pygame.K_d]:
					xMovement = 0

				elif event.key in [pygame.K_UP, pygame.K_w]:
					yMovement = 0

				elif event.key in [pygame.K_RIGHT, pygame.K_a]:
					xMovement = 0

				elif event.key in [pygame.K_DOWN, pygame.K_s]:
					yMovement = 0

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					zMovement = posChange

				elif event.button == 5:
					zMovement = -posChange
			



		glTranslatef(xMovement, yMovement, zMovement)
		zMovement = 0
		for cube in cubes:
			if axis == 'z':
				cube.zTurn(change, row)

			elif axis == 'x':
				cube.xTurn(change, row)

			elif axis == 'y':
				cube.yTurn(change, row)

			if show:
				cube.draw()

		if show:

			pygame.display.flip()

			# glRotatef(1, 1, 1, 1)

	for cube in cubes:
		cube.roundCenters()



def basicTurns(cubes, right, turns, show = True):
	speed = 3
	global solving
	if solving:
		moveLstForSolved.extend(turns)
		return
	for turn in turns:
		if turn == 'R':
			turnCubes(cubes, 'x', speed, right, show = show)

		elif turn == 'L':
			turnCubes(cubes, 'x', -speed, -right, show = show)

		elif turn == 'U':
			turnCubes(cubes, 'y', speed, right, show = show)

		elif turn == 'D':
			turnCubes(cubes, 'y', -speed, -right, show = show)

		elif turn == 'F':
			turnCubes(cubes, 'z', speed, right, show = show)

		elif turn == 'B':
			turnCubes(cubes, 'z', -speed, -right, show = show)

		elif turn == 'R\'':
			turnCubes(cubes, 'x', -speed, right, show = show)

		elif turn == 'L\'':
			turnCubes(cubes, 'x', speed, -right, show = show)

		elif turn == 'U\'':
			turnCubes(cubes, 'y', -speed, right, show = show)

		elif turn == 'D\'':
			turnCubes(cubes, 'y', speed, -right, show = show)

		elif turn == 'F\'':
			turnCubes(cubes, 'z', -speed, right, show = show)

		elif turn == 'B\'':
			turnCubes(cubes, 'z', speed, -right, show = show)




def cornerAlg(cubes, right):
	basicTurns(cubes, right, ['R', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R\'', 'F\'', 'R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R'])
	# # R
	# turnCubes(cubes, 'x', -3, right, show = True)
	# # U'
	# turnCubes(cubes, 'y', -3, right, show = True)
	# # R'
	# turnCubes(cubes, 'x', 3, right, show = True)
	# # U'
	# turnCubes(cubes, 'y', -3, right, show = True)
	# # R
	# turnCubes(cubes, 'x', -3, right, show = True)
	# # U
	# turnCubes(cubes, 'y', 3, right, show = True)
	# # R'
	# turnCubes(cubes, 'x', 3, right, show = True)
	# # F'
	# turnCubes(cubes, 'z', 3, right, show = True)
	# # R
	# turnCubes(cubes, 'x', -3, right, show = True)
	# # U
	# turnCubes(cubes, 'y', 3, right, show = True)
	# # R'
	# turnCubes(cubes, 'x', 3, right, show = True)
	# # U'
	# turnCubes(cubes, 'y', -3, right, show = True)
	# # R'
	# turnCubes(cubes, 'x', 3, right, show = True)
	# # F
	# turnCubes(cubes, 'z', -3, right, show = True)
	# # R
	# turnCubes(cubes, 'x', -3, right, show = True)



def solveForLetter(cubes, letter, right):
	reverseMoves = {'R' : 'R\'',
					'R\'' : 'R',
					'D' : 'D\'',
					'D\'' : 'D',
					'U' : 'U\'',
					'U\'' : 'U',
					'L' : 'L\'',
					'L\'' : 'L',
					'F' : 'F\'',
					'F\'' : 'F',
					'B' : 'B\'',
					'B\'' : 'B'}



	if letter == 'b':
		moves = ['R\'', 'R\'']


	elif letter == 'c':
		moves = ['R\'', 'R\'', 'D\'']

	elif letter == 'd':
		moves = ['F', 'F']

	elif letter == 'f':
		moves = ['F\'', 'D']

	elif letter == 'g':
		moves = ['F\'']

	elif letter == 'h':
		moves = ['D', 'F', 'F', 'R\'']

	elif letter == 'i':
		moves = ['F', 'R\'']

	elif letter == 'j':
		moves = ['R\'']

	elif letter == 'k':
		moves = ['F\'', 'R\'']

	elif letter == 'l':
		moves = ['F', 'F', 'R\'']

	elif letter == 'm':
		moves = ['F']

	elif letter == 'n':
		moves = ['R\'', 'F']

	elif letter == 'o':
		moves = ['R', 'R', 'F']

	elif letter == 'p':
		moves = ['R', 'F']

	elif letter == 'q':
		moves = ['R', 'D\'']

	elif letter == 's':
		moves = ['D', 'F\'']

	elif letter == 't':
		moves = ['R']

	elif letter == 'u':
		moves = ['D']

	elif letter == 'v':
		moves = []

	elif letter == 'w':
		moves = ['D\'']

	elif letter == 'x':
		moves = ['D', 'D']

	else:
		return False



	basicTurns(cubes, right, moves, show = True)

	cornerAlg(cubes, right)

	moves.reverse()

	newMoves = []

	for i in moves:
		newMoves.append(reverseMoves[i])


	basicTurns(cubes, right, newMoves, show = True)


		







def verticesToLetter(vertices):
	possibleLetters = []
	common = {(round(i * 10)/10, ind) : 1 for ind, i in enumerate(vertices[0])}
	for i in vertices[1:]:
		for ind, j in enumerate(i):
			if (round(j * 10)/10, ind) in common.keys():
				common[(round(j * 10)/10, ind)] += 1

	for i, ind in common:
		if common[(i, ind)] == 4:
			common.pop((i, ind))
			common = [i for i, ind in common]
			if ind == 0:
				if i >= 0:
					# possibleLetters = ['m', 'n', 'o', 'p']
					if common[0] >= 0:
						# possibleLetters = ['m', 'n']
						if common[1] >= 0:
							return 'm'

						else:
							return 'n'

					else:
						# possibleLetters = ['o', 'p']
						if common[1] >= 0:
							return 'p'

						else:
							return 'o'

				else:
					# possibleLetters = ['e', 'f', 'g', 'h']
					if common[0] >= 0:
						# possibleLetters = ['e', 'f']
						if common[1] >= 0:
							return 'f'

						else:
							return 'e'


					else:
						# possibleLetters = ['g', 'h']
						if common[1] >= 0:
							return 'g'

						else:
							return 'h'

			elif ind == 1:
				if i >= 0:
					# possibleLetters = ['a', 'b', 'c', 'd']
					if common[0] <= 0:
						# possibleLetters = ['a', 'd']

						if common[1] >= 0:
							return 'd'

						else:
							return 'a'

					else:
						# possibleLetters = ['b', 'c']
						if common[1] >= 0:
							return 'c'

						else:
							return 'b'

				else:
					# possibleLetters = ['y', 'v', 'w', 'x']
					if common[0] <= 0:
						# possibleLetters = ['u', 'x']

						if common[1] >= 0:
							return 'u'

						else:
							return 'x'

					else:
						# possibleLetters = ['v', 'w']
						if common[1] >= 0:
							return 'v'

						else:
							return 'w'

			elif ind == 2:
				if i >= 0:
					# possibleLetters = ['i', 'j', 'k', 'l']
					if common[0] <= 0:
						# possibleLetters = ['i', 'l']
						if common[1] >= 0:
							return 'i'

						else:
							return 'l'

					else:
						# possibleLetters = ['j', 'k']
						if common[1] >= 0:
							return 'j'

						else:
							return 'k'

				else:
					# possibleLetters = ['q', 'r', 's', 't']
					if common[0] <= 0:
						# possibleLetters = ['r', 's']
						if common[1] >= 0:
							return 'r'

						else:
							return 's'

					else:
						# possibleLetters = ['q', 't']
						if common[1] >= 0:
							return 'q'

						else:
							return 't'





def solve3x3Bad(cubes, sideLength):
	left = -math.floor(sideLength/2)
	right = math.floor(sideLength/2)
	# Solve Corners
	notSolved = True
	while notSolved:
		curCube = None
		curTargetFaceColor = None

		for i in cubes:
			if i.centerX == left and i.centerY == right and i.centerZ == left:
				curCube = i
				notCorrect = True
				if curCube.centerX == curCube.originalCenterX and curCube.centerY == curCube.originalCenterY and curCube.centerZ == curCube.originalCenterZ:
					solved = True
					for i in cubes:
						if (not i.centerX == i.originalCenterX or not i.centerY == i.originalCenterY or not i.centerZ == i.originalCenterZ) and len(i.surfaces) == 3 and not (i.centerX != curCube.centerX and i.centerY != curCube.centerY and i.centerZ != curCube.centerZ):
							newSurface = []
							for k in i.surfaces[0]:
								newSurface.append(i.vertices[k])
							targetFaceLetter = verticesToLetter(newSurface)
							solved = False
							break


					if solved:
						notSolved = False
				else:

					curTargetFaceColor = None 
					possibleSurfaces = curCube.surfaces.copy()
					# for ind, j in enumerate(curCube.vertices):
					# 	if j[0] + 0.5 == left:
					# 		for k in possibleSurfaces:
					# 			if ind not in k:
					# 				possibleSurfaces.remove(k)
					counter = 0
					while len(possibleSurfaces) != 1:
						deleted = False
						for k in possibleSurfaces[counter]:
							if curCube.vertices[k][0] + 0.5 != left:
								possibleSurfaces.pop(counter)

								deleted = True

								break

						if not deleted:
							break


					curTargetFaceInd = curCube.surfaces.index(possibleSurfaces[0])

					targetFace = curCube.originalSurfaces[curTargetFaceInd]

					targetFaceLetter = verticesToLetter(targetFace)

					if targetFaceLetter not in ['a', 'r', 'e']:
						notCorrect = False

				

						# for i in range(len(curCube.colors)):
						# 	curCube.colors[i] = (0, 0, 0)


				while notCorrect:
					print("Forced")
					solved = True
					for i in cubes:
						if not i == curCube and len(i.surfaces) == 3 and not i.solved():
							newSurface = []
							for k in i.surfaces[0]:
								newSurface.append(i.vertices[k])
							targetFaceLetter = verticesToLetter(newSurface)
							solved = False
							notCorrect = False
							break


					if solved:
						notSolved = False
						notCorrect = False
			# for i in targetFace:
			# 	curCube.vertices.append(i)

			# curCube.surfaces.append([8, 9, 10, 11])

			# curCube.colors.append((0, 0, 0))

			# cubes.reverse()

				break

		print(targetFaceLetter)

		if solveForLetter(cubes, targetFaceLetter, right) == False:
			print(curCube.centerY, curCube.originalCenterY, targetFaceLetter)



		# target = None



		# for i in cubes:
		# 	if i.centerX == curCube.originalCenterX and i.centerY == curCube.originalCenterY and i.centerZ == curCube.originalCenterZ:
		# 		target = i
		# 		for j in target.colors:
		# 			if j == curTargetFaceColor:
		# 				print("Found Color On Target")

		# 		notSolved = False
		# 		break

def rotateCubes(cubes, degrees):
	global show
	if show:
		for i in range(degrees):
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

			for cube in cubes:
				cube.draw()

			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
					break
			glRotatef(1, 0, 0, 0)

	else:
		glRotatef(degrees, 0, 0, 0)



def solve3x3(cubes, sideLength, speed = 3):
	global realChange, solving

	left = -math.floor(sideLength/2)
	right = math.floor(sideLength/2)
	# Cross
	# Red, Orange, Green, Blue, White, Yellow
	pieceOrder = [[GREEN, WHITE],
				  [RED, WHITE],
				  [BLUE, WHITE],
				  [ORANGE, WHITE]]

	for edge in pieceOrder:
		curEdge = None
		for cube in cubes:
			if cube.colors == edge and not cube.ignore:
				curEdge = cube
				break

		curTurn = None
		if not curEdge.solved():
			mess = True
			if curEdge.centerY == right:
				curTurn = curEdge.findAxisOfSurface(0, right)
				if curTurn[0] == 'y':
					curTurn = curEdge.findAxisOfSurface(1, right)
				
				else:
					mess = False

				turnCubes(cubes, curTurn[0], speed, curTurn[1])
				


			if curEdge.centerY == 0:
				curTurn = curEdge.findAxisOfSurface(0, right)
				multiplier = -1
				if curTurn[0] == 'x':
					if curEdge.centerZ == left:
						multiplier = 1

				else:
					if curEdge.centerX == right:
						multiplier = 1


				turnCubes(cubes, curTurn[0], multiplier * speed, curTurn[1])
				if mess:
					basicTurns(cubes, right, ['D'])

					turnCubes(cubes, curTurn[0], -1 * multiplier * speed, curTurn[1])

			if curEdge.findAxisOfSurface(0, right)[0] == 'y':
				while True:
					if curEdge.colors[0] == RED:
						if curEdge.centerX == 0 and curEdge.centerZ == right:
							basicTurns(cubes, right, ['F\'', 'R', 'F'])
							break

					elif curEdge.colors[0] == BLUE:
						if curEdge.centerX == right and curEdge.centerZ == 0:
							basicTurns(cubes, right, ['R\'', 'B', 'R'])
							break

					elif curEdge.colors[0] == ORANGE:
						if curEdge.centerX == 0 and curEdge.centerZ == left:
							basicTurns(cubes, right, ['B\'', 'L', 'B'])
							break

					elif curEdge.colors[0] == GREEN:
						if curEdge.centerX == left and curEdge.centerZ == 0:
							basicTurns(cubes, right, ['L\'', 'F', 'L'])
							break

					basicTurns(cubes, right, ['D'])




			else:
				while True:

					if curEdge.colors[0] == GREEN:
						if curEdge.centerX == 0 and curEdge.centerZ == right:
							basicTurns(cubes, right, ['F', 'F'])
							break

					elif curEdge.colors[0] == RED:
						if curEdge.centerX == right and curEdge.centerZ == 0:
							basicTurns(cubes, right, ['R', 'R'])
							break

					elif curEdge.colors[0] == BLUE:
						if curEdge.centerX == 0 and curEdge.centerZ == left:
							basicTurns(cubes, right, ['B', 'B'])
							break

					elif curEdge.colors[0] == ORANGE:
						if curEdge.centerX == left and curEdge.centerZ == 0:
							basicTurns(cubes, right, ['L', 'L'])
							break

					basicTurns(cubes, right, ['D'])


	# White Corners
	# Red, Orange, Green, Blue, White, Yellow
	pieceOrder = [[RED, GREEN, WHITE],
				  [RED, BLUE, WHITE],
				  [ORANGE, BLUE, WHITE],
				  [ORANGE, GREEN, WHITE]]


	for corner in pieceOrder:
		curCorner = None
		for cube in cubes:
			if cube.colors == corner and not cube.ignore:
				curCorner = cube
				break



		if not curCorner.solved():

			if curCorner.centerY == right:
				if curCorner.centerX == left and curCorner.centerZ == left:
					basicTurns(cubes, right, ['L\'', 'D\'', 'L'])

				elif curCorner.centerX == right and curCorner.centerZ == left:
					basicTurns(cubes, right, ['R', 'D', 'R\''])

				elif curCorner.centerX == right and curCorner.centerZ == right:
					basicTurns(cubes, right, ['R\'', 'D\'', 'R'])

				elif curCorner.centerX == left and curCorner.centerZ == right:
					basicTurns(cubes, right, ['L', 'D', 'L\''])








			while curCorner.centerX != curCorner.originalCenterX or curCorner.centerZ != curCorner.originalCenterZ:
				basicTurns(cubes, right, ['D'])

			if curCorner.findAxisOfSurface(-1, right)[0] == 'y':
				if curCorner.centerX == right and curCorner.centerZ == right:
					basicTurns(cubes, right, ['R\'', 'D', 'D', 'R', 'D'])

				elif curCorner.centerX == right and curCorner.centerZ == left:
					basicTurns(cubes, right, ['B\'', 'D', 'D', 'B', 'D'])

				elif curCorner.centerX == left and curCorner.centerZ == left:
					basicTurns(cubes, right, ['L\'', 'D', 'D', 'L', 'D'])

				elif curCorner.centerX == left and curCorner.centerZ == right:
					basicTurns(cubes, right, ['F\'', 'D', 'D', 'F', 'D'])



			if curCorner.centerX == left and curCorner.centerZ == left:
				if curCorner.findAxisOfSurface(-1, right)[0] == 'x':
					basicTurns(cubes, right, ['L\'', 'D\'', 'L'])

				else:
					basicTurns(cubes, right, ['B', 'D', 'B\''])

			elif curCorner.centerX == right and curCorner.centerZ == left:
				if curCorner.findAxisOfSurface(-1, right)[0] == 'x':
					basicTurns(cubes, right, ['R', 'D', 'R\''])

				else:
					basicTurns(cubes, right, ['B\'', 'D\'', 'B'])

			elif curCorner.centerX == right and curCorner.centerZ == right:
				if curCorner.findAxisOfSurface(-1, right)[0] == 'x':
					basicTurns(cubes, right, ['R\'', 'D\'', 'R'])

				else:
					basicTurns(cubes, right, ['F', 'D', 'F\''])

			elif curCorner.centerX == left and curCorner.centerZ == right:
				if curCorner.findAxisOfSurface(-1, right)[0] == 'x':
					basicTurns(cubes, right, ['L', 'D', 'L\''])

				else:
					basicTurns(cubes, right, ['F\'', 'D\'', 'F'])




	# Middle Layer
	# Red, Orange, Green, Blue, White, Yellow
	pieceOrder = [[RED, GREEN],
				  [RED, BLUE],
				  [ORANGE, BLUE],
				  [ORANGE, GREEN]]


	for edge in pieceOrder:
		curEdge = None
		for cube in cubes:
			if cube.colors == edge and not cube.ignore:
				curEdge = cube
				break

		if not curEdge.solved():

			if curEdge.centerY == 0:
				if curEdge.centerX == left and curEdge.centerZ == left:
					basicTurns(cubes, right, ['L\'', 'D', 'L', 'D', 'B', 'D\'', 'B\''])

				elif curEdge.centerX == right and curEdge.centerZ == left:
					basicTurns(cubes, right, ['R', 'D\'', 'R\'', 'D\'', 'B\'', 'D', 'B'])

				elif curEdge.centerX == right and curEdge.centerZ == right:
					basicTurns(cubes, right, ['D\'', 'R\'', 'D', 'R', 'D', 'F', 'D\'', 'F\''])

				elif curEdge.centerX == left and curEdge.centerZ == right:
					basicTurns(cubes, right, ['L', 'D\'', 'L\'', 'D\'', 'F\'', 'D', 'F'])

			normal = True
			while True:
				if curEdge.originalCenterX == left and curEdge.originalCenterZ == left:
					if curEdge.centerX == right and curEdge.centerZ == 0 and curEdge.findAxisOfSurface(0, right)[0] == 'y':
						break

					elif curEdge.centerX == 0 and curEdge.centerZ == right and curEdge.findAxisOfSurface(0, right)[0] != 'y':
						normal = False
						break

				elif curEdge.originalCenterX == right and curEdge.originalCenterZ == left:
					if curEdge.centerX == left and curEdge.centerZ == 0 and curEdge.findAxisOfSurface(0, right)[0] == 'y':
						break

					elif curEdge.centerX == 0 and curEdge.centerZ == right and curEdge.findAxisOfSurface(0, right)[0] != 'y':
						normal = False
						break

				elif curEdge.originalCenterX == right and curEdge.originalCenterZ == right:
					
					if curEdge.centerX == left and curEdge.centerZ == 0 and curEdge.findAxisOfSurface(0, right)[0] == 'y':
						break

					elif curEdge.centerX == 0 and curEdge.centerZ == left and curEdge.findAxisOfSurface(0, right)[0] != 'y':
						normal = False
						break



				elif curEdge.originalCenterX == left and curEdge.originalCenterZ == right:
					if curEdge.centerX == right and curEdge.centerZ == 0 and curEdge.findAxisOfSurface(0, right)[0] == 'y':
						break

					elif curEdge.centerX == 0 and curEdge.centerZ == left and curEdge.findAxisOfSurface(0, right)[0] != 'y':
						normal = False
						break


				basicTurns(cubes, right, ['D'])

			if curEdge.originalCenterX == left and curEdge.originalCenterZ == left:
				if normal:
					basicTurns(cubes, right, ['L\'', 'D', 'L', 'D', 'B', 'D\'', 'B\''])

				else:

					basicTurns(cubes, right, ['B', 'D\'', 'B\'', 'D\'', 'L\'', 'D', 'L'])

			elif curEdge.originalCenterX == right and curEdge.originalCenterZ == left:
				if normal:
					basicTurns(cubes, right, ['R', 'D\'', 'R\'', 'D\'', 'B\'', 'D', 'B'])

				else:

					basicTurns(cubes, right, ['B\'', 'D', 'B', 'D', 'R', 'D\'', 'R\''])
			elif curEdge.originalCenterX == right and curEdge.originalCenterZ == right:
				if normal:
					basicTurns(cubes, right, ['R\'', 'D', 'R', 'D', 'F', 'D\'', 'F\''])

				else:
					basicTurns(cubes, right, ['F', 'D\'', 'F\'', 'D\'', 'R\'', 'D', 'R'])

			elif curEdge.originalCenterX == left and curEdge.originalCenterZ == right:
				if normal:

					basicTurns(cubes, right, ['L', 'D\'', 'L\'', 'D\'', 'F\'', 'D', 'F'])

				else:
					basicTurns(cubes, right, ['F\'', 'D', 'F', 'D', 'L', 'D\'', 'L\''])

	rotateCubes(cubes, 180)

	# YELLOW CROSS
	allUp = []


	for cube in cubes:
		if YELLOW in cube.colors and cube.findAxisOfSurface(-1, right)[0] == 'y' and len(cube.surfaces) == 2 and not cube.ignore:
			allUp.append(cube)

	if len(allUp) == 0:
		basicTurns(cubes, right, ['F', 'L', 'D', 'L\'', 'D\'', 'F\''])

		basicTurns(cubes, right, ['D', 'D'])

		basicTurns(cubes, right, ['F', 'D', 'L', 'D\'', 'L\'', 'F\''])

	elif len(allUp) == 2:

		while True:
			if (allUp[0].centerX == 0 and allUp[0].centerZ == left and allUp[1].centerX == right and allUp[1].centerZ == 0) or (allUp[1].centerX == 0 and allUp[1].centerZ == left and allUp[0].centerX == right and allUp[0].centerZ == 0):
				basicTurns(cubes, right, ['F', 'D', 'L', 'D\'', 'L\'', 'F\''])
				break

			elif (allUp[0].centerX == right and allUp[0].centerZ == 0 and allUp[1].centerX == left and allUp[1].centerZ == 0) or (allUp[1].centerX == right and allUp[1].centerZ == 0 and allUp[0].centerX == left and allUp[0].centerZ == 0):
				basicTurns(cubes, right, ['F', 'L', 'D', 'L\'', 'D\'', 'F\''])
				break

			basicTurns(cubes, right, ['D'])

	
	# Permuting Top Cross


	frontEdge = None

	for cube in cubes:
		if cube.originalCenterX == 0 and cube.originalCenterZ == right and cube.originalCenterY == left and not cube.ignore:
			frontEdge = cube
			break

	while not frontEdge.solved():
		basicTurns(cubes, right, ['D'])


	allSolved = []



	for cube in cubes:
		if cube.solved() and YELLOW in cube.colors and len(cube.colors) == 2 and not cube.ignore:
			allSolved.append(cube)



	if len(allSolved) == 2:
		if (allSolved[1].centerX == 0 and allSolved[1].centerZ == left and allSolved[1].centerY == left) or (allSolved[0].centerX == 0 and allSolved[0].centerZ == left and allSolved[0].centerY == left):
			basicTurns(cubes, right, ['L', 'D', 'L\'', 'D', 'L', 'D\'', 'D\'', 'L\''])

	allSolved = []
	backEdge = None

	for cube in cubes:
		if cube.solved() and YELLOW in cube.colors and len(cube.colors) == 2 and not cube.ignore:
			allSolved.append(cube)

		if cube.centerX == 0 and cube.centerY == left and cube.centerZ == left and not cube.ignore:
			backEdge = cube


	if len(allSolved) == 2:
		while not backEdge.solved():
			basicTurns(cubes, right, ['D'])

		if backEdge.centerX == right:
			while not frontEdge.solved():
				basicTurns(cubes, right, ['F', 'D', 'F\'', 'D', 'F', 'D\'', 'D\'', 'F\''])

		elif backEdge.centerX == left:
			while not frontEdge.solved():
				basicTurns(cubes, right, ['B', 'D', 'B\'', 'D', 'B', 'D\'', 'D\'', 'B\''])


	elif len(allSolved) == 1:
		while True:
			solved = 0
			for cube in cubes:
				if YELLOW in cube.colors and len(cube.colors) == 2:
					if cube.solved():
						solved += 1

			if solved == 4:
				break


			basicTurns(cubes, right, ['L', 'D', 'L\'', 'D', 'L', 'D\'', 'D\'', 'L\''])
			

	# Position Corners Correctly

	bottomLeft = None


	for cube in cubes:
		if cube.originalCenterX == right and cube.originalCenterY == left and cube.originalCenterZ == right and not cube.ignore:
			bottomLeft = cube
			break


	if bottomLeft.centerX == left and bottomLeft.centerY == left and bottomLeft.centerZ == right:
		basicTurns(cubes, right, ['D'])
		while not (bottomLeft.centerX == right and bottomLeft.centerY == left and bottomLeft.centerZ == left):
			basicTurns(cubes, right, ['D', 'L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R'])

		basicTurns(cubes, right, ['D\''])



	else:

		while not bottomLeft.positioned():
			basicTurns(cubes, right, ['D', 'L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R'])

	while True:
		positioned = []
		for cube in cubes:
			if cube.positioned() and YELLOW in cube.colors and len(cube.colors) == 3:
				positioned.append(cube)

		if len(positioned) == 4:
			break

		basicTurns(cubes, right, ['D', 'F', 'D\'', 'B\'', 'D', 'F\'', 'D\'', 'B'])

	# # ORIENT LAST LAYER

	# while True:
	# 	solved = 0
	# 	for cube in cubes:
	# 		if cube.centerY == left and cube.findAxisOfSurface(-1, right) == ['y', -right]:
	# 			solved += 1

	# 	if solved == 9:
	# 		break

	# 	running = True
	# 	while True:
	# 		for cube in cubes:
	# 			if cube.centerX == right and cube.centerY == left and cube.centerZ == right:
	# 				if cube.findAxisOfSurface(-1, right) != ['y', -right]:
	# 					running = False
	# 					break

	# 		if not running:
	# 			break

	# 		basicTurns(cubes, right, ['D'])

	# 	running = True
	# 	while True:
	# 		for cube in cubes:
	# 			if cube.centerX == right and cube.centerY == left and cube.centerZ == right:
	# 				if cube.findAxisOfSurface(-1, right) == ['y', -right]:
	# 					running = False
						

	# 			if cube.centerX == right and cube.centerY == right and cube.centerZ == right:
	# 				if cube.findAxisOfSurface(-1, right) == ['y', -right]:
	# 					running = True
	# 					while cube.originalCenterX != cube.centerX or cube.originalCenterZ != cube.centerZ:
	# 						basicTurns(cubes, right, ['D'])
	# 						cube.originalCenterX, cube.originalCenterZ = cube.rotate(None, cube.originalCenterX, cube.originalCenterZ, -90, nonVertex = True)

	# 					break

	# 		if not running:
	# 			break

	# 		basicTurns(cubes, right, ['R', 'U', 'R\'', 'U\''])

	# Red, Orange, Green, Blue, White, Yellow

	pieceOrder = [[RED, GREEN, YELLOW],
				  [RED, BLUE, YELLOW],
				  [ORANGE, BLUE, YELLOW],
				  [ORANGE, GREEN, YELLOW]]


	for piece in pieceOrder:
		curCorner = None
		for cube in cubes:
			if cube.colors == piece and not cube.ignore:
				curCorner = cube
				break





		while not curCorner.findAxisOfSurface(-1, right) == ['y', left]:
			
			basicTurns(cubes, right, ['R', 'U', 'R\'', 'U\''])


		basicTurns(cubes, right, ['D\''])











	rotateCubes(cubes, 180)


def solveNxN(cubes, sideLength):
	global realChange


	right = math.floor(sideLength/2)
	left = -right
	# White Center
	for x in range(left + 1, right):
		for z in range(left + 1, right):
			smallMess = z != left + 1
			bigMess = x != left + 1
			curCenter = None
			for cube in cubes:
				if cube.originalCenterX == x and cube.originalCenterZ == z and cube.originalCenterY == right:
					curCenter = cube
					break

			if curCenter.centerY == left:
				turnX = curCenter.centerX
				turnCubes(cubes, 'x', -realChange, turnX)

				if bigMess or smallMess:

					while curCenter.centerX == turnX:
						turnCubes(cubes, 'z', realChange, left)

					turnCubes(cubes, 'x', realChange, turnX)

			elif curCenter.centerY == right:

				turnZ = curCenter.centerZ

				turnCubes(cubes, 'z', realChange, turnZ)

				turnY = curCenter.centerY

				if bigMess:

					if curCenter.centerX == 0 and curCenter.centerY == 0:

						turnCubes(cubes, 'y', realChange, turnY)

					else:

						turnCubes(cubes, 'y', -realChange, turnY)

					turnCubes(cubes, 'z', -realChange, turnZ)

				else:
					turnCubes(cubes, 'y', -realChange, turnY)

				if smallMess:


					if curCenter.centerX != 0 or curCenter.centerY != 0:

						while curCenter.centerY == turnY:

							turnCubes(cubes, 'z', -realChange, left)



						turnCubes(cubes, 'y', realChange, turnY)


			elif curCenter.centerZ == right and -curCenter.centerY != curCenter.originalCenterZ and curCenter.centerX != curCenter.originalCenterX:
				if not (curCenter.originalCenterX == 0 and curCenter.originalCenterZ == 0):
					if smallMess:
						turnCubes(cubes, 'z', realChange, right)

					turnCubes(cubes, 'y', realChange, curCenter.centerY)
					turnCubes(cubes, 'y', realChange, curCenter.centerY)

					if smallMess:
						turnCubes(cubes, 'z', -realChange, right)


			else:
				turnY = curCenter.centerY
				totalMoves = 0
				if curCenter.originalCenterX == 0 and curCenter.originalCenterZ == 0:
					while curCenter.centerZ != right:
						turnCubes(cubes, 'y', realChange, turnY)

				else:
					while curCenter.centerZ != left:
						turnCubes(cubes, 'y', realChange, turnY)
						totalMoves += 1

					if smallMess:
						while curCenter.centerY == turnY:

							turnCubes(cubes, 'z', realChange, left)

						for i in range(totalMoves):
							turnCubes(cubes, 'y', -realChange, turnY)

			if -curCenter.centerY != curCenter.originalCenterZ or curCenter.centerX != curCenter.originalCenterX or curCenter.centerZ != right:
				if curCenter.centerZ != left:
					print(curCenter.centerZ)

				while -curCenter.centerX != curCenter.originalCenterX or -curCenter.centerY != curCenter.originalCenterZ:
   
					turnCubes(cubes, 'z', -realChange, left)

				turnCubes(cubes, 'y', realChange, curCenter.centerY)
				turnCubes(cubes, 'y', realChange, curCenter.centerY)


				


		turnCubes(cubes, 'x', realChange, curCenter.centerX)




	# Yellow Center
	# Middle Bar

	x = 0
	for z in range(left + 1, right):

		if z != 0:
			
			smallMess = False

		
			curCenter = None
			for cube in cubes:
				if cube.originalCenterX == x and cube.originalCenterZ == z and cube.originalCenterY == left:
					curCenter = cube
					break




			curCenter.originalCenterX, curCenter.originalCenterZ = curCenter.originalCenterZ, curCenter.originalCenterX





			if curCenter.centerY == left:

				turnX = curCenter.centerX

				turnCubes(cubes, 'x', -realChange, turnX)

				turnY = curCenter.centerY

				if curCenter.centerX == 0 and curCenter.centerY == 0:

					turnCubes(cubes, 'y', realChange, turnY)
					turnCubes(cubes, 'x', realChange, turnX)
					turnCubes(cubes, 'y', realChange, turnY)



				else:

					while curCenter.centerX == turnX:
						turnCubes(cubes, 'z', realChange, left)

					turnCubes(cubes, 'x', realChange, turnX)

			



			elif curCenter.centerZ == right and (curCenter.centerY != curCenter.originalCenterZ or curCenter.centerX != curCenter.originalCenterX):
				
				if smallMess:
					turnCubes(cubes, 'z', realChange, right)

				turnCubes(cubes, 'y', realChange, curCenter.centerY)
				turnCubes(cubes, 'y', realChange, curCenter.centerY)

				if smallMess:
					turnCubes(cubes, 'z', -realChange, right)


			else:


				turnY = curCenter.centerY
				totalMoves = 0
				while curCenter.centerZ != left:

					turnCubes(cubes, 'y', realChange, turnY)
					totalMoves += 1



				if smallMess:

					while curCenter.centerY == turnY:
						turnCubes(cubes, 'z', realChange, left)

					for i in range(totalMoves):
						turnCubes(cubes, 'y', -realChange, turnY)

			if curCenter.centerY != curCenter.originalCenterZ or curCenter.centerX != curCenter.originalCenterX or curCenter.centerZ != right:
				if curCenter.centerZ != left:
					print(curCenter.centerZ)

				while -curCenter.centerX != curCenter.originalCenterX or -curCenter.centerY != curCenter.originalCenterZ:
   
					turnCubes(cubes, 'z', -realChange, left)

				turnCubes(cubes, 'y', realChange, curCenter.centerY)
				turnCubes(cubes, 'y', realChange, curCenter.centerY)


			curCenter.originalCenterX, curCenter.originalCenterZ = curCenter.originalCenterZ, curCenter.originalCenterX

			turnX = curCenter.centerX

			turnCubes(cubes, 'x', -realChange, turnX)

			basicTurns(cubes, right, ['D', 'D'])

			turnCubes(cubes, 'x', realChange, turnX)

	basicTurns(cubes, right, ['D'])

	# All But Middle Bars

	for x in range(left + 1, right):
		for z in range(left + 1, right):

			if x != 0:
				smallMess = z != left + 1

			
				curCenter = None
				for cube in cubes:
					if cube.originalCenterX == x and cube.originalCenterZ == z and cube.originalCenterY == left:
						curCenter = cube
						break





				if curCenter.centerY == left:

					turnX = curCenter.centerX

					turnCubes(cubes, 'x', -realChange, turnX)

					turnY = curCenter.centerY

					if curCenter.centerX == 0 and curCenter.centerY == 0:

						turnCubes(cubes, 'y', realChange, turnY)
						turnCubes(cubes, 'x', realChange, turnX)
						turnCubes(cubes, 'y', realChange, turnY)



					else:

						while curCenter.centerX == turnX:
							turnCubes(cubes, 'z', realChange, left)

						turnCubes(cubes, 'x', realChange, turnX)

				



				elif curCenter.centerZ == right and (curCenter.centerY != curCenter.originalCenterZ or curCenter.centerX != curCenter.originalCenterX):

					if smallMess:
						turnCubes(cubes, 'z', realChange, right)

					turnCubes(cubes, 'y', realChange, curCenter.centerY)
					turnCubes(cubes, 'y', realChange, curCenter.centerY)

					if smallMess:
						turnCubes(cubes, 'z', -realChange, right)


				else:


					turnY = curCenter.centerY
					totalMoves = 0
					while curCenter.centerZ != left:

						turnCubes(cubes, 'y', realChange, turnY)
						totalMoves += 1



					if smallMess:

						while curCenter.centerY == turnY:
							turnCubes(cubes, 'z', realChange, left)

						for i in range(totalMoves):
							turnCubes(cubes, 'y', -realChange, turnY)

				if curCenter.centerY != curCenter.originalCenterZ or curCenter.centerX != curCenter.originalCenterX or curCenter.centerZ != right:

					if curCenter.centerZ != left:
						print(curCenter.centerZ)

					while -curCenter.centerX != curCenter.originalCenterX or curCenter.centerY != curCenter.originalCenterZ:

						turnCubes(cubes, 'z', -realChange, left)

					turnCubes(cubes, 'y', realChange, curCenter.centerY)
					turnCubes(cubes, 'y', realChange, curCenter.centerY)




		turnX = curCenter.centerX

		turnCubes(cubes, 'x', -realChange, turnX)

		basicTurns(cubes, right, ['D', 'D'])

		turnCubes(cubes, 'x', realChange, turnX)

		if x != 1:
			basicTurns(cubes, right, ['D', 'D'])


	# GREEN CENTER
	# MIDDLE LINE
	x = 0
	for cube in cubes:
		if cube.originalCenterX == 0 and cube.originalCenterZ == right and cube.originalCenterY == 0:
			while cube.centerZ != right:
				turnCubes(cubes, 'y', realChange, 0)
	for y in range(left + 1, right):
		if y != 0:
			curCenter = None
			for cube in cubes:
				if cube.originalCenterX == x and cube.originalCenterY == y and cube.originalCenterZ == right:
					curCenter = cube
					break

			if not curCenter.solved():
				if -curCenter.centerY == curCenter.originalCenterY and curCenter.centerX == curCenter.originalCenterX and curCenter.centerZ == right:
					turnCubes(cubes, 'y', realChange, curCenter.centerY)
					turnCubes(cubes, 'x', realChange, left)
					turnCubes(cubes, 'x', realChange, left)

				else:
					basicTurns(cubes, right, ['F'])
			
					if curCenter.centerZ == right:

						turnCubes(cubes, 'y', realChange, curCenter.centerY)

						while curCenter.centerY != curCenter.originalCenterY:
							turnCubes(cubes, 'x', realChange, left)

		

					else:

						while curCenter.centerY != curCenter.originalCenterY:
							centerAxis = curCenter.findAxisOfSurface(0, right)
							turnCubes(cubes, centerAxis[0], realChange, centerAxis[1])

						while curCenter.centerX != left:
							turnCubes(cubes, 'y', realChange, curCenter.centerY)
				
					basicTurns(cubes, right, ['F\''])

				turnCubes(cubes, 'y', -realChange, curCenter.centerY)

	# ALL OTHER LINES
	realChange = 10

	for x in range(left + 1, right):
		for y in range(left + 1, right):
			if x != 0:
				curCenter = None
				for cube in cubes:
					if cube.originalCenterX == x and cube.originalCenterY == y and cube.originalCenterZ == right:
						curCenter = cube
						curCenter.colors = [BLACK]
						break

				basicTurns(cubes, right, ['F'])

				if curCenter.centerZ == right:

					turnCubes(cubes, 'y', realChange, curCenter.centerY)
					turnCubes(cubes, 'y', realChange, curCenter.centerY)


				elif curCenter.centerZ != left:

					turn = 'R' if curCenter.centerY < 0 else 'R\''

					otherTurn = 'R' if turn == 'R\'' else 'R\''

					basicTurns(cubes, right, [turn])

					count = 0

					turnY = curCenter.centerY

					while curCenter.centerZ != left:
						count += 1
						turnCubes(cubes, 'y', realChange, turnY)

					surface = curCenter.findAxisOfSurface(0, right)
					
					while curCenter.centerY != curCenter.originalCenterY:
						turnCubes(cubes, surface[0], realChange, surface[1])

					for i in range(count):
						turnCubes(cubes, 'y', -realChange, turnY)

					basicTurns(cubes, right, [otherTurn])

				basicTurns(cubes, right, ['F\''])
				while -curCenter.centerX != curCenter.originalCenterX or curCenter.centerY != curCenter.originalCenterY:
					basicTurns(cubes, right, ['B'])

				turnY = curCenter.centerY

				firstMove = ['R']
				secondMove = ['R\'']
				if y == right - 1:
					firstMove, secondMove = secondMove, firstMove

				turnCubes(cubes, 'y', realChange, turnY)
				basicTurns(cubes, right, ['R'])
				turnCubes(cubes, 'y', -realChange, turnY)
				basicTurns(cubes, right, ['R\''])





			else:
				break

			






		


async def main(sideLength):

	global BLACK, YELLOW, GREEN, RED, BLUE, ORANGE, WHITE, moveLstForSolved, show, solving, realChange

	moveLstForSolved = []
	show = True
	solving = False
	realChange = 10

	BLACK = (0, 0, 0)
	YELLOW = (1, 1, 0)
	GREEN = (0, 1, 0)
	RED = (1, 0, 0)
	BLUE = (0, 0, 1)
	ORANGE = (1, 0.647, 0)
	WHITE = (1, 1, 1)
	
	pygame.init()

	display = (600, 600)

	screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

	pygame.display.set_caption('Rubik\'s Cube Solver')

	cubes = []

	for i in range(0, sideLength ** 2):
		cubes.append(Piece(sideLength, i))

	for i in range(1, sideLength - 1):
		for k in range(i * (sideLength ** 2), (i * (sideLength ** 2)) + sideLength):
			cubes.append(Piece(sideLength, k))

		for k in range(1, sideLength - 1):
			cubes.append(Piece(sideLength, (i * (sideLength ** 2)) + (k * sideLength)))
			cubes.append(Piece(sideLength, ((i * (sideLength ** 2)) + ((k + 1) * sideLength)) - 1))

		for k in range((i + 1) * (sideLength ** 2) - sideLength, (i + 1) * (sideLength ** 2)):
			cubes.append(Piece(sideLength, k))

	for i in range((sideLength ** 2) * (sideLength - 1), sideLength ** 3):
		cubes.append(Piece(sideLength, i))


	# for i in range(0, sideLength ** 3):
	# 	cubes.append(Piece(sideLength, i))

	gluPerspective(45, (display[0]/display[1]), 0.1, 10000.0)

	glTranslatef(-1.5, -1.5, -20)

	glRotatef(40, 1, 1, 1)


	speed = 90

	moves = 20

	# moves = ['R', 'U', 'R\'', 'U\'', 'L', 'L\'', 'D', 'D\'', 'F', 'F\'', 'B', 'B\'']

	# scramble = []

	# for i in range(movesTotal):
	# 	scramble.append(random.choice(moves))

	# basicTurns(cubes, math.floor(sideLength/2), scramble)


	axes = ['x', 'y']

	allMoves = []

	oldAxis = 'z'

	for i in range(moves):

		axis = random.choice(axes)

		axes.remove(axis)

		axes.append(oldAxis)

		oldAxis = axis

		args = [cubes, axis, random.choice([-speed, speed]), random.randint(-math.floor(sideLength/2), math.floor(sideLength/2))]

		while args[-1] == 0:
			args = [cubes, axis, random.choice([-speed, speed]), random.randint(-math.floor(sideLength/2), math.floor(sideLength/2))]




			

		turnCubes(*args, show = False)

		if args[2] > 0:
			args[2] -= args[2] * 2

		else:
			args[2] += abs(args[2]) * 2

		allMoves.append(args)

		await asyncio.sleep(0)


	# Main loop
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				running = False

		await asyncio.sleep(0)

	# solveNxN(cubes, sideLength)

	solve3x3(cubes, sideLength)

	# input("Press enter to solve ")

	# allMoves.reverse()

	# for i in allMoves:
	# 	turnCubes(*i, show = True)




	clock = pygame.time.Clock()

	# cubes[0].rightTurn(1)




	while True:
		# clock.tick(60)
		glEnable(GL_DEPTH_TEST) 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				break

		
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		for cube in cubes:
			cube.draw()

		pygame.display.flip()



		glRotatef(1, 1, 1, 1)

		await asyncio.sleep(0)

	


# random.seed(1123)
asyncio.run(main(3))







		