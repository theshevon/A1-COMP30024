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



class combination:
    coords = {}
    def __init__(self, coords):
        self.coords = set(coords) 
    def __str__(self):
        return str(sorted(self.coords))
    def __hash__(self):
        return hash( tuple(sorted(self.coords)))
    def __eq__(self, other):
        # THIS IS WRONG CUZ DICTIONARY ORDERING CHANGES
        return self.coords == other.coords

def jump(current, adjacent):
    return (2*adjacent[0] - current[0], 
        2*adjacent[1] - current[1] )  



# actions
move_ = "MOVE from {} to {}."
jump_ = "JUMP from {} to {}."
exit_ = "EXIT from {}."


def findPath(data):

    #creates an empty board
    board = Board(data)

    # a star algorithim
    # nodes for which we have calculated the f cost and need to be evaluated
    open_nodes = set()
    # nodes which we have evaluated
    closed_nodes = set()
    #queue that stores the f_cost of each value
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
        
        #a= time.time()
        currentNode = f_cost_queue.get()
        #print("--- %s seconds ---" % (time.time() - a))
        # print(currentNo)
        #moves currentNode from open set to closed set
       ##print(currentNode)
       #removes item if present
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
                    # print(traversal_cost)
                    
                    if (traversal_cost < board.combination_data[child].g_cost):
                      # set f cost of neighbour
                        board.combination_data[child].g_cost = traversal_cost
                        f_cost_queue.put(child, traversal_cost + board.combination_data[child].h_cost)
                        # set parent of neighbour to curr   ent
                        board.combination_data[child].parent = currentNode
                        # if neighbour not in open, add neighbour to open

    #board.printBoard()

#returns a list of the node locations that can be visited from the current node
#If a jump is required it will include first the location of the jumped tile
# than the location of the target tile
#example return value [Location, [jumpedLocation, Location], atLocation]
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



def find_lowest_scoring(open_nodes, board):
    lowestScore= sys.maxsize
    lowestScoringComb = None
    for comb in open_nodes:
        if board.combination_data[comb].f_cost != None and board.combination_data[comb].f_cost< lowestScore :
            lowestScoringComb = comb
            lowestScore = board.combination_data[comb].f_cost
    return lowestScoringComb       

def print_path(starting_node, target_node, board):
    '''prints the traversal path'''

    # base condition
    if board.combination_data[target_node].parent != starting_node:
        print_path(starting_node, board.combination_data[target_node].parent, board)

    move_start = board.combination_data[target_node].parent.coords - target_node.coords
    move_end =  target_node.coords - board.combination_data[target_node].parent.coords

    # some nasty ass code, need to fix the popping
    if move_end:
        move_start= move_start.pop()
        move_end = move_end.pop()

        if move_end in adjacentnodes(move_start):
            move = move_.format(move_start, move_end)
            debugger.update(move_start, move_end)
        else :
            move = jump_.format(move_start, move_end)
            debugger.update(move_start, move_end)
    else:
        m = move_start.pop()
        move= exit_.format(m)
        debugger.piece_locns.remove(m)

    debugger.print_board(message=move)
    time.sleep(0.75) # sleep used to show the pieces moving in a cinematic fashion
    #print(move)



