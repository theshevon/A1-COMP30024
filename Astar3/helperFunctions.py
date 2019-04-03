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
