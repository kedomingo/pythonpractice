#https://www.codewars.com/kata/closest-and-smallest/train/python

def closest(str):
    if str == "":
        return []
    weights = [[sum(int(z) for z in list(y)), x, int(y)] for x, y in enumerate(str.split())]
    weights = sorted(weights, key=lambda x: x[0])
    candidates = [];
    minim = 99999999999
    for i in range(1, len(weights)):
        if weights[i][0] - weights[i -1][0] < minim:
            candidates = []
        if weights[i][0] - weights[i -1][0] <= minim:
            minim = weights[i][0] - weights[i -1][0]
            candidates.append([weights[i-1], weights[i]])
    candidates = sorted(candidates, key=lambda x: (x[1][0]-x[0][0], min(x[1][0], x[0][0]), min(x[1][1], x[0][1])))
    return candidates[0]

print closest("315411   165   53195   87   318638   107   416122   121   375312   193 59")
