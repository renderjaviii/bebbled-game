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

        group_list.pop(group_position) # Deleting group touched
        gravityEffect(table)
        shiftToTheRight(table)

    # Return the touch score
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
    aux = len(table) - 1
    for i in range(1, len(table)):
        for j in range(len(table)):
            if table[j][aux] != 0:
                break
            elif j == (len(table) - 1):
                for k in range(len(table)):
                    table[k][aux] = table[k][aux - 1]
                    table[k][aux - 1] = 0
        aux -= 1
    return table

def getTouchPuntuation(N):
    return N * (N - 1)


# Genetic algorithm
def generateNextState(current_table, current_playlist):
    current_group_list = makeGroups(current_table)
    index_group = random.randint(0, len(current_group_list) - 1)
    position_to_touch = current_group_list[index_group].positions[0]
    current_score = touchPosition(current_table, position_to_touch, True)

    current_playlist.append(position_to_touch)

    return current_table, makeGroups(current_table), current_score

def getLargerGroupIndex(group_list):
    max = -1
    for i in range(len(group_list)):
        max_tmp = len(group_list[i].positions)
        if max_tmp > max:
            index = i
            max = max_tmp

    return index, max

def getSizeBoxesByColor(group_list):
    size_groups_by_color = {}

    for group in group_list:
        color_number = group.colorNumber
        if color_number in size_groups_by_color.keys():
            size_groups_by_color[color_number] = (size_groups_by_color[color_number] + len(group.positions))
        else: size_groups_by_color[color_number] = len(group.positions)

    return  size_groups_by_color

def hasOnlySingletons(group_list):
    for g in group_list:
        if len(g.positions) > 1:
            return False
    return True

def gameWon(group_list):
    return len(group_list) == 0

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


def solveGame(table,  n_attempts, n_tables, n_projections):

    best_score = -1
    best_general_playlist = []
    for i in range(n_attempts):
        print("\nAttempt #{}".format(i + 1))
        print("---------------------------")
        score_and_playlist_attempt = {}

        for j in range(n_tables):
            if len(best_general_playlist) > 0:
                print("\nDescendant of the best previous generation")
                table_attempt, score_attempt = projectGameUsingPlaylist(copyTable(table), best_general_playlist)
                playlist_attempt = best_general_playlist

                print("Score inherited: {}\nPlaylist inherited -> {}".format(score_attempt, playlist_attempt))

                game_state = getGameState(group_list_attempt, score_attempt, False)
                if game_state == 0 or game_state == 1:
                    break
            else:
                print("\nPossible initial population")
                score_attempt = 0
                playlist_attempt = []
                table_attempt = copyTable(table)

            for k in range(n_projections):
                table_attempt, group_list_attempt, score = generateNextState(table_attempt, playlist_attempt)
                score_attempt += score

                game_state = getGameState(group_list_attempt, score_attempt, True)
                if game_state == 0 or game_state == 1:
                    break

            score_and_playlist_attempt[score_attempt] = playlist_attempt

        max_score_attempt = max(score_and_playlist_attempt.keys())
        if max_score_attempt > best_score:
            best_score = max_score_attempt
            best_general_playlist = score_and_playlist_attempt[max_score_attempt]

    print("BEST SCORE FOUND", best_score)
    print(best_general_playlist)


def projectGameUsingPlaylist(table, playlist):
    score = 0
    for position in playlist:
        score += touchPosition(table, position, False)

    return table, score


def printState(table, group_list, score):
    print("SCORE:", score)
    printTable(table)
    for g in group_list:
        print(g.colorNumber, "->", g.positions)


#table = ([2, 2, 1, 1], [1, 2, 1, 2], [1, 2, 1, 2], [2, 2, 1, 2])
table = generateTable(10)
printTable(table)

solveGame(table, n_attempts=2, n_tables=5, n_projections=1)

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

#Peso = (cantidad de fichas un color) / (cantidad total de fichas)

# Tocar las fichas de menor peso en orden ascendente
# Tocar las fichas que estén imposibilitando la unión de 2 grupos que formarían un gran peso
# Elegir el color con mayor peso e intentar romper la mayor cantidad de las otras
# fichas, buscando que todas las fichas del color elegido queden juntas







