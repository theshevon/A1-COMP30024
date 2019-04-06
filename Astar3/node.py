import sys

class Node:
    combination = set()
    parent_combination = set()
    g_cost = sys.maxsize
    h_cost = None
    f_cost = None

    def __init__(self, combination):
        self.combination = combination
    # purely for debugging purposes
    def print_info(self):
        print("Parent:", self.combination)
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)
        print("F_Cost:", self.f_cost)