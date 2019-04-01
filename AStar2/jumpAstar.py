# g_cost is the cost from starting node
# h_cost is the cost from the target node
# f_cost = g_cost + h_cost

import math
import helperFunctions
import sys

#Modified so that each node is stored in a dict with location as a key and then stores data
class Node:
    location = None
    parent = []
    g_cost = sys.maxsize
    h_cost = None
    f_cost = None

    def __init__(self, location):
        self.location = location
    # purely for debugging purposes
    def print_info(self):
        print("Parent:", self.parent)
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)
        print("F_Cost:", self.f_cost)

class location:
    qCoord= None
    rCoord = None
    def __init__(self, qCoord, rCoord):
        self.qCoord = qCoord
        self.rCoord = rCoord    
    def __str__(self):
        return "({}, {})".format(self.qCoord,self.rCoord)
    def __hash__(self):
        return hash("{}{}".format(self.qCoord,self.rCoord))
    def __eq__(self, other):
        return (self.qCoord == other.qCoord and self.rCoord == other.rCoord)         
    def toList():
        return [self.qCoord, self.rCoord]
    #returns the coord the location resulting from jumping over an adjacent tile
    def jump(self, adjacent):
        return location(2*adjacent.qCoord -self.qCoord, 
            2*adjacent.rCoord - self.rCoord)     


class Board:
    tiles = {}
    exit_locations = []
    def __init__(self, data):
        self.tiles = self.initialise_nodes()
        self.exit_locations= self.returnExits(data["colour"])
    def initialise_nodes(self):
        '''initialises and returns a list of all the nodes on the board'''
        nodes = {}
        board_size = 3 
        ran = range(-board_size, board_size + 1)
        for q in ran:
            for r in ran:
                if -q-r in ran :
                    node = Node(location(q,r))
                    nodes.update({location(q,r) : node})
        return nodes  
    def getNode(self, location):
        return tile[location]
        #clears everything but the location and heuristic
    def clearBoard(self):
        for tile in self.tiles.values():
            tile.parent = []
            tile.g_cost = sys.maxsize
            tile.f_cost = None
        #Needs to set values back to 0
    def addHeuristic (self,colour):
        for node in self.tiles.values():
            node.h_cost = self.estimateCost( node,colour)

    #returns the min possible moves from each node to any exit nodes
    #Note doesn't inlcude cost of exiting board 
    def estimateCost(self, node, colour):
        #coefficents for line cf[0]q + cf[1]r + cf[2] = 0 
        cf = {"blue" : [1,1,3] , "red": [1,0,-3], "green" : [0,1,-3]}
        
        stepCost = None
        jumpCOst = None
        #Shortest number of nodes between the node and any exit node
        stepCost = abs(cf[colour][0]*node.location.qCoord + cf[colour][1]*node.location.rCoord + cf[colour][2])
        #Shortest number of moves between node and any exit node
        #ie if the piece could jump whenever possible
        jumpCost = stepCost//2 + stepCost%2
        print("Jump Cost: {}, Start Cost: {}", stepCost, jumpCost)
        return jumpCost

    def printBoard(self):
        for location in self.tiles.keys():
            print( "Location: {}".format(location))
            #self.tiles[location].print_info()
            print(self.tiles[location].h_cost)
        print("Number of Tiles:{}".format(len(self.tiles.keys())))


    # exit locations for the pieces for the pieces
    def returnExits(self, colour):
        exits = {
            "red" : [location(3,-3),location(3,-2),location(3,-1),location(3,0)],
            "green" : [location(-3,3), location(-2,3),location(-1,3),location(0,3)],
            "blue" : [location(-3,0),location(-2,-1),location(-1,-2),location(0,-3)]
        }
        return exits[colour]

# actions
move_ = "MOVE from {} to {}."
jump_ = "JUMP from {} to {}."
exit_ = "EXIT from {}."


def findPath(data):
    #creates an empty board
    board = Board(data)
    #fills in the heuristic for the board
    board.addHeuristic(data["colour"])  

    ####Stores set of each type of node
    pieceSet = set(location(piece[0], piece[1]) for piece in data["pieces"])
    blockSet = set(location(block[0], block[1]) for block in data["blocks"])
    #tileSet= ((createBoardSet()-blockSet)-pieceSet)
    #board.printBoard()  

    #need to add as check incase one piece can't find the exit without another moving
    while pieceSet:
        # nodes for which we have calculated the f cost and need to be evaluated
        open_nodes = set()
        # nodes which we have evaluated
        closed_nodes = set()
        board.clearBoard()
        start_loc = pieceSet.pop()
        board.tiles[start_loc].f_cost = 0;
        board.tiles[start_loc].g_cost = 0;
        open_nodes.add(start_loc)
        while open_nodes:

            currentNode = find_lowest_scoring(open_nodes, board)

            #moves currentNode from open set to closed set
            open_nodes.remove(currentNode)
            closed_nodes.add(currentNode)
            if currentNode in board.exit_locations:
                print_path(start_loc, currentNode, board) 
                break
            elif board.tiles[currentNode].f_cost == None :
                print("error no route found")
            else:  
                for neighbour in getExplorableNodes(currentNode, blockSet, pieceSet, board):
                    if neighbour not in closed_nodes:
                        open_nodes.add(neighbour)
                            # if new path to neighbour is shorter or neighbour is not in open
                        traversal_cost = 1 + board.tiles[currentNode].g_cost
                        
                        if (traversal_cost < board.tiles[neighbour].g_cost):
                          # set f cost of neighbour
                            board.tiles[neighbour].g_cost = traversal_cost
                            board.tiles[neighbour].f_cost = traversal_cost + board.tiles[neighbour].h_cost
                            # set parent of neighbour to curr   ent
                            board.tiles[neighbour].parent = currentNode
                            # if neighbour not in open, add neighbour to open
      
                



    #board.printBoard()

#returns a list of the node locations that can be visited from the current node
#If a jump is required it will include first the location of the jumped tile
# than the location of the target tile
#example return value [Location, [jumpedLocation, Location], atLocation]
def getExplorableNodes(currentLocation, blockSet, pieceSet, board):
    explorableNodes = []
    for loc in adjacentnodes(currentLocation):
        if loc in board.tiles.keys():
            if (loc in blockSet) or (loc in pieceSet):
                landingLoc= currentLocation.jump(loc)
                if landingLoc in board.tiles.keys() and landingLoc not in blockSet and landingLoc not in pieceSet:
                    explorableNodes.append(landingLoc)                    
            else:
                explorableNodes.append(loc)         
    return explorableNodes
            

#returns list of adjacent nodes
def adjacentnodes(loc):
    neighbours = []
    r_start = loc.rCoord
    r_end = loc.rCoord + 2
    col = 0
    for q in range(loc.qCoord-1, loc.qCoord+2):
        for r in range(r_start, r_end):
            neighbours.append(location(q,r))
        col += 1
        
        if col == 1:
            r_start -= 1
        
        if col == 2:
            r_end -= 1
 
    return neighbours



def find_lowest_scoring(locations, board):
    lowestScore= sys.maxsize
    lowestScoringCoord = None
    for location in locations:
        if board.tiles[location].f_cost != None and board.tiles[location].f_cost< lowestScore :
            lowestScoringCoord = location
            lowestScore = board.tiles[location].f_cost
    return lowestScoringCoord        



