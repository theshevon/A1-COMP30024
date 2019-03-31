# g_cost is the cost from starting node
# h_cost is the cost from the target node
# f_cost = g_cost + h_cost

from math import sqrt

class Node:
    location = None
    parent = None
    g_cost = None
    h_cost = None
    f_cost = None

    def __init__(self, location):
        self.location = location
    
    # purely for debugging purposes
    def print_info(self):
        print("Location:", self.location)
        print("Parent:", self.parent)
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)
        print("F_Cost:", self.f_cost)

board_size = 3

# exit locations for the pieces for the pieces
exit_locations = {
    "red" : [[3,-3],[3,-2],[3,-1],[3,0]],
    "blue" : [[-3,3],[-2,3],[-1,3],[0,3]],
    "green" : [[-3,0],[-2,-1],[-1,-2],[0,-3]]
}

# actions
move_ = "MOVE from {} to {}"
jump_ = "JUMP from {} to {}"
exit_ = "EXIT from {}"

def findPath(data):
    ''' finds the shortest path for a node to exit the map'''
    
    # all nodes on the board
    nodes = initialise_nodes()

    # nodes that can actually be traversed
    traversable_nodes = get_traversable_nodes(nodes, data["pieces"], data["blocks"])

    # not all the end points may be accessible
    end_points = get_target_nodes(nodes, data["colour"], data["blocks"])

    # nodes for which we have calculated the f cost and need to be evaluated
    open_nodes = []

    # nodes which we have evaluated
    closed_nodes = []

    for piece in data["pieces"]:

        starting_node = [node for node in nodes if node.location == piece].pop()

        # TODO: adjust to work with mutiple exit nodes
        target_node = end_points[0]
        
        # update all the nodes relative to the starting and target points
        update_nodes(nodes, starting_node, target_node)

        open_nodes.append(starting_node)

        while True:

            # remove node in open list with lowest f cost
            open_nodes.sort(key=lambda x:x.f_cost)
            
            # for debuggin
            # locs = [node.location for node in open_nodes]
            # print(locs[0])

            current_node = open_nodes.pop(0)
            # current_node.print_info()
            closed_nodes.append(current_node)
            
            if current_node.location == target_node.location:
                break

            # for each neighbour of the current node
            for node in get_neighbour_nodes(traversable_nodes, current_node):

                if node in closed_nodes:
                    continue

                # if new path to neighbour is shorter or neighbour is not in open
                traversal_cost = get_dist(current_node.location, node.location) + current_node.f_cost
                if (traversal_cost < node.f_cost) or (node not in open_nodes):

                    # set f cost of neighbour
                    node.f_cost = traversal_cost
                    # set parent of neighbour to current
                    node.parent = current_node
                    
                    # if neighbour not in open, add neighbour to open
                    if node not in open_nodes:
                        open_nodes.append(node)
                
        print_path(starting_node, target_node)


def initialise_nodes():
    '''initialises and returns a list of all the nodes on the board'''

    nodes = []

    r_start = 0
    for q in range(-board_size, board_size+1):
        for r in range(r_start, board_size+1):
            node = Node([q,r])
            nodes.append(node)
        r_start -= 1

    return nodes

def get_traversable_nodes(all_nodes, pieces, blocks):
    '''returns a list of all the nodes that can be traversed'''

    traversable_nodes = []
    for node in all_nodes:
        # a node can be traversed if it isn't occupied by a piece or a block
        if (node.location not in pieces) and (node.location not in blocks):
            traversable_nodes.append(node)

    return traversable_nodes

def get_target_nodes(all_nodes, colour, blocks):
    '''returns a list of accessible exit nodes'''
    
    exits = [location for location in exit_locations[colour] if location not in blocks]
    return [node for node in all_nodes if node.location in exits]

def update_nodes(nodes, starting_node, target_node):
    '''updates the costs for each node'''
    
    for node in nodes:
        node.g_cost = get_dist(node.location, starting_node.location)
        node.h_cost = get_dist(node.location, target_node.location)
        node.f_cost = node.g_cost + node.h_cost
    

def get_neighbour_nodes(traversable_nodes, current_node):
    '''returns a list of neighbouring nodes'''

    neighbours = []

    r_start = current_node.location[1]
    r_end = current_node.location[1] + 2
    col = 0
    for q in range(current_node.location[0]-1, current_node.location[0]+2):
        for r in range(r_start, r_end):
            if [q,r] == current_node.location:
                continue
            for node in traversable_nodes:
                if node.location == [q,r]:
                    neighbours.append(node)
        col += 1
        
        if col == 1:
            r_start -= 1
        
        if col == 2:
            r_end -= 1

    return neighbours

def get_dist(coord1, coord2):
    '''returns the euclidean distance between two node locations'''
    return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def print_path(starting_node, target_node):
    '''prints the traversal path'''

    # base condition
    if target_node.parent != starting_node:
        print_path(starting_node, target_node.parent)
    print(move_.format(target_node.parent.location, target_node.location))

