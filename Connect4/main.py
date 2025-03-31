# !/usr/bin/python
import pygame
import copy
# from timeit import default_timer as timer
import asyncio
# pyautogui.screenshot('screen.png')


def evaluateBoard(board):
	evaluation = 0
	for y in range(len(board)):
		for x in range(len(board[y])):
			# if x == 3:
			# 	if board[y][x] == 1:
			# 		evaluation += 5

			if board[y][x] == 1:
				if check_row(x, y, board, 1, 3, True, True):
					evaluation += 5
			elif board[y][x] == 2:
				if check_row(x, y, board, 2, 3, True, False):
					evaluation -= 5

	return evaluation

def checkFutureTerminalNode(board, depth, curTurn, mulitplier):
	for move in range(1, 8):
		newBoard = copy.deepcopy(board)
		if check_guess(curTurn, move, newBoard):
			if check_win(curTurn, newBoard, False):
				return [True, move, (winVal * (depth + 1)) * mulitplier]

		newBoard = copy.deepcopy(board)
		if check_guess(curTurn + 1, move, newBoard):
			if check_win(curTurn + 1, newBoard, False):
				return [False, move]


	return None




def terminalNode(board):
	return [check_win(1, board, False), check_win(2, board, False), check_tie(turn)]



def convertBoard(curBoard):
	boardRepr = ''
	for row in curBoard:
		for piece in row:
			boardRepr += str(piece)

	return boardRepr

def minimax(board, depth, maximizingPlayer, alpha, beta, turn):
	terminalMove = None
	boardRepr = convertBoard(board)
	# while boardRepr in transpositionTable:
	# 	# depth -= 1
	# 	if terminalMove == None:
	# 		terminalMove = transpositionTable[boardRepr][1]
	# 	check_guess(1 if maximizingPlayer else 2, transpositionTable[boardRepr][1], board)
	# 	print(boardRepr)
	# 	maximizingPlayer = not maximizingPlayer
	# 	boardRepr = convertBoard(board)

	win1 = check_win(1, board, draw=False)
	win2 = check_win(2, board, draw=False)
	tie = check_tie(turn)

	if win1:
		return [winVal * depth, terminalMove]

	elif win2:
		return [-(winVal * depth), terminalMove]

	elif tie:
		return [0, terminalMove]

	elif depth == 0:
		return [evaluateBoard(board), terminalMove]

	if boardRepr in transpositionTable:
		return transpositionTable[boardRepr]
	if maximizingPlayer:
		value = float('-inf')
		bestMove = 0
		for column in [4, 3, 5, 2, 6, 1, 7]:
			newBoard = copy.deepcopy(board)
			if check_guess(1, column, newBoard):
				newVal = minimax(newBoard, depth - 1, not maximizingPlayer, alpha, beta, turn + 1)
				if newVal[0] > value:
					value = newVal[0]
					bestMove = column

				alpha = max(newVal[0], alpha)

				if beta <= alpha:
					return [value, bestMove]

	else:
		value = float('inf')
		bestMove = 0
		for column in [4, 3, 5, 2, 6, 1, 7]:
			newBoard = copy.deepcopy(board)
			if check_guess(2, column, newBoard):
				newVal = minimax(newBoard, depth - 1, not maximizingPlayer, alpha, beta, turn + 1)
				if newVal[0] < value:
					value = newVal[0]
					bestMove = column

				beta = min(newVal[0], beta)

				if beta <= alpha:
					return [value, bestMove]

	transpositionTable[boardRepr] = [value, bestMove]

	return [value, bestMove]







def write(msg, font, x, y, color):
	much_font = pygame.font.Font('freesansbold.ttf', font)
	much_text = much_font.render(msg, True, color)
	screen.blit(much_text, (x, y))

def clear():

    # os.system('clear')
    pass

def create_board():

	for i in range(6):
		board.append([0, 0, 0, 0, 0, 0, 0])
	return board



def check_guess(y, column, board):
	found = False
	for row in range(len(board) - 1, -1, -1):
		if board[int(row)][int(column) - 1] != 1 and board[int(row)][int(column) - 1] != 2:
			board[int(row)][int(column) - 1] = y
			found = True		
			break
		else:
			continue
	return found
