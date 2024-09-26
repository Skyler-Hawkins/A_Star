# SKYLER HAWKINS SOLUTIONS FOR QUESTION 2 PROBLEMS
import copy
import time
from collections import deque

'''
CMPSC 442 Project 1: Search 
Written By Skyler Hawkins

NOTES: 
I opted to use two libraries in this project, copy and deque.
Copy is used to deep copy the puzzle state so I can quickly get a copy of the puzzle for each move
    - I ran into this issue in the past on other projects, since python is pass by reference, I figured this is a viable solution
Deque is used to implement a queue for BFS, since it was an easy way to implement a queue in python
    - Since we are not being tested on our data structure implementation skills, but rather our search algorithms, I hope this is acceptable

*In github codespace, where I have been developing my project, my DFS crashes rather quickly, likely due to the memory limits
set on the codespace student account. I added a time check as per the Professor's suggestion.*    
'''


# global variables
puzzle_array = []

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

# gets every new possible board state from the current board state, and returns these states in list form

def get_possible_moves(puzzle_state):
    potential_moves = []
    # find the blank piece
    blank_x, blank_y = None, None

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
        potential_moves.append([new_puzzle, new_puzzle[blank_x][blank_y] + "U"])

    # check if can move a piece RIGHT into the blank
    # aka, if blank is not in rightmost column (if j < 2)
    if blank_y < 2:
        new_puzzle = copy.deepcopy(puzzle_state)

        new_puzzle[blank_x][blank_y] = new_puzzle[blank_x][blank_y+1]
        new_puzzle[blank_x][blank_y+1] = '_'
        potential_moves.append([new_puzzle, new_puzzle[blank_x][blank_y] + "R"])
    
    # check if can move a piece DOWN into the blank
    # aka, if blank is not in bottom row (if i < 2)
    if blank_x < 2:
        new_puzzle = copy.deepcopy(puzzle_state)

        new_puzzle[blank_x][blank_y] = new_puzzle[blank_x+1][blank_y]
        new_puzzle[blank_x+1][blank_y] = '_'
        potential_moves.append([new_puzzle, new_puzzle[blank_x][blank_y] + "D"])
    
    # check if can move a piece LEFT into the blank
    # aka, if blank is not in leftmost column (if j > 0)
    if blank_y > 0:
        new_puzzle = copy.deepcopy(puzzle_state)

        new_puzzle[blank_x][blank_y] = new_puzzle[blank_x][blank_y-1]
        new_puzzle[blank_x][blank_y-1] = '_'
        potential_moves.append([new_puzzle, new_puzzle[blank_x][blank_y] + "L"])
    # this is essentially biasing left, down, right, up for DFS since it is a stack, but U R D L for BFS since it is a FIFO queue
    return potential_moves
    

#my heuristic: 
'''
given a state, there will be a current sum of the top row
this can either be < 11, 11, or > 11
if < 11, we need to find what number would make it 11 (if possible)
we then calculate the manhattan distance of that number to the blank space in the top row (if possible)
if == 11, goal state reached, should never reach here
if > 11, we need to find what number would make it 11 by replacing one of the numbers in the top row
More complicated than previous heuristic function, but should be more efficient
I likely took some liberties that reduce the efficiency of the heuristic (perhaps overly optimistic), but it works
'''

def manhattan_distance_2(current_state):
    total_distance = 0
    # need to find the blank space first
    blank_x, blank_y = None, None
    for i in range(0,3):
        for j in range(0, 3):
            if current_state[i][j] == '_':
                blank_x, blank_y = i, j

    sum = 0
    for i in range(0, 3):
        if current_state[0][i] != '_':
            sum += int(current_state[0][i])
    # next, if blank space in top row here
    if blank_x == 0:
        # sum of top row

        if sum < 11: 
            # find index of number that would make it 11, then calc manhattan distance from there 
            target = 11 - sum
            for i in range(1, 3):
                for j in range(0, 3): 
                    if current_state[i][j] == str(target):
                        # distance from target to blank space, dont care about the other 
                        total_distance = abs(i-0) + abs(j-blank_y)
                        break
        elif sum > 11:
            # need to find the number that would make it 11
            # but, we need to replace one of the numbers in the top row with this number... since 
            # thus we need to find manhattan distance to the number we choose to replace. 
            target = sum - 11 
            # if blank space is left or right, replace middle #, otherwise replace right
            if blank_y == 0 or blank_y == 2:
                target -= int(current_state[0][1])
            else:
                target -= int(current_state[0][2])
            
            
            for i in range(1, 3):
                for j in range(0, 3):
                    if current_state[i][j] == str(target):
                        if blank_y == 0:
                            total_distance = abs(i-0) + abs(j-(blank_y + 1))
                        if blank_y == 1:
                            total_distance = abs(i-0) + abs(j-0)
                        if blank_y == 2:
                            total_distance = abs(i-0) + abs(j-(blank_y - 1))
                            break
    else:
        # arbitarily choosing to replace the middle number with the hypothetical new one (probably not optimal but it is my temp solution) 
        sum = sum - int(current_state[0][1])
        if sum < 11:
            target =  11 - sum
            for i in range(0, 3):
                for j in range(0, 3):
                    if current_state[i][j] == str(target):
                        total_distance = abs(i-0) + abs(j-1)
                        break
        elif sum > 11:
            target = sum - 11
            for i in range(0, 3):
                for j in range(0, 3):
                    if current_state[0][i] == str(target):
                        total_distance = abs(i-0) + abs(j-1)
                        break
    return total_distance

        
