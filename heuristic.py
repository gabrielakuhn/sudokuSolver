from arrangeBoard import arrange_board
from queue import Queue
import copy
import time

class Problem(object):

    def __init__(self, initial):
        self.initial = initial

    def check_rules(self, state):
        # total = 45 => max sum of row, column and mini grid [3x3]
        total = 45

        # Checking if sum of row and column = 45
        for row in range(9):
            if (len(state[row]) != 9) or (sum(state[row]) != total):
                return False
            column_sum = 0
            for column in range(9):
                column_sum += state[column][row]
            if (column_sum != total):
                return False

        # Checking if sum of mini grid = 45
        for column in range(0,9,3):
            for row in range(0,9,3):
                mini_grid_sum = 0
                for mini_grid_row in range(0,3):
                    for mini_grid_column in range(0,3):
                        mini_grid_sum += state[row + mini_grid_row][column + mini_grid_column]

                if (mini_grid_sum != total):
                    return False
        return True

    # values = return values that can be used in line and collumn
    # used = return list of values that already bee used in row and column
    def filter_values(self, values, used):
        return [number for number in values if number not in used]

    # Retorna um local vazio na grade com a maioria das restrições (menor quantidade de opções)
    def select_space(self, state):
        board_size = 9
        smaller_num_option = 9
        row = 0
        while row < board_size:
            column = 0
            while column < board_size:
                if state[row][column] == 0: ## just return a option if the number in the spot (row x column) is blanck (num = 0)
                    # Na primeira opção ele checa aapenas as opções pra linha, ai depois ele checa dentro dessa opções da linha, quais são as opções que também servem pra coluna
                    ##ai ele pega essa opções que também servem juntamente pra linha e pra coluna e ve quais que servem pro mini grid
                    ##e ai ele tem um vetor final de opções
                    options = self.filter_row(state, row) ## checking options to be placed in the row
                    options = self.filter_col(options, state, column) ## checking inside of options wich number can be placed also in the column
                    options = self.filter_mini_grid(options, state, row, column) ## checking options to be placed in the row, in the column and in the mini grid [3x3]
                    if len(options) < smaller_num_option: #verifica se o número de opções desta linha e coluna é menor do que o menor anterior, se é significa que este local é o que tem menos opções de números pra ser preenchido
                        smaller_num_option = len(options)
                        target_row = row
                        target_col = column
                column = column + 1
            row = row + 1
        return target_row, target_col

    # Getting row and filter valid options that can be placed there
    def filter_row(self, state, row):
        num_range = range(1, 10) # Range of valid numbers that can be filled on board [integers from 1 to 9]
        values_in_row = [number for number in state[row] if (number != 0)]
        options = self.filter_values(num_range, values_in_row)
        return options

    # Getting column and filter valid options that can be placed there, considering row options
    def filter_col(self, options, state, column):
        values_in_column = []
        for column_index in range(9):
            if state[column_index][column] != 0:
                values_in_column.append(state[column_index][column])
        options = self.filter_values(options, values_in_column)
        return options

    # Getting mini gris [3x3] and filter valid number that can be placed there, considering row and column  options
    def filter_mini_grid(self, options, state, row, column):
        values_in_mini_grid = [] # List of valid values in spot's quadrant
        row_start = int(row/3)*3
        column_start = int(column/3)*3
        
        for mini_grid_row in range(0, 3):
            for mini_grid_column in range(0,3):
                values_in_mini_grid.append(state[row_start + mini_grid_row][column_start + mini_grid_column])
        options = self.filter_values(options, values_in_mini_grid)
        return options    

    def movements(self, state):
        row, column = self.select_space(state) # Getting the most contraint place in the board for such state
        #print ("Atention !!!!!!!!!!!!!!!!!!!!!!!! most contraint PLACE IN THE BOARD !!!!!!!", row, column)

        # Getting the value to put in the most contraint place, filter by row, column and minigrid
        options = self.filter_row(state, row)
        options = self.filter_col(options, state, column)
        options = self.filter_mini_grid(options, state, row, column)

        # Returning one state for each valid option defined above
        # A vantagem aqui é que na maioria das vezes vai retornar um estado só, nos na BlindSerach retorna varios estados porque não considera as opções
        for number in options:
            new_state = copy.deepcopy(state) # Doing a clone of the original state
            new_state[row][column] = number
            yield new_state

class Node:
    
    def __init__(self, state):
        self.state = state

    def expand(self, problem):
        # Return list of valid states
        return [Node(state) for state in problem.movements(self.state)]

def BreadthFirst(problem): # using the Search BreadthFirst to serch in all states
    # Define an initial node for the tree
    node = Node(problem.initial)

    ## Creatinag a queue to investigate the noded (Firt in Firt out - FIFO)
    tree = Queue()
    tree.put(node)
    cont_state = 0

    ## Here is whn the magic happens
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

def heurisctic_solve(board):
    print ("\nSolving with Heuristic:")

    start_time = time.time()
    problem = Problem(board)
    solution = BreadthFirst(problem)
    elapsed_time = time.time() - start_time

    if solution:
        print("\n*** Solution Board ***")
        arrange_board(solution.state)
    else:
        print ("No solution")

    print ("\nTime to solve: " + str(elapsed_time) + " seconds")
