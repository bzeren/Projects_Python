"""6.009 Lab 5 -- Mines"""

import copy

def dump(game):
    """Print a human-readable representation of game.

    Arguments:
       game (dict): Game state


    >>> dump({'dimensions': [1, 2], 'mask': [[False, False]], 'board': [['.', 1]]})
    dimensions: [1, 2]
    board: ['.', 1]
    mask:  [False, False]
    """
    lines = ["dimensions: {}".format(game["dimensions"]),
             "board: {}".format("\n       ".join(map(str, game["board"]))),
             "mask:  {}".format("\n       ".join(map(str, game["mask"])))]
    print("\n".join(lines))


def count_bomb_neighbors(r, c, bombs):
    """
    Counts the number of bomb neighbors a square has. 

    Args:
        r (int): the y coordinate of the square whose neighbors we are counting
        c (int): the x coordinate of the square whose neighbors we are counting
        bombs (list): List of bombs, given in (row, column) pairs

    Returns:
        count (int): number of neighbors 

    >>> count_bomb_neighbors(1,2,[(0,1),(0,2),(1,0),(2,3)]) 
    3

    """

    count = 0
    for dr in range(-1,2):
        for dc in range(-1,2):
            if (r+dr,c+dc) in bombs: 
                count += 1
    return count 