# new straight line distance heuristic
def straight_line_distance_2(current_state):
    total_distance = 0
    # need to find the blank space first
    blank_x, blank_y = None, None
    for i in range(0,3):
        for j in range(0, 3):
            if current_state[i][j] == '_':
                blank_x, blank_y = i, j
    
    sum = 0
    for i in range(0, 3):
        if current_state[0][i] != '_':
            sum += int(current_state[0][i])
    # next, if blank space in top row here
    if blank_x == 0:
        # sum of top row

        if sum < 11: 
            # find index of number that would make it 11, then calc manhattan distance from there 
            target = 11 - sum
            for i in range(1, 3):
                for j in range(0, 3): 
                    if current_state[i][j] == str(target):
                        # distance from target to blank space, dont care about the other 
                        total_distance = ((i - 0) ** 2 + (j - blank_y) ** 2) ** 0.5
                        break
        elif sum > 11:
            # need to find the number that would make it 11
            # but, we need to replace one of the numbers in the top row with this number... since 
            # thus we need to find manhattan distance to the number we choose to replace. 
            target = sum - 11
            # if blank space is left or right, replace middle #, otherwise replace right
            if blank_y == 0 or blank_y == 2:
                target -= int(current_state[0][1])
            else:
                target -= int(current_state[0][2])

            for i in range(1, 3):
                for j in range(0, 3):
                    if current_state[i][j] == str(target):
                        if blank_y == 0:
                            total_distance = (abs(i - 0) ** 2 + abs(j - (blank_y + 1)) ** 2) ** 0.5
                        if blank_y == 1:
                            # total_distance = abs(i-0) + abs(j-0)
                            total_distance = (abs(i - 0) ** 2 + abs(j - blank_y) ** 2) ** 0.5
                        if blank_y == 2:
                            total_distance = (abs(i - 0) ** 2 + abs(j - (blank_y - 1)) ** 2) ** 0.5
                            # total_distance = abs(i-0) + abs(j-(blank_y - 1))
                            break
    else:
        # arbitarily choosing to replace the middle number with the hypothetical new one (probably not optimal but it is my temp solution) 
        sum = sum - int(current_state[0][1])
        if sum < 11:
            target =  11 - sum
            for i in range(0, 3):
                for j in range(0, 3):
                    if current_state[i][j] == str(target):
                        total_distance = (abs(i - 0) ** 2 + abs(j - 1) ** 2) ** 0.5
                        # total_distance = abs(i-0) + abs(j-1)
                        break
        elif sum > 11:
            target = sum - 11
            if blank_y == 0 or blank_y == 2:
                target -= int(current_state[0][1])
            else:
                target -= int(current_state[0][2])
                
            for i in range(0, 3):
                for j in range(0, 3):
                    if current_state[0][i] == str(target):
                        total_distance = (abs(i - 0) ** 2 + abs(j - 1) ** 2) ** 0.5
                        # total_distance = abs(i-0) + abs(j-1)
                        break
    return total_distance



# checks if goal is met
# the numbers in the top row should sum to 11
def check_goal(puzzle_state):
    sum = 0
    for i in range(0, 3):
        current = puzzle_state[0][i]
        if current != '_':
            sum += int(current)
    if sum == 11:
        return True
    return False


# SEARCH ALGORITHMS BELOW

# specific heuristic for which direction to check next is not specified so 
# Arbitraily chose to explore with the following priority: left, down, right, up
# Seen both recursive and iterative approaches to DFS, I do not like recursion so I will implement an iterative approach


def DFS(initial_puzzle):
    start_time = time.time()

    visited = set() # 9/20: changed to set for increased efficiency of check
    print("beginning dfs")
    node_expansions = 0
    # LIFO stack as per lecture slides
    # initial_puzzle = [['1', '2', '3'], ['_', '4', '5'], ['6', '7', '8']] #example puzzle that this DFS can solve
    stack = []
    stack.append([initial_puzzle, []])
    print(stack)
    while stack: 
        stackout = stack.pop()
        current_state = stackout[0]
        path = stackout[1]
        # print(len(stack))
        if check_goal(current_state):
            # solution found
            return path
        # using tuple so I can check if the state has been visited in O(1) time
        current_tuple = tuple(map(tuple, current_state))
        if current_tuple not in visited:
            visited.add(current_tuple)
            node_expansions += 1
            for new_board_state, new_move in get_possible_moves(current_state):
                new_board_tuple = tuple(map(tuple, new_board_state))
                if new_board_tuple not in visited:
                    stack.append([new_board_state, path + [new_move]])
        if time.time() - start_time > 10:
            return ("Solution not found in reasonable amount of time")


    return False


