import heapq

class NodeGroupPriorityQueue:

    def __init__(self):
        self.heap = []
        self.next_element_id = 1
    
    def is_empty(self):
        '''returns True if the queue is empty'''

        return len(self.heap) == 0
    
    def add(self, priority, node_group):
        '''adds a node to the priority queue'''

        heapq.heappush(self.heap, (priority, self.next_element_id, node_group))
        self.next_element_id += 1
    
    def peek(self):
        '''returns the node group with the lowest f score'''

        return self.heap[0][2]

    def poll(self):
        '''removes and returns the node group with the lowest f cost'''

        return heapq.heappop(self.heap)

    def contains(self, node_group):
        node_groups = [item[2] for item in self.heap] 

        return node_group in node_groups