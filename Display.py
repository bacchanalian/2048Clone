import pygame
import sys
from pygame.locals import *
from time import sleep
from random import randint

# definition of main structure
map_size = 4
map = [[0 for x in range(map_size)] for y in range(map_size)]
map1 = map2 = map3 = map4 = map5 = map
block = []

pygame.init()
pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DGREY = (60, 60, 50)
DDGREY = (25, 25, 25)
LGREY = (110, 110, 110)
LLGREY = (160, 160, 160)
LLBROWN = (140, 70, 20)
ORANGE = (210, 105, 30)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (170, 170, 0)
BYELLOW = (255, 250, 30)

numcolor = {1: BLACK, 2: DDGREY, 4: DDGREY, 8: WHITE, 16: WHITE, 32: WHITE, 64: WHITE, 128: WHITE, 256: WHITE, 1024: WHITE, 2048 : WHITE, 4096: WHITE, 8192: WHITE}
boxcolor = {0: LLGREY,1: LGREY, 2: LGREY, 4: LLBROWN, 8: LLBROWN, 16: ORANGE, 32: ORANGE, 64: RED, 128: RED, 256: YELLOW, 1024: YELLOW, 2048 : BYELLOW, 4096: BYELLOW, 8192: BLACK}

xL = len(map[0]) # columns
yL = len(map)    #rows
xsizew = 16 + 121*xL
ysizew = 16 + 121*xL
DISPLAY=pygame.display.set_mode((xsizew,ysizew),0,32)
myfont = pygame.font.Font(None, 60)

#Functions

def open_screen():
    DISPLAY.fill(DGREY)
    pygame.draw.rect(DISPLAY, LGREY, (16, 16, 130, 100), 0)
    openfont = pygame.font.Font(None, 40)
    welcome = openfont.render("Welcome", True, WHITE)
    tothe = openfont.render("to the", True, WHITE)
    game = openfont.render("Game!", True, WHITE)
    DISPLAY.blit(welcome, (20, 25))
    DISPLAY.blit(tothe, (37, 50))
    DISPLAY.blit(game, (32, 77))
    #Controls
    controlfont = pygame.font.Font(None, 30)
    control = controlfont.render("Controls", True, WHITE)
    DISPLAY.blit(control, (60, 150))
    direc = controlfont.render("Direction keys and WASD - Moves tiles", True, WHITE)
    DISPLAY.blit(direc, (60, 170))
    undo = controlfont.render("Backspace and U - Undo last 5 moves", True, WHITE)
    DISPLAY.blit(undo, (60, 190))
    reset = controlfont.render("R - Reset game", True, WHITE)
    DISPLAY.blit(reset, (60, 210))
    block = controlfont.render("B - Add block to random position", True, WHITE)
    DISPLAY.blit(block, (60, 230))
    block1 = controlfont.render("in order to increase difficulty", True, WHITE)
    DISPLAY.blit(block1, (95, 250))
    #Press Space
    spacefont = pygame.font.Font(None, 40)
    space = spacefont.render("Press Space to Begin", True, WHITE)
    DISPLAY.blit(space, (175, 375))
    #show
    pygame.display.flip()

def score(matrix):
    L = len(map[0])  # columns
    H = len(map)  # rows
    scorenum = 0
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            if matrix[i][j] > scorenum:
                scorenum = matrix[i][j]
    return scorenum

def kill_screen():
    DISPLAY.fill(DGREY)
    #game over
    gameoverfont = pygame.font.Font(None, 50)
    gameover = gameoverfont.render("Game Over", True, WHITE)
    DISPLAY.blit(gameover, (60, 150))
    #score
    scorefont = pygame.font.Font(None, 30)
    scoretext = scorefont.render("Your score is %d" % score(map), True, WHITE)
    DISPLAY.blit(scoretext, (100, 200))
    #press r to reset
    spacefont = pygame.font.Font(None, 40)
    reset = spacefont.render("Press r to Reset or click X to close", True, WHITE)
    DISPLAY.blit(reset, (175, 375))
    pygame.display.flip()

def redraw(matrix, doubled):
    templist = doubled[:] #lists aren't copied and are mutable or something and not global/local
    DISPLAY.fill(DGREY)
    L = len(matrix[0])  # columns
    H = len(matrix)  # rows
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            #set variables
            xlength = ylength = 105
            xpos = 16 + 121*j
            ypos = 16 + 121*i
            num = map[i][j]
            #draw rectangles
            if [i,j] in templist:    #for now we depict blocked as being black
                pygame.draw.rect(DISPLAY, BLACK, (xpos, ypos, xlength, ylength), 0)
                continue
            pygame.draw.rect(DISPLAY, boxcolor[num], (xpos, ypos, xlength, ylength), 0)
            if num == 0:            #don't add text to position with zero
                continue
            else:
            #draw text
                text = myfont.render(str(num), True, numcolor[num])
                DISPLAY.blit(text, (xpos + 42, ypos + 35))
    templist.append([1,1])
    #use templist instead of doubled or block
    #templist = []
    pygame.display.flip()

