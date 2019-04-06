import sys

class NodeGroup:

    # set of nodes that make up the group
    nodes = None

    parent = None
    g_cost = sys.maxsize
    h_cost = None
    f_cost = None

    def __init__(self, nodes):
        self.nodes = nodes

    def __eq__(self, other):
        return other and sorted(self.nodes) == sorted(other.nodes)

    def copy(self):
        return NodeGroup(self.nodes)

    # purely for debuggin purposes
    def print_info(self):
        print("Node Group Info:")
        print("Nodes: ", list(self.nodes))
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)
        print("F_Cost:", self.f_cost)
        if self.parent is not None:
            print("Parents: ", list(self.parent.nodes))