def baddirection(direction, number, starting_point, curBoard, length = 3, check_block = False, block_number = None):
	l = 0
	for i in range(0,length):
		if direction == 1:
			if curBoard[starting_point[0]-1][starting_point[1]] ==  number:
				starting_point[0] -= 1
				l += 1  
			
			else:
				 pass
		if direction == 2:
			if curBoard[starting_point[0]+1][starting_point[1]-1] ==  number:
				starting_point[0] += 1
				starting_point[1] -= 1
				l += 1 
			
			else:
				 pass
		if direction == 3:

			if curBoard[starting_point[0]][starting_point[1]+1] ==  number:
				starting_point[1] += 1
				l += 1 
			
			else:
				 pass

		if direction == 4:
			if curBoard[starting_point[0] + 1][starting_point[1] + 1] == number:
				starting_point[0] += 1
				starting_point[1] += 1
				l += 1 
					
			else:
				pass

	blocked = False

	try:

		if check_block:
			if direction == 1:
				if curBoard[starting_point[0]-1][starting_point[1]] == block_number:
					starting_point[0] -= 1
					blocked = True 
				
				else:
					 pass
			if direction == 2:
				if curBoard[starting_point[0]+1][starting_point[1]-1] == block_number:
					starting_point[0] += 1
					starting_point[1] -= 1
					blocked = True
				
				else:
					 pass
			if direction == 3:

				if curBoard[starting_point[0]][starting_point[1]+1] == block_number:
					starting_point[1] += 1
					blocked = True
				
				else:
					 pass

			if direction == 4:
				if curBoard[starting_point[0] + 1][starting_point[1] + 1] == block_number:
					starting_point[0] += 1
					starting_point[1] += 1
					blocked = True
						
				else:
					pass

	except IndexError:
		blocked = True


	if starting_point[0] < 0 or starting_point[1] < 0 or blocked:
		l = -1

	return l == length


def direction(number, startX, startY, xChange, yChange, board, length, check_block, odd):
	try:
		curPosX = startX
		curPosY = startY
		block_number = 1 if number == 2 else 2
		for i in range(length):
			curPosX += xChange
			curPosY += yChange
			if board[curPosY][curPosX] != number:
				return False

		if check_block:
			curPosX += xChange
			curPosY += yChange
			if board[curPosY][curPosX] == block_number or (curPosY % 2 == 0 and odd) or (curPosY % 2 == 1 and not odd) or curPosX == startX:
				return False

		if curPosX >= 0 and curPosY >= 0:
			return True

	except IndexError:
		return False


