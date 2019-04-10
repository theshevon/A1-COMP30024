class NodeGroupPriorityQueue:

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
        #if the node_group hasn't been in the heap yet or the current path to it is better
        #append the record to the heap and update it's record in the map
        #uses the __eq__ of node_group so it only checks that the positions of the pieces are the same
        #comparing f_cost is the same as comparing g_cost as the heuristics will be the same
        if node_group not in self.node_groups_to_record_map.keys() or priority < self.node_groups_to_record_map[node_group][0] :
        		#we could remove the now redundent record , but it might be time costly O(n)? per operation
        		#However it increases our space complexity leaving it
        		#The algorithim will work fine with duplicate records, because we keep track of closed nodes (and visit the lowest ones first)
        		#self.heap.remove(self.node_groups_to_record_map[node_group])
                self.heap.append(record)
                self.node_groups_to_record_map[node_group] = record
                self.next_element_id += 1

    
    def peek(self):
        '''returns the node group with the lowest f score'''

        return self.heap[0][2]

    def poll(self):
        '''removes and returns the node group with the lowest f cost'''

        node_group = self.heap.pop(0)[2]
        #self.node_groups_to_record_map.pop(node_group)
       	#we could put this back if we wanted to go for the remove redundant node route 
       	#currently if we put this line back in and there is another record of the same node_group in the heap we would get errors
       	#this also increases the space complexity
       	# dictionary will end up being length of closed_nodes + open_nodes 
       	# or we could add a duplicate counter somehow and remove when the counter goes to zero
  

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
