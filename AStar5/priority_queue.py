class NodeGroupQueue:

    def __init__(self):
        self.heap = []
        self.node_groups_to_record_map = {}
        self.next_element_id = 0
    
    def is_empty(self):
        '''returns True if the queue is empty'''

        return len(self.heap) == 0
    
    def add(self, priority, node_group):
        '''adds a node group to the heap. If it already exists in the heap,
           update its record'''

        record = (priority, self.next_element_id, node_group)

        if node_group not in self.node_groups_to_record_map:
            self.heap.append(record)

        self.node_groups_to_record_map[node_group] = record

        self.next_element_id += 1
    
    def peek(self):
        '''returns the node group with the lowest f score'''

        return self.heap[0][2]

    def poll(self):
        '''removes and returns the node group with the lowest f cost'''

        node_group = self.heap.pop(0)[2]
        self.node_groups_to_record_map.pop(node_group)

        return node_group

    def heapify(self):
        '''restructures the heap'''
        
        self.heap.sort()

    def get_item_index(self, node_group):
        '''returns True if a particular node group is in the queue'''
        
        node_groups = [item[2] for item in self.heap] 

        try:
            return node_groups.index(node_group)
        except:
            return -1

