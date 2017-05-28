import lab, json, traceback

reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test(input_data):
  result = ""
  try:
      f = getattr(lab, input_data["function"])
      result = f(**input_data["inputs"])
  except:
    result = traceback.format_exc()
  return result

def find_shortest_path( input_data ):
  return lab.find_shortest_path(input_data["graph"], input_data["start"], input_data["end"], input_data["twisty"])

def find_shortest_path_bonus( input_data ):
  return lab.find_shortest_path_bonus(input_data["graph"], input_data["start"], input_data["end"], input_data["num_left_turns"])
