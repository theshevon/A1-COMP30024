import sys



class Node:
    def __init__(self):
        self.g_cost = sys.maxsize
        self.h_cost = None
        self.parent = None
    # purely for debugging purposes
    def print_info(self):
        print("G_Cost:", self.g_cost)
        print("H_Cost:", self.h_cost)