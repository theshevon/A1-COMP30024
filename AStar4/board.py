class Board:

    # size of the board
    size = 3
   
    # exit locations for the pieces 
    all_exit_nodes   = {
                            "red"   : [ (3,-3), (3,-2),  (3,-1),  (3,0)  ],
                            "blue"  : [ (-3,0), (-2,-1), (-1,-2), (0,-3) ],
                            "green" : [ (-3,3), (-2,3),  (-1,3),  (0,3)  ]
                        }

    # coefficents for lines through exits (cf[0]q + cf[1]r + cf[2] = 0) 
    exit_line_cfs = {"blue" : (1, 1, 3) , "red": (1, 0, -3), "green" : (0, 1, -3) }

    all_nodes          = set()
    traversable_nodes  = set()

    def __init__(self, data):
        self.initialise_nodes(data["colour"], data["blocks"])
    
    def initialise_nodes(self, colour, block_locations):
        '''creates and updates lists, one to store the all the node and another
           to store the list of nodes that can actually be traversed'''

        # create all the nodes
        ran = range(-self.size, self.size+1)
        for node in [(q,r) for q in ran for r in ran if -q-r in ran]:
            
            self.all_nodes.add(node)

            if list(node) not in block_locations:
                self.traversable_nodes.add(node)

    def get_heuristic_cost(self, node_group, colour):
        '''adds the heuristic cost for the node group'''

        cost = 0
        for node in node_group.nodes:
            cost += self.get_distance_estimate(node, self.exit_line_cfs[colour])
        
        return cost

    def get_distance_estimate(self, node, cfs):
        '''returns the minimum possible moves from each node to any exit nodes'''
        
        # shortest number of 'move' actions to reach an exit node
        min_move_cost = abs(cfs[0] * node[0] + cfs[1] * node[1] + cfs[2])

        # shortest number of  'jump' actions to reach an exit node
        min_jump_cost = min_move_cost // 2 + min_move_cost % 2 + 1

        return min_jump_cost

    def get_neighbouring_nodes(self, node):
        '''returns a list of possible neighbouring nodes'''

        neighbours = []

        r_start = node[1]
        r_end = node[1] + 2
        col = 0
        for q in range(node[0]-1, node[0]+2):
            for r in range(r_start, r_end):
                possible_neighbour = (q,r)

                if possible_neighbour != node:
                    neighbours.append(possible_neighbour)

            col += 1
            
            if col == 1:
                r_start -= 1
            
            if col == 2:
                r_end -= 1

        return neighbours

    def get_landing_node(self, curr_node, node_to_jump_over):
        '''returns the landing node when when jumping from one node over another.
           returns None if the landing node is not on the board (i.e. a jump 
           isn't possible)'''

        q = 2 * node_to_jump_over[0] - curr_node[0]
        r = 2 * node_to_jump_over[1] - curr_node[1]

        landing_location = (q,r)

        return landing_location if landing_location in self.traversable_nodes else None
        
    def is_on_board(self, node):
        '''returns True if a node is on the board'''

        return node in self.all_nodes

    def is_traversable(self, node):
        '''returns True if a node is traversable'''

        return node in self.traversable_nodes