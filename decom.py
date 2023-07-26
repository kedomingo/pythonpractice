#https://www.codewars.com/kata/primes-in-numbers/train/python
def primeFactors(num):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    primefactors = [];
    for x in primes:
        while (num % x == 0):
            primefactors.append(x)
            num /= x
    return ''.join('('+str(x)+('**'+ str(y) if y > 1 else '')+')' for x, y in {x: primefactors.count(x) for x in primefactors}.iteritems())


print primeFactors(7775460)
