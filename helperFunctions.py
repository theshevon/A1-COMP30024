#Helper functions
def createBoardSet():
	ran = range(-3, +3+1)
	CoordSet = set()
	for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
		CoordSet.add(qr)
	return CoordSet	

def AdjacentTiles(coord):
	adjacent = []
	for p in [-1, 1]:
		for r in [-1, 1]:
			if(withinBoard(coord[0] +p , coord[1]+r)):
				adjacent.append(coord[0] +p , coord[1]+r)
	return adjacent 				

def exitCoords(colour):
	exits = {
	"red" : [(3, -3), (3, -2), (3,-1), (3,0)] , 
	"blue" : [(-3, 0), (-2, -1), (-1,-2), (0,-3)], 
	"green" : [(-3, 3), (-2, 3), (-1,3), (0,3)]
	 }