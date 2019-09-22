#import sys
#sys.setrecursionlimit(10000) # 10000 is an example, try with different value

import random
import numpy

def generateTable(n):
    print("Initializing table...")
    table = numpy.zeros((n, n))
    for i in range(n):
        for j in range(n):
            table[i][j] = random.randint(1, 5)
    return table

def printTable(table):
    print("Printing table...")
    for i in range(len(table)):
        for j in range(len(table)):
            print(int(table[i][j]), end=" ")
        print()


class Movement():
    def __init__(self, previousPos, currentPos):
        self.previousPos = previousPos
        self.currentPos = currentPos

    def __str__(self):
        print("current: {}".format(self.currentPos), end=" ")

class ColorGroup():
    def __init__(self, colorNumber, positions):
        self.positions = positions
        self.colorNumber = colorNumber

    def __str__(self):
        print("color:", self.colorNumber, ", size: ",len(self.positions),"\npositions-> ", end="")
        for position in self.positions:
            print(position, end=" ")
        print("\n")


def isInvalidMovement(movement, n):
    return movement[0] < 0 or  movement[1] < 0 or movement[0] > (n - 1) or movement[1] > (n - 1)

def existPosition(group_list, position):
    for group in group_list:
        for pos in group.positions:
            if pos == position:
                return True
    return False

def moveLeft(movement, n):
    next_pos = [movement.currentPos[0], (movement.currentPos[1] - 1)]

    if movement.previousPos is None:
        if isInvalidMovement(next_pos, n):
            return None
    elif next_pos[1] == movement.previousPos[1] or isInvalidMovement(next_pos, n):
        return None
    return Movement(movement.currentPos, next_pos)

def moveRigth(movement, n):
    next_pos = [movement.currentPos[0], (movement.currentPos[1] + 1)]

    if movement.previousPos is None:
        if isInvalidMovement(next_pos, n):
            return None
    elif next_pos[1] == movement.previousPos[1] or isInvalidMovement(next_pos, n):
        return None
    return Movement(movement.currentPos, next_pos)

def moveUp(movement, n):
    next_pos = [(movement.currentPos[0] - 1), movement.currentPos[1]]

    if movement.previousPos is None:
        if isInvalidMovement(next_pos, n):
            return None
    elif next_pos[0] == movement.previousPos[0] or isInvalidMovement(next_pos, n):
        return None
    return Movement(movement.currentPos, next_pos)

def moveDown(movement, n):
    next_pos = [(movement.currentPos[0] + 1), movement.currentPos[1]]
    if movement.previousPos is None:
        if isInvalidMovement(next_pos, n):
            return None
    elif next_pos[0] == movement.previousPos[0] or isInvalidMovement(next_pos, n):
        return None
    return Movement(movement.currentPos, next_pos)


def getPossibleMovements(movement, n):
    movements_to_do = []

    move = moveUp(movement, n)
    if move is not None:
        movements_to_do.append(move)

    move = moveRigth(movement, n)
    if move is not None:
        movements_to_do.append(move)

    move = moveDown(movement, n)
    if move is not None:
        movements_to_do.append(move)

    move = moveLeft(movement, n)
    if move is not None:
        movements_to_do.append(move)

    return movements_to_do

def makeGroups(table):
    group_list = []
    for i in range(len(table)):
        for j in range(len(table)):
            visited_elements = []
            pos = [i, j]

            if not existPosition(group_list, pos):
                group_by = table[i][j]
                algorithm(table, group_by, Movement(None, pos), visited_elements)
                group_list.append(ColorGroup(group_by, visited_elements))

    return group_list

def algorithm(table, group_by, move, movements_made):
    tmp_element = table[move.currentPos[0]][move.currentPos[1]]

    if move.currentPos not in movements_made and tmp_element == group_by:
        movements_made.append(move.currentPos)
        next_movements = getPossibleMovements(move, len(table))

        for next_movement in next_movements:
            algorithm(table, group_by, next_movement, movements_made)


def getPositionGroup(group_list, position):
    for i in range(len(group_list)):
        if position in group_list[i].positions:
            return i

def touchPosition(table, group_list, position):
    print("Touching a position {}...".format(position))
    group_position = getPositionGroup(group_list, position)
    for position in group_list[group_position].positions:
        table[position[0]][position[1]] = 0

def gravityEffect(table):
    for i in reversed(range(1, len(table))):
        for j in reversed(range(len(table))):
            if table[i][j] == 0:
                table[i][j] = table[i - 1][j]
                table[i - 1][j] = 0
    return table

def shiftToTheRight(table):
    for i in reversed(range(len(table))):
        for j in reversed(range(1, len(table))):
            if table[i][j] == 0:
                table[i][j] = table[i][j - 1]
                table[i][j - 1] = 0
    return table


#n = 4
#table = generateTable(n)
table = ([1, 1, 2], [1, 1, 2], [2, 2, 1])

printTable(table)
groupList = makeGroups(table)

"""nGroup = 1
for i in groupList:
    print("Grupo # {}".format(nGroup))
    i.__str__()
    nGroup += 1"""

touchPosition(table, groupList, [0, 2])

gravityEffect(table)
printTable(table)

shiftToTheRight(table)
printTable(table)