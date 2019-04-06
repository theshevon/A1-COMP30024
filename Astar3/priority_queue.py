import heapq

class BinQueue:

	def __init__(self):
		self.elements = []
		self.id = 0
	def empty(self):
		return len(self.elements)== 0
	def put(self, item , priority):
		self.id+=1
		heapq.heappush(self.elements, (priority, self.id , item))
	def get (self):
		return heapq.heappop(self.elements)[2]
