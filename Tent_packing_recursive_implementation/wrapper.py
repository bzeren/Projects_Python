import lab, json, traceback
import copy
reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test(input_data):
  #f = getattr(solution, input_data["function"])
  #temp = f(**input_data["inputs"])
  return pack(input_data)


def pack(input_data):
  tentSize = copy.deepcopy(input_data["tent_size"])
  missingSquares = copy.deepcopy(input_data["rocks"])
  r = lab.pack(tentSize, missingSquares)

  return r
  

def init():
  return None

  
