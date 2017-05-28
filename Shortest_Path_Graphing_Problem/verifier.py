import traceback

def check_turn_type(a,b,c):
	if (not isinstance(a[0],int) or not isinstance(a[1],int) or 
		not isinstance(b[0],int) or not isinstance(b[1],int) or 
		not isinstance(c[0],int) or not isinstance(c[1],int)):
		raise TypeError
	v1=(b[0]-a[0],b[1]-a[1])
	v2=(c[0]-b[0],c[1]-b[1])
	cross=v1[0]*v2[1]-v1[1]*v2[0]
	dot = v1[0]*v2[0]+v1[1]*v2[1]
	if cross==0 and dot<0: return 'U'		# U turn
	if cross==0: return 'S'				# straight turn
	if cross<0: return 'L'				# left turn, notice different x-y plane orientation
	return 'R'						# right turn

def check_is_valid(path, edges, source, destination, twisty, numTurns):
    if path[0]["start"] != source:
        return False
    if path[-1]["end"] != destination:
        return False

    if len(path) == 1:
        return path[0] in edges
    else:
        countTurns = 0
        start1 = path[0]['start']
        end1 = path[0]['end']
        
        if path[0] not in edges:
            return False
	
        for i in range(len(path)-1):
            start2 = path[i+1]['start']
            end2 = path[i+1]['end']
            if end1 != start2:
                return False
            if path[i+1] not in edges:
                return False
	    
            ch = check_turn_type(start1, end1, end2);
            if ch=='U':
		    return False
            if ch=='L':
                countTurns+=1
            if ch=='S' and twisty == True:
                return False
           
            start1 = start2
            end1 = end2

        return countTurns<=numTurns or twisty

def verify(result, input_data, gold):
    d = input_data["inputs"]
    ok = False
    message = "is not correct :("
    try:
        if (type(result) == str) or (type(result) == unicode):
            ok = False
            print result
            message = "crashed :( The error message is printed above"
        else:
            if result:
                graph = d["graph"]
                start = d["start"]
                end = d["end"]
                twisty = False
                if "twisty" in d.keys(): twisty = d["twisty"]
                num_left_turns = 0
                if "num_left_turns" in d.keys(): num_left_turns = d["num_left_turns"]

                if check_is_valid(result,graph,start,end,twisty,num_left_turns):
                    result = len(result)
                    ok = (result == gold)
                else:
                    result = "is not a valid path :("
                    ok = False

            ok = (result == gold)
        if ok:
            message = "is correct. Hooray!"
    except:
        traceback.print_exc();
        ok = False
        message = "The result your code produced is wrong, and caused the autograder to crash :( See above for details."

    return ok, message
