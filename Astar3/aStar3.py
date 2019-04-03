# g_cost is the cost from starting node
# h_cost is the cost from the target node
# f_cost = g_cost + h_cost

import math
import helperFunctions
import sys

#Modified so that each node is stored in a dict with location as a key and then stores data
class Node:
    combination = set()
    parent_combination = set()
    g_cost = sys.maxsize
    h_cost = None
    f_cost = None

    def __init__(self, combination):
        self.combination = combination
    # purely for debugging purposes
    def print_info(self):
        print("Parent:", self._combination)
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)
        print("F_Cost:", self.f_cost)

class combination:
    coords = {}
    def __init__(self, coords):
        self.coords = set(coords) 
    def __str__(self):
        return str(sorted(coords))
    def __hash__(self):
        return hash( tuple(sorted(self.coords)))
    def __eq__(self, other):
        return self.coords == other.coords



def jump(current, adjacent):
    return (2*adjacent[0] - current[0], 
        2*adjacent[1] - current[1] )  


class Board:
    pieces_colour = None
    combination_data = {}
    exit_locations = []
    blockSet = set()
    def __init__(self, data):
        self.pieces_colour = data["colour"]
        self.exit_locations= self.returnExits(self.pieces_colour)
        self.blockSet = [tuple(l) for l in data["blocks"]] 


    def getNode(self, combination):
        return combination_data[combination]
        #clears everything but the location and heuristic

    #adds the heuristic for a combination, if comb is empty (ie all pieces have exited), heuristic is zero
    def addHeuristic (self,combination):
        tempCost = 0
        for coord in combination.coords:
            tempCost += self.estimateCost( coord, self.pieces_colour)
        self.combination_data[combination].h_cost = tempCost
    def addNode(self, comb):
        if comb not in self.combination_data.keys():
            self.combination_data[comb] = Node(comb)
            self.addHeuristic(comb)
    #returns the min possible moves from each node to any exit nodes
    #Note doesn't inlcude cost of exiting board 
    def estimateCost(self, coord, colour):
        #coefficents for line cf[0]q + cf[1]r + cf[2] = 0 
        cf = {"blue" : [1,1,3] , "red": [1,0,-3], "green" : [0,1,-3]}
        
        stepCost = None
        jumpCOst = None
        #Shortest number of nodes between the node and any exit node
        stepCost = abs(cf[colour][0]*coord[0] + cf[colour][1]*coord[1] + cf[colour][2])
        #Shortest number of moves between node and any exit node
        #ie if the piece could jump whenever possible
        #cost includes the cost of exiting the board
        jumpCost = stepCost//2 + stepCost%2 +1
        return jumpCost

    def printBoard(self):
        for comb in self.combination_data.keys():
            print( "combination: {}".format(comb))
            #self.tiles[location].print_info()
            print(self.combination_data[combination].h_cost)
        print("Number of Tiles:{}".format(len(self.combination_data.keys())))

    def returnExits(self, colour):
        exits = {
        "red" : [(3, -3), (3, -2), (3,-1), (3,0)] , 
        "blue" : [(-3, 0), (-2, -1), (-1,-2), (0,-3)], 
        "green" : [(-3, 3), (-2, 3), (-1,3), (0,3)]}
        return exits[colour]

    def withinBoard(self, coord):
        board_size = 3 
        ran = range(-board_size, board_size + 1)
        if (coord[0] in ran) and (coord[1] in ran) and (-coord[0] - coord[1] in ran):
            return True
        else:
            return False

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
    #converting to hashable
    start_loc = [tuple(l) for l in data["pieces"]]
    start_loc = combination(start_loc)
    #adding to the board
    board.addNode(start_loc)

    board.combination_data[start_loc].f_cost = 0;
    board.combination_data[start_loc].g_cost = 0;
    open_nodes.add(start_loc)


    while open_nodes:

        currentNode = find_lowest_scoring(open_nodes, board)
        # print(currentNode)

        #moves currentNode from open set to closed set
        open_nodes.remove(currentNode)
        closed_nodes.add(currentNode)
        if not currentNode.coords:
            # current node is empty hence at exit
            print_path(start_loc, currentNode, board) 
            break
        elif board.combination_data[currentNode].f_cost == None :
            print("error no route found")
        else:  
           # print(currentNode.coords)
            #***************************
            for child in getChildren(currentNode, board):
                #adds the comb to the board if not already initiated
                board.addNode(child)
                if child not in closed_nodes:
                    open_nodes.add(child)
                        # if new path to neighbour is shorter or neighbour is not in open
                    traversal_cost = 1 + board.combination_data[currentNode].g_cost
                    
                    if (traversal_cost < board.combination_data[child].g_cost):
                      # set f cost of neighbour
                        board.combination_data[child].g_cost = traversal_cost
                        board.combination_data[child].f_cost = traversal_cost + board.combination_data[child].h_cost
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

    #some nasty ass code, need to fix the popping
    if move_end:
        move_start= move_start.pop()
        move_end = move_end.pop()

        if move_end in adjacentnodes(move_start):
            move = move_.format(move_start, move_end)
        else :
            move = jump_.format(move_start, move_end)
    else:
        move= exit_.format(move_start.pop())

    print(move)



