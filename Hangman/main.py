import pygame
import asyncio


def write(msg, font, x, y):
    much_font = pygame.font.Font('freesansbold.ttf', font)
    much_text = much_font.render(msg, True, (0, 0, 0))
    screen.blit(much_text, (x, y))



def showLines():
    global dashX, dashY, numberOfLetters, word, y, numberOfLettersReset, numberOfDashes
    if numberOfLetters > 80:
        write("No more letters", 64, 0, 0)
    else:
        if numberOfLettersReset > 19:
            numberOfLettersReset = 0
            y += 40
    for i in range(numberOfDashes):
        screen.blit(dashImg[i], (dashX[i], dashY[i]))

def create_drawing():
    pygame.draw.line(screen, (0, 0, 0), (100, 350), (200, 350))
    pygame.draw.line(screen, (0, 0, 0), (150, 350), (150, 200))
    pygame.draw.line(screen, (0, 0, 0), (150, 200), (225, 200))
    pygame.draw.line(screen, (0, 0, 0), (225, 200), (225, 225))
    if incorrect_letters > 0:
        pygame.draw.circle(screen, black, (225, 237), 13, 1)
        if incorrect_letters > 1:
            pygame.draw.line(screen, black, (225, 250), (225, 275))
            if incorrect_letters > 2:
                pygame.draw.line(screen, black, (225, 250), (238, 263))
                if incorrect_letters > 3:
                    pygame.draw.line(screen, black, (225, 250), (213, 263))
                    if incorrect_letters > 4:
                        pygame.draw.line(screen, black, (225, 275), (238, 288))
                        if incorrect_letters > 5:
                            pygame.draw.line(screen, black, (225, 275), (212, 288))
                            if incorrect_letters > 6:
                                pygame.draw.circle(screen, black, (229, 234), 2)
                                if incorrect_letters > 7:
                                    pygame.draw.circle(screen, black, (221 , 234), 2)
                                    if incorrect_letters > 8:
                                        pygame.draw.line(screen, black, (222, 243), (228, 243))

# def button(x, y, w, h, ac, ic, letter):
# 	mouse = pygame.mouse.get_pos()
# 	click = pygame.mouse.get_pressed()
# 	if x + w > mouse[0] > x and y + h > mouse[1] > y:

def button(x,y,w,h,ic,ac,letter):
    global used_letters, incorrect_letters, correct_count
    if incorrect_letters != 9 and correct_count != len(word):
        correct = False
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(mouse)
        # print(click)
        stop = False
        for i in used_letters:
            if i == letter:
                stop = True
        if stop:
            pygame.draw.rect(screen, ic, (0, 0, 0, 0))
            # print("stop "+ letter)
            pass
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
            if x+w > mouse[0] > x and y+h > mouse[1] > y:
                pygame.draw.rect(screen, ac, (x, y, w, h))
                if click[0] == 1:
                    guessed_letters.append(letter)
                    used_letters.append(letter)
                    for i in range(len(word)):
                        if letter == word[i]:
                            write(letter, 32, dashX[i] + 7, dashY[i] - 20)
                            correct_count += 1
                            correct = True
                    if correct == True:
                        pass
                    else:
                        incorrect_letters += 1


                    used_letters.append(letter)
                        # print(used_letters)
                    # if click[0] == 1:
                    # 	while True:
                    # 		click = pygame.mouse.get_pressed()
                    # 		print("loop")
                    # 		print(click)
                    # 		if click[0] == 1:
                    # 			break

        much_font = pygame.font.Font('freesansbold.ttf', 32)
        much_text = much_font.render(letter.upper(), True, (0, 0, 0))
        text_rect = much_text.get_rect(center= (x+w/2, (y+h/2)))
        screen.blit(much_text, text_rect)


def writeLettersAndLines():
    
    showLines()
    create_drawing()
    iteration = 0
    for i in range(len(word)):
        for j in guessed_letters:
            if j == word[i]:
                write(word[i], 32, dashX[i] + 7, dashY[i] - 20)




