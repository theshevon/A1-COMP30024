from board import *
from node_group import *
from priority_queue import *
from math import sqrt
from debugger import *
import time

class PathFinder:
    
    # TODO: remove this
    debugger = Debugger()
    # actions
    move_ = "MOVE from {} to {}."
    jump_ = "JUMP from {} to {}."
    exit_ = "EXIT from {}."

    def __init__(self, data):

        self.board  = Board(data)
        self.colour = data["colour"]
        self.exits  = self.board.get_exit_nodes(self.colour)

        self.open_node_groups   = NodeGroupPriorityQueue()
        self.closed_node_groups = set()

        self.init_node_group = NodeGroup(set([tuple(node) for node in data["pieces"]]))
        self.init_node_group.g_cost = 0
        
        self.open_node_groups.add(0, self.init_node_group)

            # TODO: reove this before submission
        self.debugger.set_colour(data["colour"])
        self.debugger.set_block_locns(data["blocks"])
        self.debugger.set_piece_locations(self.init_node_group.nodes)

    def find_path(self):


    	
        while self.open_node_groups.heap:

            curr_node_group = self.open_node_groups.poll()
            self.closed_node_groups.add(curr_node_group)

            if not curr_node_group.nodes:
                break

            # evaluate all the possible node groups
            for successor_group in self.get_successor_groups(curr_node_group):

                if successor_group not in self.closed_node_groups:
                    
                    traversal_cost = 1 + curr_node_group.g_cost

                    if traversal_cost < successor_group.g_cost:

                        successor_group.g_cost = traversal_cost
                        successor_group.h_cost = self.board.get_heuristic_cost(successor_group, self.colour)
                        f_cost = successor_group.g_cost + successor_group.h_cost

                        successor_group.parent = curr_node_group

                        self.open_node_groups.add(f_cost, successor_group)

            self.open_node_groups.heapify()
            
        self.print_path(curr_node_group)

    def get_successor_groups(self, curr_node_group):
        '''returns the possible successor groups for a given node group'''

        nodes = curr_node_group.nodes
        successor_groups = set()

        for node in nodes:

            # -- find explorable nodes

            explorable_nodes = set()
            
            # if the node is an exit node, add an empty tuple to the explorable set
            if node in self.exits:
                explorable_nodes.add(tuple())

            # find explorable nodes by assessing a node's neighbours
            for neighbour in self.board.get_neighbouring_nodes(node):

                if self.board.is_on_board(neighbour):
                    
                    if (neighbour in self.board.blocked_nodes) or (neighbour in nodes):
                    
                        # add landing node only if it's an unoccupied node on the board
                        landing_node = self.board.get_landing_node(node, neighbour)
                        if landing_node and (landing_node not in nodes):
                            explorable_nodes.add(landing_node)

                    else:
                        explorable_nodes.add(neighbour)
            
            # -- create and add possible successor groups

            for explorable in explorable_nodes:

                temp = nodes.copy()
                temp.discard(node)

                if explorable:
                    temp.add(explorable)

                successor_groups.add(NodeGroup(temp))

        return successor_groups
        
    def get_dist(self, node_1, node_2):
        '''returns the euclidean distance between two nodes'''

        return sqrt((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)

    def print_path(self, target_node_group):
     # recursive case
        if target_node_group.parent != self.init_node_group:
            self.print_path(target_node_group.parent)

        # -- base case

        start = (target_node_group.parent.nodes - target_node_group.nodes).copy().pop()
        end   = (target_node_group.nodes - target_node_group.parent.nodes).copy()


        if end:
            
            end   = end.pop()

            # if the action is to a neighbour, it will be a 'MOVE', otherwise 
            # a 'JUMP'
            if (self.get_dist(start, end) == 1):
                print(self.move_.format(start, end))
                self.debugger.update(start, end)
            else:
                print(self.jump_.format(start, end))
                self.debugger.update(start, end)

        else:
            print(self.exit_.format(start))
            self.debugger.piece_locns.remove(start)

        self.debugger.print_board(message = )
        time.sleep(1) # sleep used to show the pieces moving in a cinematic fashion
        

    

                        
                
            
                        
                        
               
                







        




