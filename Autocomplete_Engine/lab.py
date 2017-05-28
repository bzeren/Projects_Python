def add_to_trie(suffix, trie):

	if suffix == "":
		trie["frequency"] += 1

	elif suffix[0] in trie["children"]:
		child_trie = trie["children"][suffix[0]]
		add_to_trie(suffix[1:], child_trie)

	else:
		child_trie = {"frequency": 0, "children": {}} #empty trie
		trie["children"][suffix[0]] = child_trie
		add_to_trie(suffix[1:], child_trie)


def generate_trie(words):
	trie = {"frequency": 0, "children": {}} #empty trie
	for word in words:
		add_to_trie(word,trie)
	return trie 

def get_subtrie(prefix, trie):
	if prefix == "":
		return trie
	elif prefix[0] in trie["children"]:
		child_trie = trie["children"][prefix[0]]
		return get_subtrie(prefix[1:], child_trie)
	else:
		return {"frequency": 0, "children": {}}

def find_max(trie, N): 
#returns the most frequent node
#return type: tuple of a string and frequency (for the recursion, we need to pass the string)
#base case: when a node doesn't have any children (then it'd return an emptry string and the freq) - not really a base case
	children = trie["children"]
	if children == {}:
		return [("", trie["frequency"])]
	else:
		result_array = [("", trie["frequency"])]
		for child in children:
			child_tree= children[child] #value of child 
			array_of_max = find_max(child_tree, N)
			N_best = []
			for tup in array_of_max:
				N_best.append((child+tup[0],tup[1]))
			result_array += N_best
		sorted_list = sorted(result_array,key=lambda x: x[1],reverse=True)
		if len(result_array)>= N:			
			return sorted_list[0:N]
		else:
			return sorted_list

def autocomplete(trie, prefix, N):

	most_common_suffixes = find_max(get_subtrie(prefix,trie),N)
	result = []
	for suffix in most_common_suffixes:
		if suffix[1] > 0:
			result.append(prefix+suffix[0])
	return result


def single_char_delete(prefix):
	result = set() 
	result.add(prefix[0:-1]) #the word fromm removing the last character
	for i in range(len(prefix)-1):
		new_word = prefix[0:i] + prefix[i+1:]
		result.add(new_word)
	return result

def single_char_replace(prefix):
	all_letters = [chr(i) for i in range(97,123)]
	result = set()
	for letter in all_letters:
		result.add(prefix[0:-1]+letter) #the word fromm removing the last character
	for i in range(len(prefix)-1):
		for letter in all_letters:
			new_word = prefix[0:i] + letter + prefix[i+1:]
			result.add(new_word)
	return result

def single_char_insert(prefix): 

	all_letters = [chr(i) for i in range(97,123)]
	result = set()

	for i in range(len(prefix)):
		for letter in all_letters:
			new_word = prefix[0:i] + letter + prefix[i:]
			result.add(new_word)
	return result

def transpose(prefix):
	result = set()
	for i in range(len(prefix)):
		for j in range(len(prefix)):
			new_list = list(prefix)
			new_list[i] = prefix[j]
			new_list[j] = prefix[i]
			result.add("".join(new_list))
	return result 

def calculate_freq(word, trie):
	return get_subtrie(word, trie)["frequency"]

def all_valid_edits(prefix,trie):
	transpose_set = transpose(prefix)
	insert_set = single_char_insert(prefix)
	delete_set = single_char_delete(prefix)
	replace_set = single_char_replace(prefix)
	all_edits = transpose_set.union(insert_set).union(delete_set).union(replace_set)
	all_edits.remove(prefix) #this mutates the set but doesnt return anything, so it throws error later on when we have a return statement before it
	valid_edits = set()
	for edits in all_edits:
		if calculate_freq(edits,trie) > 0:
			valid_edits.add(edits)
	return valid_edits
	

def autocorrect(trie, prefix, N):
	result = autocomplete(trie, prefix, N)
	if len(result)== N:
		return result
	else: 
		all_val_edits = list(all_valid_edits(prefix,trie))
		print all_valid_edits
		sorted_edits = sorted(all_val_edits, key=lambda word: calculate_freq(word,trie), reverse=True)
		edits_needed = N - len(result)
		if len(sorted_edits)>= edits_needed:			
			return result + sorted_edits[0:edits_needed]
		else:			
			return result + sorted_edits




