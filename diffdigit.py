# https://www.codewars.com/kata/find-the-stray-number/train/python
def stray(a):
  base = a[0] if a[0] == a[-1] or a[0] == a[len(a)/2] else a[-1] if a[-1] == a[len(a)/2] else None
  return base + sum(x - base for x in a)

print stray([1, 1, 1, 1, 1, 1, 2])
