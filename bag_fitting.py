#https://www.codewars.com/kata/packing-your-backpack/train/python

def pack_bagpack(scores, weights, capacity):
    weightsSortedByValue = sortWeightsByValue(scores, weights)
    return pack(weightsSortedByValue, capacity)

def pack(items, limit):
    totalWeight, maxValue = 0, 0
    for i, (weight, value) in enumerate(items):
        if currentWeight + weight <= limit:
            result = pack(items[i+1:], limit, currentWeight + weight, currentValue + value)
            if result > maxValue:
                maxValue = result
    return maxValue

def sortWeightsByValue(scores, weights):
    scoresDict = []
    for i, x in enumerate(scores):
        scoresDict.append((i, scores[i]))

    weightsSortedByValue = []
    for i, value in sorted(scoresDict, key=lambda x: x[1], reverse=True):
        weightsSortedByValue.append((weights[i], value))
    return weightsSortedByValue


#print pack_bagpack([15, 10, 9, 5], [1, 5, 3, 4], 8)
print pack_bagpack([5], [4], 8)
