#https://www.codewars.com/kata/simple-fun-number-303-prime-product/train/python
def prime_product(n):
    sums = getSum2(n)
    return max(x*y for x,y in sums)

def getSum(n, primes):
    x, result = 2, [(0, 0)]
    while x < n:
        if x in primes and n-x in primes:
            del primes[x]
            if n-x in primes:
                del primes[n-x]
            result.append((x, n-x))
        x += 1
    return result

def getSum2(n):
    sums = [(0, 0)]
    for x in range(2, n):
        if is_prime(x) and is_prime(n-x):
            sums.append((x, n-x))
    return sums

def is_prime(n):
    """"pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2:
         return False;
    if n % 2 == 0:
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

def sieve(n):
    primes = {x:1 for x in range(2, n+1)}
    for i in range(2, n):
        step = 2 * i
        while step <= n:
            if step in primes:
                del primes[step]
            step += i
    return primes

for x in range(100):
   prime_product(x * 1000)
