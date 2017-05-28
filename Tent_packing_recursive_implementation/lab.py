from copy import copy 

def is_valid_sleepingbag(occupied,height,width,sleeping_bag):
	for square in sleeping_bag:
		x1,y1 = square
		if x1 >= width or x1 < 0 or y1 >= height or y1 < 0 or (x1,y1) in occupied: #invalid
			return False 
	return True 


def add_sleepingbag(board,sleeping_bag,orientation):

	dimensions = board["dimensions"]
	people = copy(board["people"]) #list
	occupied = board["occupied"].copy() #set
	for square in sleeping_bag:
		x1,y1 = square
		occupied.add((x1,y1))
	people.append({"anchor": sleeping_bag[0], "orientation":orientation})
	new_board = {"dimensions": dimensions, "people": people, "occupied": occupied}
	return new_board


def get_first_unoccupied_square(occupied, height, width):
	for y in range(height): #what row we are in
		for x in range(width): #what column we are in
			if (x,y) not in occupied:
				return (x,y)
	return None 


def get_children(board):
	children = []
	height = board["dimensions"][1]
	width = board["dimensions"][0]
	occupied = board["occupied"]
	first_square = get_first_unoccupied_square(occupied,height,width)
	if first_square == None:
		return "complete"
	
	(x,y) = first_square

	##Try to place horizontal sleeping bag
	sleeping_bag = [[x,y],[x+1,y],[x+2,y]]
	if is_valid_sleepingbag(occupied,height,width,sleeping_bag):
		new_board = add_sleepingbag(board,sleeping_bag,0)
		children.append(new_board)

	##Place vertical sleeping bag
	sleeping_bag = [[x,y],[x,y+1],[x,y+2]] 
	if is_valid_sleepingbag(occupied,height,width,sleeping_bag):
		new_board = add_sleepingbag(board,sleeping_bag,1)
		children.append(new_board)

	return children 


# dimensions=[3,3]
# people=[]
# missingSquares=set()
# board={"dimensions":dimensions, "people":people,"occupied":missingSquares}
# children=get_children(board)
# for child in children:
# 	print child

# grandchildren=get_children(child)
# for grandchild in grandchildren:
# 	print grandchild


def pack(tentSize, missingSquares):
    # Take care to return a list of dictionaries with keys:
    #  "anchor": [x,y]
    #  "orientation": 0/1
    occupied = set()
    for i in missingSquares:
    	element = tuple(i)
    	occupied.add(element)

    board = {"dimensions":tentSize, "people":[], "occupied":occupied} #the very first board
    queue = [board]

    while len(queue)>0:
    	current_board = queue.pop()
    	result = get_children(current_board)
    	if result == "complete":
    		return current_board["people"]
    	queue += result #concatenate
    return False 

print pack([3,3],[[0,0]])


