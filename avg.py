#https://www.codewars.com/kata/average-array/train/python

def avg_array(arrs):
    ret = arrs[0]
    for row in arrs[1:]:
        ret = [ret[i] + x for i, x in enumerate(row)]
    return [float(x) / len(arrs) for x in ret]


print avg_array([
    [2, 3, 9, 10, 7],
    [12, 6, 89, 45, 3],
    [9, 12, 56, 10, 34],
    [67, 23, 1, 88, 34]
])