def new_game(num_rows, num_cols, bombs):
    
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.

    Args:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs

    Returns:
       A game state dictionary

    >>> dump(new_game(2, 4, [(0, 0), (1, 0), (1, 1)]))
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, False, False, False]
           [False, False, False, False]

    """
    dimensions = [num_rows, num_cols]

    board = []

    for r in range (num_rows):
        row =[]
    	for c in range (num_cols): 
    		if (r,c) in bombs:
    			row.append('.')
    		else:
    			row.append(count_bomb_neighbors(r, c, bombs))
        board.append(row)

    mask = [[False for i in range (num_cols)] for j in range (num_rows)]

    game_dict = {"dimensions": dimensions, "board": board, "mask":mask}

    return game_dict 


def dig(game, row, col):
    """Recursively dig up (row, col) and neighboring squares.

    Update game["mask"] to reveal (row, col); then recursively reveal (dig up)
    its neighbors, as long as (row, col) does not contain and is not adjacent to
    a bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    Args:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       Tuple[str,int]: A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 3)
    ('victory', 4)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, True, True, True]
           [False, False, True, True]

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 0)
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [True, True, False, False]
           [False, False, False, False]
    """
    
    num_rows = game["dimensions"][0]
    num_cols = game["dimensions"][1]
    board = game["board"]
    mask = game["mask"]

    game_status = 'ongoing' #defaulting to ongoing, and checking if there is defeat or victory

    if row >= num_rows or col >= num_cols:
        return (game_status,0)

    if mask[row][col] == True:
        victory = True 
        for r in range(num_rows):
            for c in range(num_cols):
                if board[r][c] == '.' and mask[r][c] == True:
                    victory = False
                    
                elif board[r][c] != '.' and mask[r][c] == False:
                    victory = False 
                    
        if victory:
            game_status = 'victory'

        return (game_status,0)


    mask[row][col] = True 



    count = 1


    if board[row][col] == 0:
        for dr in range(-1,2):
            for dc in range(-1,2):
                #check to make sure the square is not out of bounds
                if row+dr < num_rows and row+dr >= 0 and col+dc < num_cols and col+dc >= 0:
                    if not mask [row+dr][col+dc]:
                        result = dig(game, row+dr, col+dc)
                        count += result[1]

    if board[row][col] == '.':
        game_status = 'defeat'
    else:    
        victory = True 
        for r in range(num_rows):
            for c in range(num_cols):
                if board[r][c] == '.' and mask[r][c] == True:
                    victory = False
                    
                elif board[r][c] != '.' and mask[r][c] == False:
                    victory = False 
                    
        if victory:
            game_status = 'victory'    
    
    #if removing a tile reveals a 0, then the surrounding squares are also revealed
      
    return (game_status,count)             
    

def render(game, xray=False):
    """Prepare a game for display.

    Returns a two-dimensional array (list of lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A 2D array (list of lists)

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'],
     ['_', '_', '1', '_']]

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '],
     ['.', '.', '1', ' ']]
    """


    result = []
    num_rows = game["dimensions"][0]
    num_cols = game["dimensions"][1]
    board = game["board"]
    mask = game["mask"]

    
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            if mask[r][c] or xray:
                if board[r][c] == 0:
                    row.append(" ")
                else:
                    row.append(str(board[r][c]))
            else:
                row.append("_")
        result.append(row)

    return result 


def render_ascii(game, xray=False):
    """Render a game as ASCII art.

    Returns a string-based representation of argument "game".  Each tile of the
    game board should be rendered as in the function "render(game)".

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A string-based representation of game

    >>> print(render_ascii({"dimensions": [2, 4],
    ...                     "board": [[".", 3, 1, 0],
    ...                               [".", ".", 1, 0]],
    ...                     "mask":  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    
    num_rows = game["dimensions"][0]
    num_cols = game["dimensions"][1]
    result = ""
    output = render(game,xray)
    for i in range(num_rows):
        row = output[i]
        for element in row:
            result += element
        if i <num_rows-1:
            result += "\n"

    
    return result


def initiate_array(dims, value):
    """
    takes in a tuple of dimensions and layer (int) and returns an n - dimensional array of values 
    this will be used for initiating board and mask

    >>> initiate_array((2,3,1),True)
    [[[True], [True], [True]], [[True], [True], [True]]]
    """
    if len(dims)== 1: #base case
        row = [value]*dims[0]
        return row

    row = []
    lower_level = initiate_array(dims[1:], value)
    for i in range(dims[0]):
        row.append(copy.deepcopy(lower_level))
    return row 


def get_cell(board,coords):
    """
    takes in board (n-d array) and coordinates (length n tuple) and returns value of cell at that 
    coordinate

    >>> get_cell(initiate_array((2,3,1,2),7),(1,2,0,1))
    7

    """
    if len(coords)==1: #base case (1dim)
        return board[coords[0]]

    x = coords[0]
    subboard=board[x]
    new_coords = coords[1:] #everything except the first one
    return get_cell(subboard,new_coords)


def set_cell(board,coords,value):
    """
    takes in a board and coordinates and a value of the cell at that coordinate and mutates the board
    returns the mutated board 

    >>> get_cell(set_cell(initiate_array((2,3,1,2),4),(1,2,0,1), 99),(1,2,0,1))
    99    
    """
    
    if len(coords)==1: #base case (1dim)
        board[coords[0]] = value
    else: 
        x = coords[0]
        subboard=board[x]
        new_coords = coords[1:] #everything except the first one
        set_cell(subboard,new_coords, value)
    return board


def get_neighbors(dims, coords):
    """
    takes in dims and coords of a cell, and returns the coords of all neighboring cells. 
    assuming the given position is valid (in range)

    >>> print get_neighbors([9,3,6,9],(0,0,0,0))
    [(0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1), (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1, 1), (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 1, 1, 1)]
    """
    neighbors =[]
    level = len(coords) #level of recursion we are at
    if level==2:
        for dr in range(-1,2):
            for dc in range(-1,2):
                if coords[0]+dr < dims[0] and coords[1]+dc < dims[1] and coords[0]+dr >= 0 and coords[1]+dc >= 0:
                    neighbors.append((coords[0]+dr, coords[1]+dc))
        return neighbors

    end = coords[-1] #the one we are adding to the end
    rest = coords[0:-1]

    neighbors_of_n_minus1 = get_neighbors(dims, rest)

    valid_ends = filter(lambda x: (x < dims[level-1] and x >= 0), [end, end+1, end-1])

    for neighbor in neighbors_of_n_minus1:
        for e in valid_ends:
            new_neighbor = neighbor + (e,) #making "e" a tuple
            neighbors.append(new_neighbor)

    if len(dims) == len(coords): #top level of the recursion
        if coords in neighbors: 
            neighbors.remove(coords)
    return neighbors


def is_valid(dims, coords):
    """
    takes in dims and coords, returns True if coords is valid within those dimensions; False otherwise

    >>> is_valid((3,2,4),(3,2,1))
    False
    """
    for i in range(len(coords)):
        if coords[i] >= dims[i] or coords[i] < 0:
            return False
    return True 


def count_nd_bomb_neighbors(dims, coords, bombs):
    """
    Counts the number of bomb neighbors a square has. 

    Args:
        dims (tuple): Tuple of dimensions
        coords (tuple): A length tuple of coordinates 
        bombs (list): List of bombs, given in coordinates

    Returns:
        count (int): number of neighbors 

    >>> count_nd_bomb_neighbors((3,3,3),(1,0,1),[(0,1,1),(1,0,2),(1,0,0),(2,2,0),(2,2,1),(1,1,1)])
    4
    """

    count = 0
    if is_valid(dims,coords):
        for neighbor in get_neighbors(dims, coords):
            if neighbor in bombs:
                count += 1
    return count 


def get_everything(dims):
    """
    takes in dimensions and returns a set of all possible coords

    >>> get_everything((1,2,4))
    set([(0, 1, 1), (0, 0, 2), (0, 1, 2), (0, 0, 1), (0, 1, 3), (0, 0, 0), (0, 1, 0), (0, 0, 3)])

    """
    origin = (0,)*len(dims)
    pointSet = set()
    pointSet.add(origin)
    
    for i in range(len(dims)):
        newSet = set()
        for point in pointSet:
            for x in range(dims[i]):
                newPoint = list(point)
                newPoint[i] = x
                newSet.add(tuple(newPoint))
        pointSet = newSet
         
    
    return pointSet
         

def nd_new_game(dims, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.  This is an N-dimensional version of new_game().

    Args:
       dims (list): Dimensions of the board
       bombs (list): bomb locations as a list of tuples, each an N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> dump(nd_new_game([2, 4, 2], [(0, 0, 1), (1, 0, 0), (1, 1, 1)]))
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, False], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    """
    
    
    board = initiate_array(dims, 0)

    mask = initiate_array(dims, False)

    for coords in bombs:
        set_cell(board, coords,".")
        neighbors = get_neighbors(dims, coords)
        for neighbor in neighbors:
            value = get_cell(board,neighbor)
            if value != ".":
                set_cell(board,neighbor,value+1)


    game_dict = {"dimensions": dims, "board": board, "mask":mask}
    
    return game_dict


def nd_dig(game, coords):
    """Recursively dig up square at coords and neighboring squares.

    Update game["mask"] to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    This is an N-dimensional version of dig().

    Args:
       game (dict): Game state
       coords (tuple): Where to start digging

    Returns:
       A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 3, 0))
    ('ongoing', 8)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, True], [True, True], [True, True]]
           [[False, False], [False, False], [True, True], [True, True]]

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 0, 1))
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, True], [False, True], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    """
    dims = game["dimensions"]
    board = game["board"]
    mask = game["mask"]

    game_status = 'ongoing' #defaulting to ongoing, and checking if there is defeat or victory

    if not is_valid(dims, coords): #is valid
        return (game_status,0)

    if get_cell(mask, coords) == True: #already dug
        
        victory = True 
        for c in get_everything(dims):
            if get_cell(board,c) == '.' and get_cell(mask,c) == True:
                victory = False
                    
            elif get_cell(board,c) != '.' and get_cell(mask,c) == False:
                victory = False 
                    
        if victory:
            game_status = 'victory'

        return (game_status,0)


    set_cell(mask,coords, True)

    count = 1


    if get_cell(board,coords) == 0:
        for neighbor in get_neighbors(dims,coords):
                #check to make sure the square is not out of bounds
               
                    if not get_cell(mask,neighbor):
                        result = nd_dig(game, neighbor)
                        count += result[1]

    if get_cell(board,coords) == '.':
        game_status = 'defeat'
    else:    
        victory = True 
        for c in get_everything(dims):
                if get_cell(board,c) == '.' and get_cell(mask,c) == True:
                    victory = False
                    
                elif get_cell(board,c) != '.' and get_cell(mask,c) == False:
                    victory = False 
                    
        if victory:
            game_status = 'victory'    
    
    return (game_status,count)  


def nd_render(game, xray=False):
    """Prepare a game for display.

    Returns an N-dimensional array (nested lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    This is an N-dimensional version of render().

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       An n-dimensional array (nested lists)

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
    ...                     [[False, False], [False, False], [True, True], [True, True]]]},
    ...           False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                     [[False, False], [False, False], [False, False], [False, False]]]},
    ...           True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    
    dims = game["dimensions"]
    result = initiate_array(dims," ")
    
    board = game["board"]
    mask = game["mask"]

    for coords in get_everything(dims):
        if get_cell(mask,coords) or xray:
            if get_cell(board,coords) == 0:
                set_cell(result,coords," ")
                
            else:
                set_cell(result, coords, str(get_cell(board,coords)))
                
        else:
            set_cell(result, coords, "_")
            
    return result

