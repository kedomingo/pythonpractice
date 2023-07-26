import math
from functools import reduce
def complete_binary_tree(items, levels = {}, level = 1):
    items.sort()
    if not items:
        return
    root = int(2 ** math.floor(math.log(len(items)) / math.log(2)));
    print root
    return
    try:
        levels[level].append(items[root-1])
    except:
        levels[level] = [items[root-1]]
    complete_binary_tree(items[0:root-1], levels, level+1)
    complete_binary_tree(items[root:], levels, level+1)
    return reduce(lambda x, y: x + y, [nums for level, nums in list(levels.items())])



print (complete_binary_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
