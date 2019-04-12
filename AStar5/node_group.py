import sys

class NodeGroup:

    g_cost = sys.maxsize
    h_cost = None

    parent = None

    def __init__(self, nodes):
        self.nodes = set(nodes)

    def __eq__(self, other):
        return type(other) == NodeGroup and self.nodes == other.nodes

    def __hash__(self):
        return hash(tuple(sorted(self.nodes)))

    def __str__(self):
        return str(sorted(self.nodes))
