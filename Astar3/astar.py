# g_cost is the cost from starting node
# h_cost is the cost from the target node
# f_cost = g_cost + h_cost
from priority_queue import *
import math
import sys
from board import *
from node import *
from debugger import *
import time

# TODO: remove this
debugger = Debugger()

# actions
move_ = "MOVE from {} to {}."
jump_ = "JUMP from {} to {}."
exit_ = "EXIT from {}."

class combination:
    coords = {}
    def __init__(self, coords):
        self.coords = set(coords) 
    def __str__(self):
        return str(sorted(self.coords))
    def __hash__(self):
        return hash( tuple(sorted(self.coords)))
    def __eq__(self, other):
        return self.coords == other.coords

def jump(current, adjacent):
    return (2*adjacent[0] - current[0], 
        2*adjacent[1] - current[1] )  


def findPath(data):

    board = Board(data)

    open_nodes = set()
    closed_nodes = set()
    f_cost_queue = BinQueue()

    #converting to hashable
    start_loc = [tuple(l) for l in data["pieces"]]
    start_loc = combination(start_loc)

    #adding to the board
    board.addNode(start_loc)

    f_cost_queue.put(start_loc, 0)

    # TODO: remove this before submission
    debugger.set_colour(data["colour"][0])
    debugger.set_block_locns(data["blocks"])
    debugger.set_piece_locations(start_loc.coords)
    debugger.print_board(start_loc.coords)

    #board.combination_data[start_loc].f_cost = 0;
    board.combination_data[start_loc].g_cost = 0
    open_nodes.add(start_loc)

    while open_nodes:
        
        currentNode = f_cost_queue.get()
   
        open_nodes.discard(currentNode)
        closed_nodes.add(currentNode)

        if not currentNode.coords:
            # current node is empty hence at exit
            print_path(start_loc, currentNode, board) 
            break
        else:  
            for child in getChildren(currentNode, board):
                #adds the comb to the board if not already initiated
                board.addNode(child)
                if child not in closed_nodes:
                    open_nodes.add(child)
                        # if new path to neighbour is shorter or neighbour is not in open
                    traversal_cost = 1 + board.combination_data[currentNode].g_cost
                    
                    if (traversal_cost < board.combination_data[child].g_cost):
                        board.combination_data[child].g_cost = traversal_cost
                        f_cost_queue.put(child, traversal_cost + board.combination_data[child].h_cost)
                        board.combination_data[child].parent = currentNode

        # print(len(open_nodes))
        # print(sorted([c.coords for c in open_nodes]))
        # break
    
def getChildren(pieceSet, board):
    childrenCombinations = []
    for piece in pieceSet.coords:
        
        
        explorableCoords = []
        for loc in adjacentnodes(piece):
            if board.withinBoard(loc):
                if (loc in board.blockSet) or (loc in pieceSet.coords):
                    landingLoc= jump(piece, loc)
                    if board.withinBoard(landingLoc) and landingLoc not in board.blockSet and landingLoc not in pieceSet.coords:
                        explorableCoords.append(landingLoc)                    
                else:
                    explorableCoords.append(loc)
            elif( piece in board.exit_locations):
                #appends an empty tuple if the piece exits
                explorableCoords.append(tuple())


        for coord in explorableCoords:
            tempCombination = pieceSet.coords.copy()
            tempCombination.remove(piece)
            #adds the coordinate of the pieces location if it hasn't exited
            if coord:
                tempCombination.add(coord)

            childrenCombinations.append(combination(tempCombination))
    return childrenCombinations

            
#returns list of adjacent nodes
def adjacentnodes(loc):
    neighbours = []
    r_start = loc[1]
    r_end = loc[1]+ 2
    col = 0
    for q in range(loc[0]-1, loc[0]+2):
        for r in range(r_start, r_end):
            neighbours.append((q,r))
        col += 1
        
        if col == 1:
            r_start -= 1
        
        if col == 2:
            r_end -= 1
 
    return neighbours
   

# def print_path(starting_node, target_node, board):
#     '''prints the traversal path'''

#     # base condition
#     if board.combination_data[target_node].parent != starting_node:
#         print_path(starting_node, board.combination_data[target_node].parent, board)

#     move_start = board.combination_data[target_node].parent.coords - target_node.coords
#     move_end =  target_node.coords - board.combination_data[target_node].parent.coords

#     # some nasty ass code, need to fix the popping
#     if move_end:
#         move_start= move_start.pop()
#         move_end = move_end.pop()

#         if move_end in adjacentnodes(move_start):
#             move = move_.format(move_start, move_end)
#             debugger.update(move_start, move_end)
#         else :
#             move = jump_.format(move_start, move_end)
#             debugger.update(move_start, move_end)
#     else:
#         m = move_start.pop()
#         move= exit_.format(m)
#         debugger.piece_locns.remove(m)

#     debugger.print_board(message=move)
#     time.sleep(0.75) # sleep used to show the pieces moving in a cinematic fashion
#     # print(move)


def print_path(starting_node, target_node, board):
    '''prints the traversal path'''

    # recursive case
    if board.combination_data[target_node].parent != starting_node:
        print_path(starting_node, board.combination_data[target_node].parent, board)
    
    print(target_node.coords)




