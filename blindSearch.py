from arrangeBoard import arrange_board
from queue import Queue
import copy
import time

class Problem(object):

    def __init__(self, initial):
        self.initial = initial

    # values = return values that can be used
    # used = return list of values that already bee used
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Returning row and column from empty spots on board -> spot =  0
    def select_space(self, board, state):
        for row in range(board):
            for column in range(board):
                if state[row][column] == 0:
                    return row, column

    def movements(self, state):
        num_range = range(1, 10) # Range of valid numbers that can be filled on board [integers from 1 to 9]
        values_in_column = [] # Values in column
        values_in_mini_grid = [] # Values in mini grid [3x3]

        row,column = self.select_space(9, state) # Getting #1 empty place on board

        # Getting row and filter valid number that can be placed there
        values_in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(num_range, values_in_row)

        # Getting column and filter valid number that can be placed there
        for column_index in range(9):
            if state[column_index][column] != 0:
                values_in_column.append(state[column_index][column])
        options = self.filter_values(options, values_in_column)

        # Getting mini gri [3x3] and filter valid number that can be placed there
        row_start = int(row/3)*3
        column_start = int(column/3)*3
        
        for mini_grid_row in range(0, 3):
            for mini_grid_column in range(0,3):
                values_in_mini_grid.append(state[row_start + mini_grid_row][column_start + mini_grid_column])
        options = self.filter_values(options, values_in_mini_grid)

        ##return all possibilities of numbers that can be placed in one spot
        for number in options:
            yield number, row, column

    # Returns updated board after adding new valid value
    def result(self, state, movement):

        value = movement[0] #value to be placed
        row = movement[1] #row to be placed
        column = movement[2] #column to be placed

        # Add new valid number to board and doing a recursively copy of the state. Creating a tree of states
        new_state = copy.deepcopy(state)
        new_state[row][column] = value

        return new_state

    # Checking the rules of Sudoku Using sums of each row, column and mini grid to determine if board state is valid
    def check_rules(self, state):

        # Expected 45 as sum of each row, column and mini quadrant.
        total = 45

        # Checking the rows and columns
        # if if total is invalid then return false
        for row in range(9):
            if (len(state[row]) != 9) or (sum(state[row]) != total):
                return False

            column_total = 0
            for column in range(9):
                column_total += state[column][row]

            if (column_total != total):
                return False

        # Checking mini grids
        for column in range(0,9,3):
            for row in range(0,9,3):

                mini_grid_total = 0
                for grid_row in range(0,3):
                    for grid_column in range(0,3):
                        mini_grid_total += state[row + grid_row][column + grid_column]

                if (mini_grid_total != total):
                    return False

        return True

class Node:

    def __init__(self, state, movement=None):
        self.state = state
        self.movement = movement

    # Using each movement to create a new board state
    def expand(self, problem):
        return [self.new_node(problem, movement)
                for movement in problem.movements(self.state)]

    # Returning object node with new state
    def new_node(self, problem, movement):
        next = problem.result(self.state, movement)
        return Node(next, movement)

def BreadthFirst(problem): # using the Search BreadthFirst to serch in all states
    # Define an initial node for the tree
    node = Node(problem.initial)

    ## Creating a queue to investigate the nodes (Firt in Firt out - FIFO)
    tree = Queue()
    tree.put(node)
    cont_state = 0

    ## Here is where the magic happens
    ## Explore all nodes of the queues and check if the state match with the rules of the game, when match, retun the child
    while (tree.qsize() != 0):
        cont_state = cont_state + 1
        node = tree.get()
        for child in node.expand(problem):
            if problem.check_rules(child.state):
                return child

            tree.put(child)
        print("Number of states = ", cont_state)
    return None

def blind_search_solve(board):
    print ("\nSolving with Blind Search:")

    start_time = time.time()

    problem = Problem(board)
    solution = BreadthFirst(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print("\n*** Solution Board ***")
        arrange_board(solution.state)
    else:
        print ("No solution")

    print ("\nTime to solve time: " + str(elapsed_time) + " seconds")
