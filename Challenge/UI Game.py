#Author: Javier Ardila {javier.ardila@flexibility.com.ar}
#Author: Guillermo Forero {guillermoforerosuarez@gmail.com}

import time
import random
from builtins import print
import sys
import numpy
import math
from tkinter import *

def generateTable(n, n_colors):
    print("Initializing table...")
    table = numpy.zeros((n, n))
    for i in range(n):
        for j in range(n):
            table[i][j] = random.randint(1, n_colors)

    printTable(table)
    return table

def printTable(table):
    print("Printing table...")
    for i in range(len(table)):
        print("    ", end="")
        for j in range(len(table)):
            print(int(table[i][j]), end=" ")
        print()

def copyTable(table):
    table_copy = numpy.zeros((len(table), len(table)))
    for i in range(len(table)):
        for j in range(len(table)):
            table_copy[i][j] = table[i][j]

    return table_copy


class Movement:

    def __init__(self, previousPos, currentPos):
        self.previousPos = previousPos
        self.currentPos = currentPos

    def _str_(self):
        print("current: {}".format(self.currentPos), end=" ")

class ColorGroup:
    def __init__(self, colorNumber, positions):
        self.positions = positions
        self.colorNumber = colorNumber

    def __str__(self):
        print("color:", self.colorNumber, ", size: ", len(self.positions), "\npositions-> ", end="")
        for position in self.positions:
            print(position, end=" ")


def isInvalidMovement(movement, n):
    return movement[0] < 0 or  movement[1] < 0 or movement[0] > (n - 1) or movement[1] > (n - 1)

def existPositionInGroups(group_list, position):
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

                if not existPositionInGroups(group_list, pos):
                    group_by = table[i][j]
                    neighborScanAlgorithm(table, group_by, Movement(None, pos), visited_elements)
                    group_list.append(ColorGroup(group_by, visited_elements))

    return group_list

def neighborScanAlgorithm(table, group_by, move, movements_made):
    tmp_element = table[move.currentPos[0]][move.currentPos[1]]

    if move.currentPos not in movements_made and tmp_element == group_by:
        movements_made.append(move.currentPos)
        next_movements = getPossibleMovements(move, len(table))

        for next_movement in next_movements:
            neighborScanAlgorithm(table, group_by, next_movement, movements_made)


def getPositionGroup(group_list, position):
    for i in range(len(group_list)):
        if position in group_list[i].positions:
            return i

def touchPosition(table, position, debug):
    if debug: print("Touching a position {}...".format(position))

    group_list = makeGroups(table)
    group_position = getPositionGroup(group_list, position)
    group = group_list[group_position].positions

    amount_boxes = len(group)
    if amount_boxes > 1:
        for position in group:
            table[position[0]][position[1]] = 0

        if debug: printTable(table)
        gravityEffect(table)
        shiftToTheRight(table)
        if debug: printTable(table)

    return getTouchPuntuation(amount_boxes)


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
    for i in range(len(table)):
        for j in range(len(table)):
            if table[j][i] != 0:
                break
            elif i != 0 and (j == (len(table) - 1)):
                for k in range(len(table)):
                    for l in reversed(range(1, i + 1)):
                        table[k][l] = table[k][l - 1]
                        table[k][l - 1] = 0

    return table

def getTouchPuntuation(N):
    return N * (N - 1)


# Utilities play the game
def getValidGroups(group_list):
    valid_groups = []
    for group in group_list:
        if len(group.positions) > 1:
            valid_groups.append(group)

    return valid_groups

def gameWon(group_list):
    return len(group_list) == 0

def hasOnlySingletons(group_list):
    for g in group_list:
        if len(g.positions) > 1:
            return False
    return True

def getGameState(group_list, score, debug):
    if gameWon(group_list):
        if debug: print("Game WIN with: {} points".format(score))
        return 0
    elif hasOnlySingletons(group_list):
        if debug: print("Game finished by singletons state, with: {} points".format(score))
        return 1
    else:
        if debug: print("NOT have finished, current points: {}".format(score))

    return -1

def playGameUsingPlayList(table, playlist):
    score = 0
    for position in playlist:
        score += touchPosition(table, position, False)
    return table, score

def getAmountOfSingletons(group_list):
    singletons_amount = 0
    for group in group_list:
        if len(group.positions) == 1:
            singletons_amount += 1
    return singletons_amount



class App():
    def __init__(self, root):
        self.root = root
        self.TopFrame = Frame(root)
        self.BottomFrame = Frame(root)
        self.FrameFinish = Frame(root)
        self.TopFrame.grid(row=0)
        self.FrameFinish.grid(row=7)
        self.BottomFrame.grid(row=6)
        self.score = 0
        self.table = []
        self.play_list = []
        self.play_index = 0


    def Function(self, table):
        self.grid = []
        for i in range(len(table)):
            row = []
            for j in range(len(table)):
                if(table[i][j] == 0):
                    row.append(Button(self.TopFrame,width=6,height=3,command=lambda i=i, j=j: self.getClick(table ,i, j),background='grey'))
                    row[-1].grid(row=i,column=j)
                if(table[i][j] == 1):
                    row.append(Button(self.TopFrame,width=6,height=3,command=lambda i=i, j=j: self.getClick(table ,i, j),background='red'))
                    row[-1].grid(row=i,column=j)
                if(table[i][j] == 2):
                    row.append(Button(self.TopFrame,width=6,height=3,command=lambda i=i, j=j: self.getClick(table ,i, j),background='blue'))
                    row[-1].grid(row=i,column=j)
                if(table[i][j] == 3):
                    row.append(Button(self.TopFrame,width=6,height=3,command=lambda i=i, j=j: self.getClick(table ,i, j),background='green'))
                    row[-1].grid(row=i,column=j)
                if(table[i][j] == 4):
                    row.append(Button(self.TopFrame,width=6,height=3,command=lambda i=i, j=j: self.getClick(table ,i, j),background='purple'))
                    row[-1].grid(row=i,column=j)
                if(table[i][j] == 5):
                    row.append(Button(self.TopFrame,width=6,height=3,command=lambda i=i, j=j: self.getClick(table ,i, j),background='yellow'))
                    row[-1].grid(row=i,column=j)
            self.grid.append(row)

    def getClick(self,table, i, j):
        orig_color = self.grid[i][j].cget('bg')
        if orig_color!="grey":
            self.score +=touchPosition(table, [i,j], False)
        print(i, j)
        if(getGameState(makeGroups(table),self.score, True)!= -1):
            self.finish()
        self.Function(table)

    def showAllGame(self, table, play_list):
        self.Function(table)
        self.table = table
        self.play_list = play_list

    def nextPlay(self):
        self.score +=touchPosition(self.table, self.play_list[self.play_index], False)
        self.Function(table)
        self.play_index = self.play_index+1
        if(getGameState(makeGroups(table),self.score, True)!= -1):
            self.finish()

    def finish(self):
        self.grid = []
        self.TopFrame.grid_forget()
        self.BottomFrame.grid_forget()
        row = []
        row.append(Label(self.FrameFinish, text="El juego ha finalizado!"))
        row[-1].grid(row=0,column=0)
        row.append(Label(self.FrameFinish, text="El puntaje fue {}".format(self.score)))
        row[-1].grid(row=1,column=0)
        self.grid.append(row)

table = generateTable(10, 5)

root = Tk()
app = App(root)
printTable(table)
app.Function(table)
root.mainloop()
