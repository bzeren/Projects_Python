import lab, json
reload(lab) # this forces the student code to be reloaded when page is refreshed

def run_test( input_data ):
  trie = lab.generate_trie(input_data["words"])
  if input_data["f"] == "autocorrect": # Tests for correct autocorrect
      return lab.autocorrect(trie, input_data["prefix"], input_data["N"])
  if input_data["f"] == "autocomplete": # Tests for correct autocomplete
      return lab.autocomplete(trie, input_data["prefix"], input_data["N"])
  else: # Tests just for producing the trie
      return trie

trie = None
def autocomplete( input_data ):
  global trie
  if trie is None:
      words = []
      print "LOADING CORPUS"
      with open("resources/words.json", "r") as f:
          words = json.load(f)
          trie = lab.generate_trie(words)
  return lab.autocomplete(trie, input_data["prefix"], input_data["N"])

def autocorrect( input_data ):
   global trie
   if trie is None:
       words = []
       print "LOADING CORPUS"
       with open("resources/words.json", "r") as f:
           words = json.load(f)
           trie = lab.generate_trie(words)
   return lab.autocorrect(trie, input_data["prefix"], input_data["N"])

def init():
  # Nothing to initialize
  return None

init()
