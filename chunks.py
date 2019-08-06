#https://www.codewars.com/kata/reverse-or-rotate/train/python

def revrot(str, sz):
    if sz <=0 or str == "" or len(str) < sz:
        return ""
    chunks = []
    while len(str) >= sz:
        chunk = str[0:sz]
        chunks.append(chunk[1:]+chunk[0] if sum(int(x) ** 3 for x in list(chunk)) % 2 <> 0 else chunk[-1]+chunk[-2::-1])
        str = str[sz:]
    return "".join(chunks)



print revrot("733049910872815764", 5)
#revrot("123456987654", 6) --> "234561876549"
#revrot("123456 987653", 6) --> "234561 356789"
#revrot("733049910872815764", 5) --> "33047 91089 28157"
#73304 99108 72815 764
#33047 R80199 R51827
#33047 98019 28157
