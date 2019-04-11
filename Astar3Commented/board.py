from node import *

class Board:
    combination_data = {}
    def __init__(self, data):
        self.pieces_colour = data["colour"]
        self.exit_locations= self.returnExits(self.pieces_colour)
        self.blockSet = [tuple(l) for l in data["blocks"]] 

    #return items from combination_data
    def getNode(self, combination):
        return self.combination_data[combination]
    def get_g_cost(combination):
        return self.combination_data[combination].g_cost
    def get_f_cost(combination): 
        return self.combination_data[combination].f_cost
    def get_parent(combination): 
        return self.combination_data[combination].f_cost

    #adds the heuristic for a combination, if comb is empty (ie all pieces have exited), heuristic is zero
    def addHeuristic (self,combination):
        tempCost = 0
        for coord in combination.coords:
            tempCost += self.estimateCost( coord, self.pieces_colour)
        self.combination_data[combination].h_cost = tempCost

    #initialises a new node and calculates it's heuristic
    def addNode(self, comb):
        if comb not in self.combination_data.keys():
            self.combination_data[comb] = Node()
            self.addHeuristic(comb)
    #Updates a node if the provided values are smaller
    def updateNode(self, comb, cost, parentComb):
        node = self.getNode(comb)
        if cost < node.g_cost :
            node.g_cost = cost
            node.parent = parentComb
            return True
        else:
            return False 


    #returns the min possible moves for each individual piece to leave the board
    def estimateCost(self, coord, colour):
        #coefficents for line cf[0]q + cf[1]r + cf[2] = 0 
        cf = {"blue" : [1,1,3] , "red": [1,0,-3], "green" : [0,1,-3]}
        
        #Shortest number of nodes between the node and any exit
        stepCost = abs(cf[colour][0]*coord[0] + cf[colour][1]*coord[1] + cf[colour][2])
        
        jumpCost = stepCost//2 + stepCost%2 +1
        return jumpCost
    #returns the tiles from which the pieces can exit
    def returnExits(self, colour):
        exits = {
        "red" : [(3, -3), (3, -2), (3,-1), (3,0)] , 
        "blue" : [(-3, 0), (-2, -1), (-1,-2), (0,-3)], 
        "green" : [(-3, 3), (-2, 3), (-1,3), (0,3)]}
        return exits[colour]
    #Returns true if the coord is within the board
    def withinBoard(self, coord):
        board_size = 3 
        ran = range(-board_size, board_size + 1)
        if (coord[0] in ran) and (coord[1] in ran) and (-coord[0] - coord[1] in ran):
            return True
        else:
            return False
