from arrangeBoard import arrange_board
from blindSearch import blind_search_solve
from heuristic import heurisctic_solve

##board input
print("\n*** Sudoku 9x9 Input ***")
print("\n ==> Level 3 <==")
board = [[0,3,9,0,0,0,1,2,0],
        [0,0,0,9,0,7,0,0,0],
        [8,0,0,4,0,1,0,0,6],
        [0,4,2,0,0,0,7,9,0],
        [0,0,0,0,0,0,0,0,0],
        [0,9,1,0,0,0,5,4,0],
        [5,0,0,1,0,9,0,0,3],
        [0,0,0,8,0,5,0,0,0],
        [0,1,4,0,0,0,8,7,0]]

for row in board:
    print(row)

print("\n*** Problem Board ***")
arrange_board(board)
print("______________________")

blind_search_solve(board)
heurisctic_solve(board)