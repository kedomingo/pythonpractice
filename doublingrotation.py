import math
def who_is_next(names, n):
    if n == 1:
        return names[0]
    i              = n-1
    position       = math.log((i+5)/5.0) / math.log(2)
    nextposition   = math.ceil(position) if position - math.floor(position) != 0 else position
    charsAtNextPos = 5 * (2 ** nextposition) # minimum chars after n where the items are in order
    idxOfNextPos   = charsAtNextPos - 5
    indexFromRight = (idxOfNextPos - i) * 2
    index          = (indexFromRight / charsAtNextPos)
    print index
    print index < 2
    if index < 0.2:
        return names[0]
    if index < 0.4:
        return names[1]
    if index < 0.6:
        return names[2]
    if index < 0.8:
        return names[3]
    return names[4]


names = ["A", "B", "C", "D", "E"]

print who_is_next(names, 2)
