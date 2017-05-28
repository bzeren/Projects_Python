def dot_product(current_edge, next_edge):
	dx1= current_edge["end"][0]-current_edge["start"][0]
	dy1= current_edge["end"][1]-current_edge["start"][1]

	dx2= next_edge["end"][0]-next_edge["start"][0]
	dy2= next_edge["end"][1]-next_edge["start"][1]

	return dx1*dx2+dy1*dy2

def cross_product(current_edge, next_edge):
	dx1= current_edge["end"][0]-current_edge["start"][0]
	dy1= current_edge["end"][1]-current_edge["start"][1]

	dx2= next_edge["end"][0]-next_edge["start"][0]
	dy2= next_edge["end"][1]-next_edge["start"][1]

	return dx1*dy2-dy1*dx2

def get_turn_type(current_edge, next_edge):
	if cross_product(current_edge,next_edge) == 0:
		if dot_product(current_edge,next_edge) < 0:
			return "u-turn"
		else:
			return "straight"
	if cross_product(current_edge,next_edge) < 0:
		return "left"
	return "right"


def get_next_graph(graph, edge_history,twisty):
	current_position=edge_history[-1]["end"]
	current_edge=edge_history[-1]
	all_next_graph=[]
	
	for next_edge in graph:
		# if next_edge not in edge_history:			

		if current_position == next_edge["start"] and next_edge not in edge_history:
			turn_type=get_turn_type(current_edge,next_edge)
			if twisty:
				if turn_type == "left" or turn_type == "right":
					all_next_graph.append(next_edge)
			else:
				if turn_type == "straight" or turn_type == "right":
					all_next_graph.append(next_edge)

	return all_next_graph

def init_agenda(graph,start):
	agenda = [] #list of edge histories which are lists of dictionaries
	for edge in graph:
		if start == edge["start"]:
			agenda.append([edge])
	return agenda


def find_shortest_path(graph, start, end, twisty):
    # Remember to return a list of graph as defined in README
    # i.e.: [{"start":[x1,y1], "end":[x2,y2]}, {"start":[x2,y2], "end":[x3,y3]}]
    agenda = init_agenda(graph,start)
    while agenda:
    	edge_history = agenda.pop(0)
    	if edge_history[-1]["end"] == end:
    		return edge_history

    	all_next_graph = get_next_graph(graph,edge_history,twisty)
    	for new_edge in all_next_graph:
    		agenda.append(edge_history+[new_edge])

    return None


## BONUS
def find_shortest_path_bonus(graph, start, end, num_left_turns):
    # Remember to return a list of graph as defined in README
    # i.e.: [{"start":[x1,y1], "end":[x2,y2]}, {"start":[x2,y2], "end":[x3,y3]}]
    return []
