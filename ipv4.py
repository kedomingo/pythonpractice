# https://www.codewars.com/kata/52e88b39ffb6ac53a400022e
def int32_to_ip(int32):
    s = "{0:b}".format(int32).zfill(32)
    return "{}.{}.{}.{}".format(int(s[0:8], 2), int(s[8:16],2), int(s[16:24],2), int(s[24:32],2))



print int32_to_ip(0)
