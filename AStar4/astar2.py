from board import *
from node import *
from priority_queue import NodeGroupPriorityQueue
import sys
from debugger import *
import time

 # actions
move_ = "MOVE from {} to {}."
jump_ = "JUMP from {} to {}."
exit_ = "EXIT from {}."

debugger = Debugger()


# ISSUE:
# NEED TO BE ABLE TO UPDATE THE OPEN NODES PRIORITY QUEUE

def findPath(data):
    '''finds and prints the optimal path for each piece on the board from its
       starting point to an exit'''
    
    colour         = data["colour"]
    board          = Board(data)
    exit_nodes     = board.all_exit_nodes[colour]
    

    # priority queue that stores node groups based on their f costs
    f_costs = NodeGroupPriorityQueue()

    # nodes which we have not evaluated
    open_node_groups = set()

    # nodes which we have evaluated
    closed_node_groups = set()

    starting_node_group = NodeGroup([tuple(location) for location in data["pieces"]])
    starting_node_group.g_cost = 0

    f_costs.add(0, starting_node_group)
    open_node_groups.add(starting_node_group)

    # TODO: reove this before submission
    debugger.set_colour(colour)
    debugger.set_block_locns(data["blocks"])
    debugger.set_piece_locations(starting_node_group.nodes)
    debugger.print_board(starting_node_group.nod
    while open_node_groups:
        
        curr_node_group = f_costs.poll()
        # open_node_groups.clear();
        closed_node_groups.add(curr_node_group)

        if not curr_node_group.nodes:
            break
    
        for group in get_possible_successor_groups(board, curr_node_group, exit_nodes):
            
            # print("Group:", group.nodes)
            if group not in closed_node_groups:

                open_node_groups.add(group)

                traversal_cost = 1 + curr_node_group.g_cost

                if (traversal_cost < group.g_cost):

                    group.g_cost = traversal_cost
                    group.h_cost = board.get_heuristic_cost(group, colour)
                    f_cost = group.g_cost + group.h_cost

                    f_cost_queue.add(f_cost, )



    


                    
        
        # print(len(open_node_groups.heap))
        # print(sorted([n[2].nodes for n in open_node_groups.heap]))
        # break

    print_path(starting_node_group, curr_node_group)

def get_possible_successor_groups(board, curr_node_group, exit_nodes):
    '''returns all the possible node groups based on the possible successors
       of each individual node in the group'''
    
    possible_groups = []
    nodes = curr_node_group.nodes

    for node in nodes:

        for explorable_node in get_explorable_nodes(board, node, nodes, exit_nodes):

            temp_group = nodes.copy()
            temp_group.remove(node)

            if explorable_node:
                temp_group.add(explorable_node)
        
            if temp_group not in possible_groups:
                possible_groups.append(NodeGroup(temp_group))

    # print([group.nodes for group in possible_groups])
    return possible_groups

def get_explorable_nodes(board, node, nodes, exit_nodes):
    '''returns a list of all the nodes that can be explored from the current
        node'''
    
    explorable_nodes = set()
    
    for neighbour_node in board.get_neighbouring_nodes(node):
        
        # print("Neighbour:", neighbour_node)
        if board.is_on_board(neighbour_node):
            # print("Neighbour on board:", neighbour_node)
            if (not board.is_traversable(neighbour_node)) or (neighbour_node in nodes):
                # print("Blocked:", neighbour_node)
                # find possible jumping locations
                landing_node = board.get_landing_node(node, neighbour_node)
                # print("Landing:", landing_node)
                if landing_node and landing_node not in nodes:
                    explorable_nodes.add(landing_node)
            else:
                explorable_nodes.add(neighbour_node)

        elif node in exit_nodes:
            explorable_nodes.add(tuple())

    # print("Explorable:", explorable_nodes)
    return explorable_nodes

def print_path(starting_node_group, target_node_group):
    '''prints the traversal path'''

    # recursive case
    if target_node_group.parent != starting_node_group:
        print_path(starting_node_group, target_node_group.parent)
    
    debugger.set_piece_locations(target_node_group.nodes)
    debugger.print_board()
    time.sleep(0.75)
    # print(target_node_group.nodes)

