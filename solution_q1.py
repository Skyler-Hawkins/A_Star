# SKYLER HAWKINS SOLUTIONS FOR QUESTION 1 PROBLEMS


# Important note: specific heuristic for which direction to check next is not specified so I will
# Arbitraily choose to explore with the following priority: up, right, down, left
# Seen both recursive and iterative approaches to DFS, I do not like recursion so I will implement an iterative approach


# HELPER FUNCTIONS: 
# There are several helper functions that can be used in several different search algorithms, they will be implemented here

# is_valid_move: checks if a move is valid given the current state of the board
def is_valid_move(x,y):
    return (0<=x<3 and 0<=y<3)

# set_puzzle: converts the input string from input.txt into a 2D list of integers




def DFS(graph, start):
    visited = set()
    to_visit = [start]
    while to_visit is not None: 
        node = to_visit.pop()
        if node not in visited: 
            visited.add(node)
            for child_node in graph[node]:
                to_visit.append(child_node)


    return None