def up(matrix, doubled):
    templist = doubled[:]   #lists aren't copied and are mutable or something and not global/local
    temparray = [row[:] for row in matrix]
    L = len(temparray[0])      #columns
    H = len(temparray)         #rows
    i = 1
    while(i<=H-1):            #ends after bottom row
        cursor_return = 0   #variable to note whether return is necessary
        if i > 0:       #make it so nothing happens when cursor is at top most row
            for j in range(0, L, 1):    #start counting along columns to the right
                if temparray[i][j] == 0:   #go to next column if this is 0
                    continue
                if [i, j] in templist or [i-1, j] in templist:  #go to next column if block, position or next position above has previously been doubled
                    continue
                if temparray[i-1][j] == temparray[i][j]:              #same value with next position above
                    temparray[i-1][j] += temparray[i][j]              #add to position above
                    temparray[i][j] = 0                            #make current position empty
                    templist.append([i-1, j])                   #note that the next position above has been doubled
                if temparray[i-1][j] == 0:                         #if next position above is empty
                    temparray[i-1][j] += temparray[i][j]              #add current to next position above
                    temparray[i][j] = 0                            #set current to empty
                    cursor_return = -2                          #note that we ought to return one position
                #how to end for loop?
            #redraw after every cursor move
            #just so i can see it, this is pretty slow
        i = i + 1
        i = i + cursor_return
    return temparray

def down(matrix, doubled):
    templist = doubled[:]   #lists aren't copied and are mutable or something and not global/local
    temparray = [row[:] for row in matrix]
    L = len(temparray[0])      #columns
    H = len(temparray)         #rows
    i = H-2
    while(i>=0):            #ends after bottom row
        cursor_return = 0   #variable to note whether return is necessary
        if i < H-1:       #make it so nothing happens when cursor is at bottom row
            for j in range(0, L, 1):    #start counting along columns to the right
                if temparray[i][j] == 0:   #go to next column if this is 0
                    continue
                if [i, j] in templist or [i+1, j] in templist:  #go to next column if block, position or next position above has previously been doubled
                    continue
                if temparray[i+1][j] == temparray[i][j]:              #same value with next position above
                    temparray[i+1][j] += temparray[i][j]              #add to position above
                    temparray[i][j] = 0                            #make current position empty
                    templist.append([i+1, j])                   #note that the next position above has been doubled
                if temparray[i+1][j] == 0:                         #if next position above is empty
                    temparray[i+1][j] += temparray[i][j]              #add current to next position above
                    temparray[i][j] = 0                            #set current to empty
                    cursor_return = 2                          #note that we ought to return one position
                #how to end for loop?
            #redraw after every cursor move
            #just so i can see it, this is pretty slow
        i = i - 1
        i = i + cursor_return
    return temparray

def left(matrix, doubled):
    templist = doubled[:]   #lists aren't copied and are mutable or something and not global/local
    temparray = [row[:] for row in matrix]
    L = len(temparray[0])      #columns
    H = len(temparray)         #rows
    j = 1
    while(j<=L-1):            #ends after first column
        cursor_return = 0   #variable to note whether return is necessary
        if j > 0:       #make it so nothing happens when cursor is at the left most column
            for i in range(0, H, 1):    #start counting down rows
                if temparray[i][j] == 0:   #go to next row if this is 0
                    continue
                if [i, j] in templist or [i, j-1] in templist:  #go to next row if block, position or next position to right has previously been doubled
                    continue
                if temparray[i][j-1] == temparray[i][j]:              #same value with next position to right
                    temparray[i][j-1] += temparray[i][j]              #add to position at right
                    temparray[i][j] = 0                            #make current position empty
                    templist.append([i, j-1])                   #note that the next position to right has been doubled
                if temparray[i][j-1] == 0:                         #if next position to right is empty
                    temparray[i][j-1] += temparray[i][j]              #add current to next position to right
                    temparray[i][j] = 0                            #set current to empty
                    cursor_return = -2                          #note that we ought to return one position
                #how to end for loop?
            #redraw after every cursor move
            #just so i can see it, this is pretty slow
        j = j + 1                                               #move down one
        j = j + cursor_return
    return temparray

