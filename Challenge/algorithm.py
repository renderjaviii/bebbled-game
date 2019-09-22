#Author: Javier Ardila {javier.ardila@flexibility.com.ar}

import random
import numpy

def generateTable(n):
    print("Initializing table...")
    table = numpy.zeros((n, n))
    for i in range(n):
        for j in range(n):
            table[i][j] = random.randint(1, 2)
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
            if table[i][j] != 0:

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

    gravityEffect(table)
    shiftToTheRight(table)

def gravityEffect(table):
    for i in reversed(range(len(table))):
        for j in reversed(range(len(table))):

            current_value = table[i][j]
            if current_value != 0:
                jumps = 1

                if (i + jumps) < (len(table)):
                    while table[i + jumps][j] == 0:
                        table[i + jumps][j] = current_value
                        table[i + jumps - 1][j] = 0
                        jumps += 1

                        if (i + jumps) > (len(table) - 1):
                            break

    return table

def shiftToTheRight(table):
    for i in reversed(range(len(table))):
        for j in reversed(range(len(table))):

            current_value = table[i][j]
            if current_value != 0:
                jumps = 1

                if (j + jumps) < (len(table)):
                    while table[i][j + jumps] == 0:
                        table[i][j + jumps] = current_value
                        table[i][j + jumps - 1] = 0
                        jumps += 1

                        if (j + jumps) > (len(table) - 1):
                            break

    return table


def getTouchPuntuation(N):
    return N * (N - 1)

def getIndexMaximumGroup(group_list):
    max = -1
    for i in range(len(group_list)):
        max_tmp = len(group_list[i].positions)
        if max_tmp > max:
            index = i
            max = max_tmp

    return index, max

#table = ([1, 2, 1, 1], [1, 2, 1, 2], [1, 2, 1, 2], [2, 2, 2, 2])
n = 4
table = generateTable(n)
printTable(table)

"""Greedy
groupList = makeGroups(table)
score = 0
while len(groupList) > 0:
    index_group, amount_boxes = getIndexMaximumGroup(groupList)
    touchPosition(table, groupList, groupList[index_group].positions[0])
    groupList = makeGroups(table)
    printTable(table)
    score += getTouchPuntuation(amount_boxes)

print("Score-> {}".format(score))"""

groupList = makeGroups(table)
nGroup = 1
for i in groupList:
    print("Grupo # {}".format(nGroup))
    i.__str__()
    nGroup += 1