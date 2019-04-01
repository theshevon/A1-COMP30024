import sys

class Node:

    location = None
    parent   = None
    g_cost   = sys.maxsize
    h_cost   = None
    f_cost   = None
    action   = "move"

    def __init__(self, location):
        self.location = location

    def reset(self):
        parent   = None
        g_cost   = sys.maxsize
        f_cost   = None

    # purely for debugging purposes
    def print_info(self):
        print("Location:", self.location)
        print("Parent location:", self.parent.location)
        print("g(n) =", self.g_cost)
        print("h(n) =", self.h_cost)
        print("f(n) =", self.f_cost)