# very similar to DFS in implementation, just using queue instead of stack
# BFS is a FIFO queue, meaning instead of popping from the end (like in DFS), we pop from the front 
# Found deque as a library, need to check with professor to see if this is allowed. If not, can try and implement a queue from scratch
def BFS(initial_puzzle):
    visited = set()
    iterations = 0
    node_expansions = 0
    # need queue
    # FOUND DEQUE from pythons collections library, should be perfect for this
    # needed to wrap in double [] to make it work, so its [[initial_puzzle, []]]
    queue = deque([[initial_puzzle, []]])

    while queue:
        queuout = queue.popleft()
        current_state = queuout[0]
        path = queuout[1]
        if check_goal(current_state):
            return path

        current_tuple = tuple(map(tuple, current_state))
        if current_tuple not in visited:
            visited.add(current_tuple)
            node_expansions += 1
            for new_board_state, new_move in get_possible_moves(current_state):
                queue.append([new_board_state, path + [new_move]])
    return False



# UCS: Uniform Cost Search
# when all edge weights are equal, UCS is the same as BFS
# so I will implement UCS as BFS
def UCS(initial_puzzle): 
    return BFS(initial_puzzle)


# A* Search
# Heuristic funnction: h(n) = the manhattan distance from the current state to the goal state
# could use # of misplaced tiles, opting to use manhattan distance for a more efficient search
# also setting heuristic function dynamically, will default to manhattan distance if none is given
def A_star(initial_puzzle, heuristic=manhattan_distance_2):
    visited = set()
    # visited = set()
    # need list (fringe)
    open = [(heuristic(initial_puzzle), 0, initial_puzzle, [])]  # (f_cost, g_cost, current_state, path)
    node_expansions = 0
    
    while open:
        # just needed a giant number to initialize the minimum f cost, since I'm looping through each element in open, check if this works
        min_f_cost = 1000000
        min_i = -1
        # print("finding a path")
        for i in range(0, len(open)):
            if open[i][0] < min_f_cost:
                # locating lowest f_cost state to go from
                min_f_cost = open[i][0]
                min_i = i
        _, g_cost, current_state, path = open.pop(min_i)

        if check_goal(current_state):
            return path
        
        current_tuple = tuple(map(tuple, current_state))
        if current_tuple not in visited:
            visited.add(current_tuple)
            node_expansions += 1
            for new_board_state, new_move in get_possible_moves(current_state):
                new_g_cost = g_cost + 1
                h_cost = heuristic(new_board_state)
                f_cost = new_g_cost + h_cost

                # checking if new board state is already in the open_list
                # if it is, we need to update the f_cost and g_cost of that state
                if new_board_state in [state[2] for state in open]:
                    for i in range(0, len(open)):
                        if open[i][2] == new_board_state:
                            if f_cost < open[i][0]:
                                open[i] = (f_cost, new_g_cost, new_board_state, path + [new_move])
                else:
                    open.append((f_cost, new_g_cost, new_board_state, path + [new_move]))

    
    return False

# DRIVER CODE OF THE FILE



try:
    dfs_puzzle_array = set_puzzle(open("input.txt", "r"))
    result = DFS(dfs_puzzle_array)
    result_str = ','.join(result)
    print("\nThe solution of Q2.1(DFS) is:\n", result_str)
except Exception as e:
    print("Failed with error: ", e)


bfs_puzzle_array = set_puzzle(open("input.txt", "r"))
result = BFS(bfs_puzzle_array)
result_str = ','.join(result)
print("\nThe solution of Q2.2(BFS) is:\n", result_str)

ucs_puzzle_array = set_puzzle(open("input.txt", "r"))
result = UCS(ucs_puzzle_array)
result_str = ','.join(result)
print("\nThe solution of Q2.3(UCS) is:\n", result_str)

a_star_puzzle_array = set_puzzle(open("input.txt", "r"))
result = A_star(a_star_puzzle_array, manhattan_distance_2)
result_str = ','.join(result)
print("\nThe solution of Q2.4(A*) is:\n", result_str)


a_star_puzzle_array = set_puzzle(open("input.txt", "r"))
result = A_star(a_star_puzzle_array, straight_line_distance_2)
result_str = ','.join(result)
print("\nThe solution of Q2.5(A*) is:\n", result_str)
