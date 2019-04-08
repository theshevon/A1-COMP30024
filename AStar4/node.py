import sys

class NodeGroup:

    parent_group = None
    g_cost       = sys.maxsize
    h_cost       = None
    f_cost       = None

    def __init__(self, nodes):

        # set of nodes that make up the group
        self.nodes = set(nodes)

    def __eq__(self, other):
        return other and type(other) == NodeGroup and self.nodes == other.nodes

    def __str__(self):
        return str(sorted(self.nodes))

    def copy(self):
        return NodeGroup(self.nodes)

    # purely for debuggin purposes
    def print_info(self):
        print("Node Group Info:")
        print("Nodes: ", list(self.nodes))
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)
        print("F_Cost:", self.f_cost)
        if self.parent_group is not None:
            print("Parents: ", list(self.parent_group.nodes))