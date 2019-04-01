from board import *
import sys

 # actions
move_ = "MOVE from {} to {}"
jump_ = "JUMP from {} to {}"
exit_ = "EXIT from {}"

def findPath(data):
    
    board          = Board(3, data)
    exit_locations = board.all_exit_locations[data["colour"]]

    # TODO get paths and inspect
    
    for piece in data["pieces"]:

        print("-----moving new piece-----")

        # nodes for which we have calculated the f cost and need to be evaluated
        open_nodes = []

        # nodes which we have evaluated
        closed_nodes = []

        # get starting node and initialise it costs
        starting_node = board.get_node(piece)
        starting_node.f_cost = 0
        starting_node.g_cost = 0

        open_nodes.append(starting_node)

        traversable_nodes = board.get_traversable_nodes(piece, data["blocks"])

        while open_nodes:
            
            # sort the open_nodes in increasing order of f(n)
            open_nodes.sort(key=lambda x:x.f_cost)
            
            # remove node in open list with lowest f cost and expand it
            current_node = open_nodes.pop(0)
            closed_nodes.append(current_node)
            
            # stop if we've reached exit
            if current_node.location in exit_locations:
                break

            # for each neighbour of the current node
            for node in get_explorable_nodes(board, traversable_nodes, current_node):

                if node in closed_nodes:
                    continue

                traversal_cost = 1 + current_node.g_cost
                if (traversal_cost < node.g_cost) or (node not in open_nodes):

                    # set costs of neighbour
                    node.g_cost = traversal_cost
                    node.f_cost = traversal_cost + node.h_cost

                    # set parent of neighbour to current
                    node.parent = current_node
                    
                    # if neighbour not in open, add neighbour to open
                    if node not in open_nodes:
                        open_nodes.append(node)

        print_path(starting_node, current_node, board, exit_locations)

        # clear the node costs for the board
        board.reset_nodes()


def get_explorable_nodes(board, traversable_nodes,curr_node):
    '''returns a list of all the nodes that can be explored from the current
        node'''
    
    explorable_nodes = []

    for node in board.get_neighbouring_nodes(curr_node.location):

        # add node only if traversable
        if node in traversable_nodes:
            explorable_nodes.append(node)
        
        # find possible jumping locations
        landing_node = board.get_landing_node(curr_node, node)
        if landing_node and board.is_on_board(landing_node.location) and landing_node in traversable_nodes:
            explorable_nodes.append(landing_node)

    # print("Current:", curr_node.location)
    # print("Explorables:", [node.location for node in explorable_nodes])
    return explorable_nodes

def print_path(starting_node, target_node, board, exit_locs):
    '''prints the traversal path'''

    # base condition
    if target_node.parent != starting_node:
        print_path(starting_node, target_node.parent, board, exit_locs)

    if target_node in board.get_neighbouring_nodes(target_node.parent.location):
        move = move_.format(target_node.parent.location, target_node.location)
    else :
        move = jump_.format(target_node.parent.location, target_node.location)

    print(move)

    if target_node.location in exit_locs:
        print(exit_.format(target_node.location))    