def check_row(startX, startY, curBoard, number, length, check_block, odd):
	possibleChange = [[0, 1], [1, 0], [-1, 0], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

	for change in possibleChange:
		if direction(number, startX, startY, change[0], change[1], curBoard, length - 1, check_block, odd):
			return True

	return False



def check_win(turn, curBoard, draw = True):
	for y in range(6):
		for x in range(7):
			square = curBoard[y][x]
			if turn%2 == 1:
				if square == 1:
					if check_row(x, y, curBoard, 1, 4, False, None):
						if draw:
							write("Red WINS", 100, 0, 0, black)
						return True

			else:
				if square == 2:
					if check_row(x, y, curBoard, 2, 4, False, None):
						if draw:
							write("Yellow WINS", 100, 0, 0, black)
						
						return True

	return False
				 


def check_tie(turn):


	if turn == 42:
		return True

	return False


def create_pygameBoard(pick, color):
	screen.fill(white)
	for x in range(7):
		pygame.draw.rect(screen, (128, 128, 128), ((100 * x), 0, WIDTH/len(board[0]), HEIGHT))

			
	for y in range(len(board)):
		for x in range(len(board[y])):
			if board[y][x] == 1:
				pygame.draw.circle(screen, red, (100 * x + 50, 100 * y + 50), 50)
			elif board[y][x] == 2:
				pygame.draw.circle(screen, yellow, (100 * x + 50, 100 * y + 50), 50)
			else:
				pygame.draw.circle(screen, white, (100 * x + 50, 100 * y + 50), 50)
	if color != True:
		for row in range(len(board) - 1, -1, -1):
			if int(board[row][pick - 1]) == 0:
				pygame.draw.circle(screen, (color[0], color[1], color[2]), (100 * (pick - 1) + 50, 100 * row + 50), 50)
				break
		tint = pygame.Surface((WIDTH/len(board[0]), HEIGHT))
		tint.set_alpha(120)
		tint.fill(color)
		screen.blit(tint, ((100 * (pick - 1)), 0))





async def main():
	global board, transpositionTable, screen, WIDTH, HEIGHT, winVal, black, blue, red, yellow, white, running, totalMoveTime, turn, game_over

	blue = (0, 0, 255)
	black = (0, 0, 0)
	pygame.init()
	winVal = 10000000000000

	transpositionTable = {}

	WIDTH = 700
	HEIGHT = 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Connect 4")
	board = []

	board = create_board()

	


	clear()
	white = (255, 255, 255)
	red = (255, 0, 0)
	yellow = (255, 255, 0)

	running = True
	totalMoveTime = 0
	turn = 0
	game_over = False
	while running:
		mini_running = True

		if turn%2 == 0:
			transpositionTable = {}
			# start = timer()
			play = minimax(copy.deepcopy(board), 8, True, -float('inf'), float('inf'), turn)
			# end = timer()

			check_guess(1, play[1], board)
			turn += 1



		elif turn%2 == 1:
			newBoard = copy.deepcopy(board)

			player_2_pick = 1
			mini_running = True
			while mini_running:
				mouse = pygame.mouse.get_pos()
				click = pygame.mouse.get_pressed()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						mini_running = False
						running = False
				if mouse[0] > 600:
					player_2_pick = 7
				elif mouse[0] > 500:
					player_2_pick = 6
				elif mouse[0] > 400:
					player_2_pick = 5
				elif mouse[0] > 300:
					player_2_pick = 4
				elif mouse[0] > 200:
					player_2_pick = 3
				elif mouse[0] > 100:
					player_2_pick = 2
				elif mouse[0] > 0:
					player_2_pick = 1
				if click[0] == 1:
					if check_guess(2, player_2_pick, board) == True:

						turn += 1
						mini_running = False
					else:
						pass
				create_pygameBoard(player_2_pick, yellow)
				pygame.display.update()

				await asyncio.sleep(0)
				#for i in board:
					#print(i)
				# print(board)
				# player_1_pick = raw_input("Player 1, make your Selection. (1-7 from right to left) ")
				# player_1_pick = random.randint(0,7)

				# try:
				# 	if check_guess(1, player_1_pick) == True:
				# 		turn += 1
				# 		break
				# 	else:
				# 		print("Pick a valid number")
				# 		print('\n\n\n\n\n\n\n\n\n\n\n')
				# 		raw_input("Press enter to continue... ")
				# except:
				# 	print("Pick a Valid Number")
				# 	print('\n\n\n\n\n\n\n\n\n\n\n')
				# 	raw_input("Press enter to continue... ")
				# 	# clear()
		# else:
		# 	clear()
		# 	while True:
		# 		print(board)
		# 		player_1_pick = raw_input("Player 2, make your Selection. (1-7 from right to left) ")
		# 		# player_1_pick = random.randint(0,7)

		# 		try:
		# 			if check_guess(2, player_1_pick) == True:
		# 				turn += 1
		# 				break
		# 			else:
		# 				print("Pick a valid number")
		# 				print('\n\n\n\n\n\n\n\n\n\n\n')
		# 				raw_input("Press enter to continue... ")
		# 				break
		# 		except:
		# 			print("Pick a Valid Number")
		# 			print('\n\n\n\n\n\n\n\n\n\n\n')
		# 			raw_input("Press enter to continue... ")
		# 			clear()
		
		create_pygameBoard(-1, True)
		mini_running = True
		x = check_win(turn, board)
		if x == True:
			while mini_running:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						mini_running = False
						running = False
				check_win(turn, board)
				pygame.display.update()

				await asyncio.sleep(0)

		mini_running = True
		j = check_tie(turn)
		if j == True:
			while mini_running:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						mini_running = False
						running = False	
				write("TIE", 100, 0, 0, black)
				pygame.display.update()
			
			await asyncio.sleep(0)
		# for i in board:
			#print(i)
		# Pygame Add On
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		mini_running = True

		pygame.display.update()
		while mini_running:
			for event in pygame.event.get():
				if event == pygame.QUIT:
					mini_running = False
			mouse = pygame.mouse.get_pressed()
			#print(mouse)

			if mouse[0] == 0:
				mini_running = False
			pygame.display.update()
			await asyncio.sleep(0)


		mini_running = True

		await asyncio.sleep(0)

asyncio.run(main())




