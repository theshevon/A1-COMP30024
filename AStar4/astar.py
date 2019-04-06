from board import *
from node import *
from priority_queue import NodeGroupPriorityQueue
import sys

 # actions
move_ = "MOVE from {} to {}."
jump_ = "JUMP from {} to {}."
exit_ = "EXIT from {}."


def findPath(data):
    '''finds and prints the optimal path for each piece on the board from its
       starting point to an exit'''
    
    colour         = data["colour"]
    board          = Board(data)
    exit_nodes     = board.all_exit_nodes[colour]

    # nodes for which we have calculated the f cost and need to be evaluated
    open_node_groups = NodeGroupPriorityQueue()

    # nodes which we have evaluated
    closed_node_groups = []

    starting_node_group = NodeGroup([tuple(location) for location in data["pieces"]])
    starting_node_group.g_cost = 0
    open_node_groups.add(0, starting_node_group)

    while not open_node_groups.is_empty():
        
        curr_node_group = open_node_groups.poll()[2]
        closed_node_groups.append(curr_node_group)

        # print(sorted(curr_node_group.nodes))
        if (len(curr_node_group.nodes) == 1) and (curr_node_group.nodes[0] in exit_nodes):
            print("hi") 
            break

        for group in get_possible_successor_groups(board, curr_node_group, exit_nodes):
            
            if group not in closed_node_groups:

                traversal_cost = 1 + curr_node_group.g_cost

                not_in_open = False
                if not open_node_groups.contains(group):
                    not_in_open = True

                if (traversal_cost < group.g_cost) or (not_in_open):

                    # set costs of neighbour
                    group.g_cost = traversal_cost
                    group.h_cost = board.get_heuristic_cost(group, colour)
                    group.f_cost = traversal_cost + group.h_cost

                    # set parent of neighbour to current
                    group.parent = curr_node_group

                    # if neighbour not in open, add neighbour to open
                    if not_in_open:
                        open_node_groups.add(group.f_cost, group)
        
    print_path(starting_node_group, curr_node_group)

def get_possible_successor_groups(board, curr_node_group, exit_nodes):
    '''returns all the possible node groups based on the possible successors
       of each individual node in the group'''
    
    possible_groups = []
    nodes = curr_node_group.nodes

    for node in nodes:

        for explorable_node in get_explorable_nodes(board, node, exit_nodes):

            temp_group = nodes.copy()
            temp_group.remove(node)

            if explorable_node:
                temp_group.append(explorable_node)
        
            possible_groups.append(NodeGroup(temp_group))

    return possible_groups

def get_explorable_nodes(board, curr_node, exit_nodes):
    '''returns a list of all the nodes that can be explored from the current
        node'''
    
    explorable_nodes = []

    for node in board.get_neighbouring_nodes(curr_node):
        
        if board.is_on_board(node):

            if board.is_traversable(node):
                explorable_nodes.append(node)
            else:
                # find possible jumping locations
                landing_node = board.get_landing_node(curr_node, node)
                if landing_node and board.is_traversable(landing_node):
                    explorable_nodes.append(landing_node)
        elif node in exit_nodes:
            explorable_nodes.append(tuple())

    return explorable_nodes

def print_path(starting_node_group, target_node_group):
    '''prints the traversal path'''

    # recursive case
    if target_node_group.parent != starting_node_group:
        print_path(starting_node_group, target_node_group.parent)
    
    print(target_node_group.nodes)

