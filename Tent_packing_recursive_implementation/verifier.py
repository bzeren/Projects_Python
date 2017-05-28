import traceback

def verify(result, input_data, gold):
    ok = True
    end = False
    message = "looks good, yay!"
    try:
        # There may be multiple valid tilings, so strict equality is not useful.
        # Gold files store the _count_ of tiles to pack (None for impossible cases).

        if gold == False:
            ok = (result == False)
            if not ok:
                message = "Proposed a packing for an impossible tent!"

        elif result == False:
            ok = (gold == False)
            if not ok:
                message = "Failed to find a solution where one exists."

        elif type(result) != list:
            message = ("didn't work :( " + str(result))
            ok = False

        elif len(result) != gold:
            ok = False
            message = "Proposed packing has incorrect number of tents."
        else:
            # validate cover
            (width, height) = input_data["tent_size"]
            covered = input_data["rocks"]
            tent = [0 for _ in range(width*height)]

            xy = lambda x,y:x+y*width

            # mark rocks
            for (rock_x, rock_y) in input_data["rocks"]:
                tent[xy(rock_x,rock_y)] = "r"

            # mark tents
            for bag in result:
                orientation = bag["orientation"]
                anchor = bag["anchor"]
                offset = (1,0) if orientation==0 else (0,1)

                squares = [ (anchor[0]+offset[0], anchor[1]+offset[1]),
                            anchor,
                            (anchor[0]+2*offset[0], anchor[1]+2*offset[1])]

                for (x,y) in squares:
                    loc = xy(x,y)
                    if loc > len(tent) -1:
                        ok = False
                        end = True
                        message = "One of your sleeping bags is not in the tent"
                        break
                    if tent[xy(x,y)] == "r":
                        ok = False
                        message = "Found a sleeping bag over a rock"
                        end = True
                        break
                    elif tent[xy(x,y)] == "b":
                        ok = False
                        end = True
                        message= "Found overlapping sleeping bags"
                        break
                    else:
                        tent[xy(x,y)] = "b"
                if end:
                    break

    except:
        traceback.print_exc();
        ok = False
        message = "CRASHED! :(. See above for details"

    return (ok, message)
