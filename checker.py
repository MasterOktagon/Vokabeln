
def visualize_diff(right, inp)->str:
    #print(right, inp)
    s = ""
    i = 0
    j = 0
    while True:
        if i >= len(right):
            return s

        if j >= len(inp):
            s += "$" +right[i:] + "$"
            return s

        if right[i] == inp[j]:
            s += right[i]
            i += 1
            j += 1
        else:
            s += "$" + right[i] + "$"
            i += 1


def visualize_v2(right, inp, depth=0)->tuple[str, int]:
    s = ""
    if max(len(right), len(inp)) > 20:
        return visualize_diff(right, inp), 100

    if right == "":
        return s, len(inp)

    if depth > 50:
        s += "$" + right + "$"
        return s, len(right)

    if inp == "":
        s += "$" + right + "$"
        return s, len(right)

    if right[0] == inp[0]:
        s += right[0]
        d = visualize_v2(right[1:], inp[1:], depth+1)
        return s+d[0], d[1]

    i = visualize_v2(right, inp[1:], depth+1)
    r = visualize_v2(right[1:], inp, depth+1)

    if i[1] < r[1]:
        return i[0], i[1]+1

    s += "$" + right[0] + "$"
    return s+r[0], r[1]+1
