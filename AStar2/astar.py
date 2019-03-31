# g_cost is the cost from starting node
# h_cost is the cost from the target node
# f_cost = g_cost + h_cost

from math import sqrt
import sys

class Node:

    location = None
    parent   = None
    g_cost   = None
    h_cost   = None
    f_cost   = None

    def __init__(self, location):
        self.location = location

    def reset(self):
        location = None
        parent   = None
        g_cost   = None
        h_cost   = None
        f_cost   = None

    # purely for debugging purposes
    def print_info(self):
        print("Location:", self.location)
        print("Parent:", self.parent)
        print("g(n) =", self.g_cost)
        print("h(n) =", self.h_cost)
        print("f(n) =", self.f_cost)

class Board:

    # size of the board
    size = 3
   
    # exit nodes for the pieces 
    exit_nodes = {
                    "red"   : [ Node([3,-3]), Node([3,-2]),  Node([3,-1]),  Node([3,0])],
                    "blue"  : [ Node([-3,3]), Node([-2,3]),  Node([-1,3]),  Node([0,3])],
                    "green" : [ Node([-3,0]), Node([-2,-1]), Node([-1,-2]), Node([0,-3])]
                 }

    all_nodes         = []
    nodes_by_location = {}
    traversable_nodes = []

    def __init__(self, data):

        self.initialise_nodes()
        self.discover_traversable_nodes(data["pieces"], data["blocks"])
        print([node.location for node in self.traversable_nodes])
    
    def initialise_nodes(self):
        '''initialises/ resets a list of all the nodes on the board'''

        r_start = 0
        for q in range(-self.size, self.size+1):
            for r in range(r_start, self.size+1):
                self.all_nodes.append(Node([q,r]))
            r_start -= 1

        return

    def discover_traversable_nodes(self, pieces, blocks):
        '''updates the list of all the nodes that can be traversed'''

        for node in self.all_nodes:
            
            # a node can be traversed if it isn't occupied by a piece or a block
            if (node.location not in pieces) and (node.location not in blocks):
                self.traversable_nodes.append(node)

        return 

    def update_nodes(self, starting_node, target_node):
        '''updates the costs for each node'''
        
        for node in self.all_nodes:
            node.g_cost = self.get_dist(node.location, starting_node.location)
            node.h_cost = self.get_dist(node.location, target_node.location)
            node.f_cost = node.g_cost + node.h_cost

        return

    def get_exit_nodes(self, colour):
        '''returns a list of accessible exit nodes for a particular colour'''

        return self.exit_nodes[colour]

    def get_neighbouring_nodes(self, current_node):
        '''returns a list of accessible neighbouring nodes'''

        neighbours = []

        r_start = current_node.location[1]
        r_end = current_node.location[1] + 2
        col = 0
        for q in range(current_node.location[0]-1, current_node.location[0]+2):
            for r in range(r_start, r_end):
                if [q,r] == current_node.location:
                    continue
                for node in self.traversable_nodes:
                    if node.location == [q,r]:
                        neighbours.append(node)
            col += 1
            
            if col == 1:
                r_start -= 1
            
            if col == 2:
                r_end -= 1

        return neighbours

    def reset_nodes(self):
        '''resets all the nodes on the board'''

        for node in self.all_nodes:
            node.reset()

    def get_dist(self, coord1, coord2):
        '''returns the euclidean distance between two node locations'''

        return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
        

def findPath(data):
    
    board = Board(data)
    exit_nodes = board.get_exit_nodes(data["colour"])[0]
    
    paths = []
    for piece in data["pieces"]:

        # nodes for which we have calculated the f cost and need to be evaluated
        open_nodes = []

        # nodes which we have evaluated
        closed_nodes = []

        starting_node = Node(piece)

        # TODO get closest exit 
        target_node = exit_nodes[0]

        # update all the nodes relative to the starting and target points
        board.update_nodes(starting_node, target_node)

        open_nodes.append(starting_node)

        while True:

            # sort the open_nodes in increasing order of f(n)
            open_nodes.sort(key=lambda x:x.f_cost)
            
            # remove node in open list with lowest f cost
            current_node = open_nodes.pop(0)
            # this node has now been explored
            closed_nodes.append(current_node)
            
            if current_node.location == target_node.location:
                break

            # for each neighbour of the current node
            for node in board.get_neighbouring_nodes(current_node):

                if node in closed_nodes:
                    continue

                # if new path to neighbour is shorter or neighbour is not in open
                traversal_cost = board.get_dist(current_node.location, node.location) + current_node.f_cost
                if (traversal_cost < node.f_cost) or (node not in open_nodes):

                    # set f cost of neighbour
                    node.f_cost = traversal_cost
                    # set parent of neighbour to current
                    node.parent = current_node
                    
                    # if neighbour not in open, add neighbour to open
                    if node not in open_nodes:
                        open_nodes.append(node)

        # clear the node costs for the board
        board.reset_nodes()

        

