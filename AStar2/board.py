from node import *
from math import sqrt

# TODO ensure appropriate conversion between lists and tuples

class Board:

    # size of the board
    size = None
   
    # exit locations for the pieces 
    all_exit_locations = {
                            "red"   : [ (3,-3), (3,-2),  (3,-1),  (3,0)  ],
                            "blue"  : [ (-3,0), (-2,-1), (-1,-2), (0,-3) ],
                            "green" : [ (-3,3), (-2,3),  (-1,3),  (0,3)  ]
                        }

    # coefficents for lines through exits (cf[0]q + cf[1]r + cf[2] = 0) 
    exit_line_cfs = {"blue" : (1, 1, 3) , "red": (1, 0, -3), "green" : (0, 1, -3) }

    all_nodes            = []
    location_to_node_map = {}

    def __init__(self, size, data):
        self.size = size
        self.initialise_nodes(data["colour"])
    
    def initialise_nodes(self, colour):
        '''initialises a list of all the nodes on the board'''

        # create all the nodes
        ran = range(-self.size, self.size+1)
        for location in [(q,r) for q in ran for r in ran if -q-r in ran]:
            node = Node(location)
            self.all_nodes.append(node)
            self.location_to_node_map[tuple(location)] = node
        
        # add the heuristic costs for each node
        self.add_heuritic_costs(colour)

    def add_heuritic_costs(self, colour):
        '''updates the costs for each node'''
        
        for node in self.all_nodes:
            node.h_cost = self.get_distance_estimate(node, self.exit_line_cfs[colour])

    def get_distance_estimate(self, node, cfs):
        '''returns the minimum possible moves from each node to any exit nodes'''
        
        # shortest number of 'move' actions to reach an exit node
        min_move_cost = abs(cfs[0]*node.location[0] + cfs[1]*node.location[1] + cfs[2])

        # shortest number of  'jump' actions to reach an exit node
        min_jump_cost = min_move_cost // 2 + min_move_cost % 2

        return min_jump_cost

    def get_traversable_nodes(self, piece_locations, block_locations):
        '''returns a list of all the nodes that can be traversed'''

        traversable_nodes = []

        for node in self.all_nodes:
            
            # a node can be traversed if it isn't occupied by the piece or a block
            if (list(node.location) not in piece_locations) and (list(node.location) not in block_locations):
                traversable_nodes.append(node)

        return traversable_nodes

    def get_neighbouring_nodes(self, location):
        '''returns a list of neighbouring nodes'''

        neighbours = []

        r_start = location[1]
        r_end = location[1] + 2
        col = 0
        for q in range(location[0]-1, location[0]+2):
            for r in range(r_start, r_end):
                possible_neighbour = (q,r)
                if possible_neighbour == location:
                    continue
                if self.is_on_board(possible_neighbour):
                    neighbours.append(self.location_to_node_map[possible_neighbour])
            col += 1
            
            if col == 1:
                r_start -= 1
            
            if col == 2:
                r_end -= 1

        return neighbours

    def is_on_board(self, location):
        '''returns True if a location is on the board'''

        return location in self.location_to_node_map

    def reset_nodes(self):
        '''resets all the nodes on the board'''

        for node in self.all_nodes:
            node.reset()

    def get_node(self, location):
        '''returns the node at a particular location'''

        return self.location_to_node_map[location]

    def get_landing_node(self, curr_node, node_to_jump_over):
        '''returns the landing node when when jumping from one node over another.
           if the landing node's location is not on the board (i.e.) a jump isn't
           possible, returns None'''

        q = 2 * node_to_jump_over.location[0] - curr_node.location[0]
        r = 2 * node_to_jump_over.location[1] - curr_node.location[1]

        landing_location = (q,r)

        return self.location_to_node_map[landing_location] if self.is_on_board(landing_location) else None
        
        