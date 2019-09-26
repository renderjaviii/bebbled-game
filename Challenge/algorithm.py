#Author: Javier Ardila {javier.ardila@flexibility.com.ar}

import random
from builtins import print
import sys

import numpy
import math

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

        if debug: printTable(table)
        gravityEffect(table)
        if debug: printTable(table)
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


# Solving game
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

def printGameState(table, movements_list, score):
    if gameWon(makeGroups(table)):
        print("WIN!!!")
    elif hasOnlySingletons(makeGroups(table)):
        print("WIN with singletons :/")

    print("SCORE:", score)
    printTable(table)
    print("Play list |-", end="")

    for movement in movements_list:
        print("-> {} ".format(movement), end="")

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


# Greedy collection tools
def getLargerGroupIndexAndPosition(group_list):

    position = -1
    max = -1
    for group in group_list:
        max_tmp = len(group.positions)
        if max_tmp > max:
            position = group.positions[0]
            max = max_tmp

    return position

def solveGameWithGreedy(table, priority_best_score, debug):

    play_list = []

    if priority_best_score:
        best_score = 0
        while True:
            larger_group_position = getLargerGroupIndexAndPosition(makeGroups(table))

            if larger_group_position != -1:
                best_score += touchPosition(table, larger_group_position, debug=debug)
                play_list.append(larger_group_position)

                game_state = getGameState(makeGroups(table), best_score, debug=debug)
                if game_state == 0 or game_state == 1:
                    return play_list

    else:
        while True:
            group_list = makeGroups(table)

            minimum_singletons = sys.maxsize
            movement = -1

            for group in group_list:
                table_copy = copyTable(table)
                touchPosition(table_copy, group.positions[0], debug=True)

                singletons = getAmountOfSingletons(makeGroups(table_copy))
                if singletons < minimum_singletons:
                    minimum_singletons = singletons
                    movement = group.positions[0]

                game_state = getGameState(makeGroups(table_copy), minimum_singletons, debug=debug)
                if game_state == 0 or game_state == 1:
                    return play_list

            if movement != -1:
                touchPosition(table, movement, False)
                play_list.append(movement)


# Genetic algorithm
def createInitialPopulation(group_list):
    print("\nCreating initial population", end=" ")
    valid_groups = getValidGroups(group_list)
    population_amount = math.ceil(len(valid_groups) * 0.5)

    initial_population = []
    for i in range(population_amount):
        group_index = random.randint(0, len(valid_groups) - 1)
        group = valid_groups[group_index].positions;
        table_position = group[0]

        if len(valid_groups) > 1 and (table_position not in initial_population):
            initial_population.append(table_position)
            valid_groups.pop(group_index)

    if len(initial_population) == 0: # Repeat process if dont have individuals, infinite possible cycle
        createInitialPopulation(group_list)

    print("-> {}".format(initial_population))
    return initial_population

def generateNextState(table):
    valid_groups = getValidGroups(makeGroups(table))

    if len(valid_groups) > 0:
        group_index = random.randint(0, len(valid_groups) - 1)
        table_position = valid_groups[group_index].positions[0]
        touchPosition(table, table_position, False)
        return table_position

    return -1  # If there arent more options

def projectGame(table, initial_states, n_projections, n_attempts, debug):
    table_copy = copyTable(table)

    for state in initial_states:
        touchPosition(table_copy, state, debug)

    play_list = []
    for time in range(n_projections):
        if debug: print("Projection # {}".format(time + 1))

        table_tmp = copyTable(table_copy)
        movement_list = initial_states.copy()

        for attempt in range(n_attempts):
            if debug: print("Attempt -> {}".format(attempt + 1))
            table_position = generateNextState(table_tmp)

            if table_position != -1:
                movement_list.append(table_position)
            else: break

        if len(movement_list) > 0 and (movement_list not in play_list):
            play_list.append(movement_list)

    return play_list

def getFitnessAndHighLights(table, play_list, is_score_priority):
    highlights = []
    max_score = -1
    minimum_singletons = sys.maxsize

    for time in play_list:
        table_copy, score = playGameUsingPlayList(copyTable(table), time)

        if is_score_priority:
            if score >= max_score:
                max_score = score
                if len(time) < len(highlights) or len(highlights) == 0:  # The minimum moves ever ?
                    highlights = time
        else:
            singletons = getAmountOfSingletons(makeGroups(table_copy))

            if singletons <= minimum_singletons:
                minimum_singletons = singletons
                if len(time) < len(highlights) or len(highlights) == 0:  # The minimum moves ever ?
                    highlights = time

    fitness_value = max_score
    if max_score == -1:
        fitness_value = minimum_singletons

    return fitness_value, highlights

def solveGameWithGA(table, n_population, n_generations, n_projections, is_score_priority, debug):

    best_general_play_list = []
    best_fitness = -1
    for initial_individual in createInitialPopulation(makeGroups(table)):
        possibles_play_list = projectGame(table, [initial_individual], n_projections, n_generations, debug=debug)
        fitness_val = getFitnessAndHighLights(table, possibles_play_list, is_score_priority)[0]
        if fitness_val > best_fitness:
            best_fitness = fitness_val
            best_initial_individual = initial_individual

    if debug: print("The initial individual is: {}, with {} points".format(best_initial_individual, best_fitness))

    best_general_play_list.append(best_initial_individual)
    touchPosition(table, best_initial_individual, debug) # Set table current status

    while getGameState(makeGroups(table), 0, debug=debug) == -1:
        for i in range(n_population + 1):
            if debug: print("\nPopulation #{}\n".format(i + 1))
            populations_generations = []

            for j in range(n_generations):
                if debug: print("Descendant # {} of the previous generation\nScore inherited: {}\nPlay list inherited -> {}"
                                .format(j + 1, best_fitness, best_general_play_list))

                play_lists = projectGame(table, [], n_projections, n_generations, debug=debug) # Projections
                for play_list in play_lists:
                    if play_list not in populations_generations:
                        populations_generations.append(play_list)

            if len(populations_generations) > 0:
                best__play_list_population = getFitnessAndHighLights(copyTable(table), populations_generations, is_score_priority)[1]
                next_movement = best__play_list_population[0]
                best_general_play_list.append(next_movement)  # Add only the first movement

                best_fitness += touchPosition(table, next_movement, debug=debug)  # Set score and table current status
                if debug: print("\nBest so far -> {} with: {} points".format(best_general_play_list, best_fitness))


    printGameState(table, best_general_play_list, fitness_val)


# TESTING
table = ([2, 2, 1, 1], [2, 2, 1, 1], [1, 1, 1, 1], [2, 1, 2, 2])
printTable(table)
# table = generateTable(5, 5)

#solveGameWithGA(table, n_population=2, n_generations=5, n_projections=20, is_score_priority=False, debug=False)

solveGameWithGreedy(table, priority_best_score=False, debug=True)

# Peso = (cantidad de fichas un color) / (cantidad total de fichas)
# Tocar las fichas de menor peso en orden ascendente
# Tocar las fichas que estén imposibilitando la unión de 2 grupos que formarían un gran peso

# Elegir el color con mayor peso e intentar romper la mayor cantidad de las otras
# fichas, buscando que todas las fichas del color elegido queden juntas

def getSizeBoxesByColor(group_list):
    size_groups_by_color = {}

    for group in group_list:
        color_number = group.colorNumber
        if color_number in size_groups_by_color.keys():
            size_groups_by_color[color_number] = (size_groups_by_color[color_number] + len(group.positions))
        else: size_groups_by_color[color_number] = len(group.positions)

    return  size_groups_by_color