def right(matrix, doubled):
    templist = doubled[:]
    temparray = [row[:] for row in matrix]
    L = len(temparray[0]) #columns
    H = len(temparray)    #rows
    j = L - 2
    while(j>=0): #ends after first column
        cursor_return = 0 #variable to note whether return is necessary
        if j < L - 1: #make it so nothing happens when cursor is at the right most column
            for i in range(0, H, 1):    #start counting down rows
                if temparray[i][j] == 0:    #go to next row if this is 0
                    continue
                if [i, j] in templist or [i, j+1] in templist:    #go to next row if block, position or next position to right has previously been doubled
                    continue
                if temparray[i][j+1] == temparray[i][j]:              #same value with next position to right
                    temparray[i][j+1] += temparray[i][j]              #add to position at right
                    temparray[i][j] = 0                            #make current position empty
                    templist.append([i, j+1])                      #note that the next position to right has been doubled
                if temparray[i][j+1] == 0:                         #if next position to right is empty
                    temparray[i][j+1] += temparray[i][j]                #add current to next position to right
                    temparray[i][j] = 0                            #set current to empty
                    cursor_return = 2                           #note that we ought to return one position
                #how to end for loop?
            #redraw after every cursor move
            #sleep(0.25) #just so i can see it, this is pretty slow
        j = j - 1
        j = j + cursor_return
    return temparray

def add(matrix, num):
    temparray = [row[:] for row in matrix]
    L = len(matrix[0])  #columns
    H = len(matrix)     #rows
    list = []
    if full(matrix):
        print("full, cannot add")
        return matrix
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            if (matrix[i][j] > 0) or ([i, j] in block):
                continue
            list.append([i, j])
    e = list[randint(0, len(list) - 1)]
    ex = e[0]
    ey = e[1]
    temparray[ex][ey] = num         #add num in random empty location
    #redraw(temparray, block)       #can't get internal redrawing to start at the right time
    return temparray

def addBlock(matrix, doubled):
    templist = doubled[:]
    L = len(matrix[0])  #columns
    H = len(matrix)     #rows
    list = []
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            if (matrix[i][j] == 0) & ([i, j] not in block):
                list.append([i, j])
    l_index = len(list) -1
    if l_index > 0:
        templist.append(list[randint(0, l_index)]) #add block in random empty location
    return templist

def full(matrix):
    L = len(matrix[0])  #columns
    H = len(matrix)     #rows
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            if (matrix[i][j] == 0) & ([i, j] not in block):
                return False
    return True

def canmove(matrix):
    L = len(matrix[0])  #columns
    H = len(matrix)     #rows
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            if (matrix[i][j] == 0) & ([i, j] not in block):
                return True
    if (matrix == right(matrix, block)) & (matrix == left(matrix, block)) & (matrix == up(matrix, block)) & (matrix == down(matrix, block)):
        return False
    return True

def reset():
    L = len(map[0])  # columns
    H = len(map)  # rows
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            map[i][j] = 0
            map1[i][j] = 0
            map2[i][j] = 0
            map3[i][j] = 0
            map4[i][j] = 0
            map5[i][j] = 0
    del block[:]

#Functions

open_screen()

while True:
    if not canmove(map):
        sleep(1)
        kill_screen() #press r to reset, or click x to close
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            condition1 = False
            if (event.key == pygame.K_BACKSPACE) or (event.key == pygame.K_u):
                map = map1
                map1 = map2
                map2 = map3
                map3 = map4
                map4 = map5
                redraw(map, block)
                continue
            map5 = map4
            map4 = map3
            map3 = map2
            map2 = map1
            map1 = map
            if event.key == pygame.K_r:  #resets the game
                reset()
                condition1 = True
            if event.key == pygame.K_SPACE: #starts the game
                condition1 = True
            if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                map = left(map, block)
                redraw(map, block)
                condition1 = True
                #continue
            if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                map = right(map, block)
                redraw(map, block)
                condition1 = True
            if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                map = up(map, block)
                redraw(map, block)
                condition1 = True
            if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                map = down(map, block)
                redraw(map, block)
                condition1 = True
            #if event.key == pygame.K_s:
                # save as txt file
                # function must have error handling
            #if event.key == pygame.K_l:
                #map, map1, map2, map3, map4, map5 = load()
                # load from txt file
                # function must have error handling
            if event.key == pygame.K_b:
                block = addBlock(map, block)
                redraw(map, block)
            if condition1:
                sleep(0.5)
                map = add(map, 1)
                redraw(map, block)