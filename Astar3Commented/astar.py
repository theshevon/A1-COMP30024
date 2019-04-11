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
	#for each combination holds the current distance and heuristic value
    board = Board(data)
    #combinations that are known but not yet explored
    open_nodes = set()
    #combination  that have been explored (min distance found)
    closed_nodes = set()
    #priority queue holding f-costs and there associated combinations  
    #may include multiple entries for the same combination if multiple paths are considered
    f_cost_queue = BinQueue()

    #converting starting locations correct format for combination
    start_loc = [tuple(l) for l in data["pieces"]]
    start_loc = combination(start_loc)

    # TODO: reove this before submission
    #debugger.set_colour(data["colour"][0])
    #debugger.set_block_locns(data["blocks"])
    #debugger.set_piece_locations(start_loc.coords)
    #debugger.print_board(start_loc.coords)

    #adds starting location to the board
    board.addNode(start_loc)
    #initialises g_cost and f_cost to 0 and adds starting location to the open set
    f_cost_queue.put(start_loc, 0)
    board.getNode(start_loc).g_cost = 0
    open_nodes.add(start_loc)

    while open_nodes:
        #the currentNode is the node with the lowest f_cost
        currentNode = f_cost_queue.get()
        #Moves the current node to the closed set 
        open_nodes.discard(currentNode)
        closed_nodes.add(currentNode)

        if not currentNode.coords:
            # current node is empty hence at exit
            print_path(start_loc, currentNode, board) 
            break

        for child in getChildren(currentNode, board):
            #creates a new node for child if not already initiated
            board.addNode(child)
            if child not in closed_nodes:
                #added to open set
                open_nodes.add(child)
                #cost to move to a connected node  
                traversal_cost = 1 + board.getNode(currentNode).g_cost
                #if current path is better updates the childs parent and g_cost,
                if board.updateNode(child, traversal_cost, currentNode):
                	#adds updated f_cost of child to the priority heap
                    f_cost_queue.put(child, traversal_cost + board.getNode(child).h_cost)


#returns the possible combinations that could be reached from the one provided
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
   
#Prints the path from the start state to the target state
def print_path(starting_node, target_node, board):
    '''prints the traversal path'''

    # base condition
    if board.combination_data[target_node].parent != starting_node:
        print_path(starting_node, board.combination_data[target_node].parent, board)

    move_start = board.combination_data[target_node].parent.coords - target_node.coords
    move_end =  target_node.coords - board.combination_data[target_node].parent.coords

    if move_end:
        move_start= move_start.pop()
        move_end = move_end.pop()

        if move_end in adjacentnodes(move_start):
            move = move_.format(move_start, move_end)
            #debugger.update(move_start, move_end)
        else :
            move = jump_.format(move_start, move_end)
            #debugger.update(move_start, move_end)
    else:
        move_start = move_start.pop()
        move= exit_.format(move_start)
        #debugger.piece_locns.remove(move_start)

    #debugger.print_board(message=move)
    #time.sleep(0.75) # sleep used to show the pieces moving in a cinematic fashion
    print(move)




