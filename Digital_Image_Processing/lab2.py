# The code below seems to have some problems.
# Fix it before implementing the rest of your lab
import math

def width(image):
    return image["width"]

def height(image):
    return image["height"]

def pixel(image, x, y): #gets the value at a certain coordinate
    index = x + width(image)*y #converts coordinates into index in the actual representation
    return image["pixels"][index]

def set_pixel(image, x, y, color): #changes the value at a certain coordinate into a new value (color, represented as an int) 
    index = x + width(image)*y
    image["pixels"][index] = color

def make_image(width, height): #makes an empty image (full of zeroes, all black)
    return {"width": width, "height": height, "pixels": ([0]*width*height)}

# return a new image by applying function f to each pixel of the input image
def apply_per_pixel(image, f):
    result = make_image(width(image), height(image))
    for x in range(width(result)):
        for y in range(height(result)):
            color = pixel(image, x, y)
            set_pixel(result, x, y, f(color)) #FIXED:indented (we want it to be done for every x and y, not just once per x) and x&y order swaped 
    return result
  
def invert(c):
    return abs(255-c)#256 fixed
    
def filter_invert(image):
    return apply_per_pixel(image, invert)

def get_adjacent(image, x, y):
    indices = {}
    index_up = x + width(image)*(y-1)
    index_down = x + width(image)*(y+1)
    index_right = x+1 + width(image)*y
    index_left = x-1 + width(image)*y
    if x != width(image) -1:
        indices["right"] = index_right
    if x != 0:
        indices["left"] = index_left
    if y != height(image)-1:
        indices["down"] = index_down
    if y != 0:
        indices["up"] = index_up

    return indices 

def get_diagonals(image,x,y):
    indices = {}
    index_right_up = x+1 + width(image)*(y-1)
    index_right_down = x+1 + width(image)*(y+1)
    index_left_up = x-1 + width(image)*(y-1)
    index_left_down = x-1 + width(image)*(y+1)

    if x != width(image) -1 and y != 0:
        indices["right_up"] = index_right_up 
    if x != 0 and y != height(image)-1:
        indices["left_down"] = index_left_down
    if x != width(image)-1 and y != height(image)-1:
        indices["right_down"] = index_right_down
    if x != 0 and y != 0:
        indices["left_up"] = index_left_up

    return indices 


def filter_gaussian_blur(image):
    new_image = make_image(width(image), height(image))
    for x in range(width(image)): 
        for y in range(height(image)):
            adjacent_indices = get_adjacent(image,x,y)
            diagonal_indices = get_diagonals(image,x,y)

            value = 0

            for i in adjacent_indices.values(): #itereates over the values of the dict 
                value += 2.0/16*image["pixels"][i] #takes the value of the pixel at index i, multiplies with weight
            for j in diagonal_indices.values():
                value += 1.0/16*image["pixels"][j]
            value += 4.0/16*pixel(image, x, y)
            value = int(round(value))
            if value > 255:
                value = 255
            if value < 0:
                value = 0

            set_pixel(new_image, x, y, value)
    
    
    return new_image



def filter_edge_detect(image):

    new_image = make_image(width(image), height(image))
    
    for x in range(width(image)): 
        for y in range(height(image)):
            adjacent_indices = get_adjacent(image,x,y)
            
            if "left" in adjacent_indices:
                left_val = image["pixels"][adjacent_indices["left"]]
            else:
                left_val=0
            if "right" in adjacent_indices:
                right_val = image["pixels"][adjacent_indices["right"]]
            else:
                right_val=0
            if "up" in adjacent_indices:
                up_val = image["pixels"][adjacent_indices["up"]]
            else:
                up_val=0
            if "down" in adjacent_indices:
                down_val = image["pixels"][adjacent_indices["down"]]
            else:
                down_val=0

            diagonal_indices = get_diagonals(image,x,y)

            if "left_up" in diagonal_indices:
                left_up_val = image["pixels"][diagonal_indices["left_up"]]
            else:
                left_up_val=0
            if "right_up" in diagonal_indices:
                right_up_val = image["pixels"][diagonal_indices["right_up"]]
            else:
                right_up_val=0
            if "left_down" in diagonal_indices:
                left_down_val = image["pixels"][diagonal_indices["left_down"]]
            else:
                left_down_val=0
            if "right_down" in diagonal_indices:
                right_down_val = image["pixels"][diagonal_indices["right_down"]]
            else:
                right_down_val=0

            ox = -1*left_up_val-2*left_val-1*left_down_val+1*right_up_val+2*right_val+1*right_down_val
            oy = -1*left_up_val+1*left_down_val-2*up_val+2*down_val-1*right_up_val+1*right_down_val

            result = int(round(math.sqrt((ox)**2+(oy)**2)))

            if result > 255:
                result = 255
            if result < 0:
                result = 0

            set_pixel(new_image, x, y, result)

    return new_image




# Unit Testing for Neigbors 
# image=make_image(3, 3)
# print get_adjacent(image, 0, 0), " expect: 1, 3"
# print get_diagonals (image, 0, 0), " expect: 4"
# print get_adjacent(image, 2, 0), " expect: 1, 5"
# print get_diagonals (image, 2, 0), " expect: 4"
# print get_adjacent(image, 1, 1), " expect: 1, 3, 5, 7"
# print get_diagonals (image, 1, 1), " expect: 0, 2, 6, 8"
# print get_adjacent(image, 2, 1), " expect: 2, 4, 8"
# print get_diagonals (image, 2, 1), " expect: 1, 7"


# any function of the form "filter_X( image ):", where X denotes the name of
# the filter, can be applied via test.py and the web UI!
# Feel free to go wild and implement your favorite filters once you are done.
# Here are some to inspire you: [GIMP filters](https://docs.gimp.org/en/filters.html)