# Create word function
async def main():

    global numberOfLetters, y, numberOfLettersReset, numberOfDashes, quit, end
    global word, letters, icon, dashImg, black, dashY, dashX, red, bright_red, numberOfLetters, numberOfDashes, numberOfLettersReset
    global word, y, incorrect_letters, guessed_letters, used_letters, end, correct_count, quit, font, y, change, exit
    global screen

    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] 
    # Screen
    icon = pygame.image.load('hangman.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Hangman")
    dashImg = []
    black =  (0, 0, 0)
    dashY = []
    dashX = []
    red = [200, 0, 0]
    bright_red = [255, 0, 0]
    
    numberOfLetters = 0
    numberOfLettersReset = 0
    numberOfDashes = 0
    word = ''
    y = 400
    incorrect_letters = 0
    guessed_letters = []
    used_letters = []
    end = "NONE"
    correct_count = 0
    quit = False

    font = 45
    y = 600
    change = 55
    exit = False
    for i in range(y+change*7 - 300):
        screen.fill((255, 255, 255))
        if exit:
            pass
        else:
            write("The rules of this game simple." ,font , 0, y)
            write("One person writes a word or phrase.", font, 0, y + change)
            write("He presses Enter and then the next", font, 0, y + change*2)
            write("player tries to guess the word by", font, 0, y + change*3)
            write("pressing the buttons. If he gets the", font, 0, y + change*4)
            write("before a man gets fully drawn,", font, 0, y + change*5)
            write("he wins. If he doesn't. The other", font, 0, y + change*6)
            write("player wins", font, 0, y+change*7)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exit = True
        
        await asyncio.sleep(0)
                
                
        y -= 1


    y = 400
    quit = False
    recent_event = []

    running = True
    while running and quit == False:
        screen.fill((255, 255, 255))
        writeLettersAndLines()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                if event.key == pygame.K_BACKSPACE:
                    try:
                        if recent_event[-1] == "Letter":
                            dashImg.pop(-1)
                            numberOfDashes -= 1
                            dashX.pop(-1)
                            dashY.pop(-1)
                            word = word[0:-1]
                        numberOfLettersReset -= 1
                        numberOfLetters -= 1
                        recent_event.pop(-1)
                    except IndexError:
                        pass
                for letter in letters:
                    if event.unicode.lower() == letter:
                        recent_event.append("Letter")
                        word += letter
                        # print(word, numberOfLetters)
                        dashImg.append(pygame.image.load('minus.png'))
                        numberOfDashes += 1
                        dashX.append((1 + numberOfLetters * 40)%800)
                        dashY.append(y)
                        numberOfLettersReset += 1
                        numberOfLetters += 1

                        # print(numberOfLetters, dashX, dashY)
                if event.key == pygame.K_SPACE:
                    recent_event.append("Space")
                    numberOfLetters += 1
                    numberOfLettersReset += 1



        showLines()
        pygame.display.update()
    if quit == False:
        running = True
        while running:
            screen.fill((255, 255, 255))
            letterX = 30
            letterY = 30
            # print(len(letters))
            for i in range(len(letters)):
                # print(i)

                button(letterX, letterY, 40, 40, red, bright_red, letters[i])
                letterX += 40
                if i == 18:
                    # print('change')
                    letterY += 40
                    letterX = 30
            # for i in used_letters:
            # 	try:
            # 		letters.remove(i)
            # 	except:

            # 		pass

            # pygame.draw.rect(screen, red, (30, 33232232, 33232323, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if correct_count == len(word) or end == "yes":
                write("The player who guessed ", 64, 0, 428)
                write("wins the game", 64, 0, 492)
                end = "yes"
                for i in letters:
                    guessed_letters.append(i)
            elif incorrect_letters >= 9 or end == "no":
                write("The player who made the ", 64, 0, 428)
                write("word wins the game", 64, 0, 492)
                end = "no"
                for i in letters:
                    guessed_letters.append(i)
            write("Incorrect Letters: " + str(incorrect_letters), 32, 400, 100)
            writeLettersAndLines()
            pygame.display.update()
            await asyncio.sleep(0)



        # running = True
        # while running:
        # 	pass







asyncio.run(main())