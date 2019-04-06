from node import *

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
        return self.combination_data[combination]
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
