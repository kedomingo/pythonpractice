# https://www.codewars.com/kata/mexican-wave/train/python
def wave(str):
    return [x for x in [None if str[x] == " " else str[0:x]+str[x].upper()+str[x+1:] for x,y in enumerate(list(str.lower()))] if x is not None]


print wave("two words")
