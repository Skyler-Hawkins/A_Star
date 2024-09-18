# SKYLER HAWKINS SOLUTIONS FOR QUESTION 1 PROBLEMS
import copy

# global variables
puzzle_array = []
goal_state = [['_', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]

# HELPER FUNCTIONS: 
# There are several helper functions that can be used in several different search algorithms, they will be implemented here


# set_puzzle: converts the input string from input.txt into a 2D list of integers
def set_puzzle(input_file):
    # input file formatted like: "1,2,3,4,_,5,8,7,6"
    puzzle_str = input_file.read().split(',')
    _puzzle_array = []
    temp_arr = []
    i = 1
    # converting 1D array to 2D array for ease of comprehension and making moves more intuitive
    for element in puzzle_str :
        if i % 3 == 0:
            temp_arr.append(element)
            _puzzle_array.append(temp_arr)
            temp_arr = []
            i+=1
        else:
            temp_arr.append(element)
            i+=1

    return _puzzle_array



def get_possible_moves(puzzle_state):
    potential_moves = []
    # find the blank piece
    blank_x, blank_y = None, None
    # print("puzzle_state: ", puzzle_state)
    for i in range(0,3):
        for j in range(0, 3):
            if puzzle_state[i][j] == '_':
                blank_x, blank_y = i, j
    
    # check if can move a piece UP into the blank
    # aka, if blank is not in top row (if i > 0)
    
    if blank_x > 0: 
        # make new board state here
        new_puzzle = copy.deepcopy(puzzle_state)

        new_puzzle[blank_x][blank_y] = new_puzzle[blank_x-1][blank_y]
        new_puzzle[blank_x-1][blank_y] = '_'
        # print('new puzzle: ', new_puzzle)
        potential_moves.append(new_puzzle)
        # print("CHECKING OLD PUZZLE: ", puzzle_state)    
    # check if can move a piece RIGHT into the blank
    # aka, if blank is not in rightmost column (if j < 2)
    if blank_y < 2:
        new_puzzle = copy.deepcopy(puzzle_state)

        new_puzzle[blank_x][blank_y] = new_puzzle[blank_x][blank_y+1]
        new_puzzle[blank_x][blank_y+1] = '_'
        potential_moves.append(new_puzzle)
    
    # check if can move a piece DOWN into the blank
    # aka, if blank is not in bottom row (if i < 2)
    if blank_x < 2:
        new_puzzle = copy.deepcopy(puzzle_state)

        new_puzzle[blank_x][blank_y] = new_puzzle[blank_x+1][blank_y]
        new_puzzle[blank_x+1][blank_y] = '_'
        potential_moves.append(new_puzzle)
    
    # check if can move a piece LEFT into the blank
    # aka, if blank is not in leftmost column (if j > 0)
    if blank_y > 0:
        new_puzzle = copy.deepcopy(puzzle_state)

        new_puzzle[blank_x][blank_y] = new_puzzle[blank_x][blank_y-1]
        new_puzzle[blank_x][blank_y-1] = '_'
        potential_moves.append(new_puzzle)
    return potential_moves
    
# specific heuristic for which direction to check next is not specified so 
# Arbitraily chose to explore with the following priority: left, down, right, up
# Seen both recursive and iterative approaches to DFS, I do not like recursion so I will implement an iterative approach

'''
heres the intuition:
1st: check if you can move a piece UP into the blank, if so, do it.
2nd: check if you can move a piece RIGHT into the blank, if so, do it.
3rd: check if you can move a piece DOWN into the blank, if so, do it.
4th: check if you can move a piece LEFT into the blank, if so, do it.
if made it through all 4 directions and no moves were made, this is a dead end, backtrack
repeat the process until a solution state is found
'''

def DFS(initial_puzzle):
    # may change to be a set, since I've heard its much more efficient, is list for now
    visited = []
    num_iterations = 0
    # LIFO stack as per lecture slides
    # print("initial_puzzle: ", initial_puzzle)
    # simple initial puzzle
    stack = []
    stack.append(initial_puzzle)
    while stack: 
        # print("stack: ", stack)

        current_state = stack.pop()
        print("current state: ", current_state)
        if current_state == goal_state:
            # solutoin found, work out details later
            return num_iterations
        num_iterations += 1
        if current_state not in visited:
            visited.append(current_state)
            for new_board_state in get_possible_moves(current_state):
                print("new_board_state: ", new_board_state)
                stack.append(new_board_state)
    return False


puzzle_array = set_puzzle(open("input.txt", "r"))
print("puzzle_array: ", puzzle_array)
result = DFS(puzzle_array)
print("Number of iterations: ", result)
