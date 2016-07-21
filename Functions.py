'''
Functions
Right
Left
Up
Down
Add
Full
'''
from random import randint
from time import sleep
#import Display

# definition of main structure
map = [[0 for x in range(4)] for y in range(4)]
#map = add(map, 2) #what's wrong with this command?
map1 = map2 = map3 = map4 = map5 = map

#test cases
block = []
map = [[2,4,16,0],[4,8,4,8],[8,16,0,16],[16,4,16,4]]
'''
map[0][0] = 4
map[0][2] = 2
map[0][3] = 2
#map[0][5] = 8
map[1][0] = 2
map[1][2] = 2
map[2][0] = 2
'''
block.append([2, 2])
#block.append([0, 2])
#Right, takes in matrix, returns matrix

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
            #redraw(matrix, block) #redraw after every cursor move
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
            #redraw(matrix, block) #redraw after every cursor move
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
            #redraw(matrix, block) #redraw after every cursor move
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
            #redraw(matrix, block) #redraw after every cursor move
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
            if (matrix[i][j] == 0) & ([i, j] not in block):
                list.append([i, j])
    ex = list[randint(0, len(list) - 1)][0]
    ey = list[randint(0, len(list) - 1)][1]
    temparray[ex][ey] = num #add num in random empty location
    #redraw(map, block)
    return temparray


def addBlock(matrix, doubled):
    L = len(matrix[0])  #columns
    H = len(matrix)     #rows
    list = []
    for i in range(0, H, 1):
        for j in range(0, L, 1):
            if matrix[i][j] == 0:
                list.append([i, j])
    doubled.append(list[randint(0, len(list) - 1)]) #add block in random empty location
    return doubled

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

if full(map):
    print("matrix is full")
if not full(map):
    print("matrix is not full")

'''
if canmove(map):
    print("matrix can move")
if not canmove(map):
    print("matrix cannot move")
'''