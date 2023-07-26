#https://www.codewars.com/kata/common-denominators/train/python
from functools import reduce

def convertFracts(lst):
    if not lst:
        return []
    denom = lcm([y for x, y in lst])
    return [[x * denom / y, denom] for x, y in lst]

# get least common multiple
def lcm(nums):
    primes = {}
    if not nums:
        return primes
    for num in nums:
        factors = getPrimeFactors(num)
        for x, y in factors.iteritems():
            primes[x] = max(y, primes[x] if x in primes else y)
    return reduce(lambda x, y: x * y, [x ** y for x, y in primes.iteritems()])

def getPrimeFactors(num):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    primefactors = [];
    for x in primes:
        while (num % x == 0):
            primefactors.append(x)
            num /= x
    return {x:primefactors.count(x) for x in primefactors}

a = [[2, 7], [1, 3], [1, 12]]
b = [[24, 84], [28, 84], [7, 84]]
print convertFracts(a) ==  b
