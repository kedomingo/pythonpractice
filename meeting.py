#https://www.codewars.com/kata/meeting/train/python
def meeting(s):
    a = ''.join('('+x[1]+', '+x[0]+')' for x in sorted([x.split(':') for x in s.split(';')], key=lambda x: (x[1], x[0]))).upper()

    print a


s = 'Alexis:Wahl;Alexa:Wahl;John:Bell;Victoria:Schwarz;Abba:Dorny;Grace:Meta;Ann:Arno;Madison:STAN;Alex:Cornwell;Lewis:Kern;Megan:Stan;Alex:Korn'
meeting(s)
