import traceback

def verify(result, input_data, gold):
    ok = False
    try:
        if input_data["f"] == "autocorrect":
            gold.sort()
            result.sort()
            ok = (result == gold)
            if not ok:
                message = "Your autocorrect results are incorrect."
        elif input_data["f"] == "autocomplete":
            for answer in gold:
                answer.sort()
            result.sort()
            ok = (result in gold)
            if not ok:
                message = "Your autocomplete results are incorrect."
        else:
            ok = (result == gold)
            if not ok:
                message = "Your trie is incorrect."
        if ok:
            message = "is correct. Hooray!"
    except:
        traceback.print_exc();
        ok = False
        message = "crashed :(. Stack trace is printed above so you can debug."

    return ok, message
