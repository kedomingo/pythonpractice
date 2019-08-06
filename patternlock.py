#https://www.codewars.com/kata/screen-locking-patterns/train/python

class Node:
    val = None
    used = False
    next = []

    def __init__(self, val):
        self.val = val

    def setUsed(self):
        self.used = True

    def setUnused(self):
        self.used = False

    def isUsed(self):
        return self.used

    def setNeighbors(self, neighbors):
        self.next = neighbors

    def getNeighbors(self):
        return self.next

def combinations(trails, trail, startnode, length):
    # print "Now at ", startnode.val, " trail: ", readable(trail)
    if length == 1:
        # print "+++Now at ", startnode.val, " Finalizing trail: ", readable(trail)
        trails.append(trail)
        return
    startnode.setUsed()
    for next,via in startnode.getNeighbors():
        if not next.isUsed() and (via == None or via.isUsed()):
            #print "Going to ", next.val
            #print "trail is now ", readable(newtrail)
            combinations(trails, trail + [next], next, length - 1)
    startnode.setUnused()

def readable(trail):
    return "-".join(node.val for node in trail)

a,b,c,d,e,f,g,h,i = Node('A'),Node('B'),Node('C'),Node('D'),Node('E'),Node('F'),Node('G'),Node('H'),Node('I')

# A B C
# D E F
# G H I
a.setNeighbors([ (b,None), (d,None), (e,None), (f,None), (h,None), (c,b), (g,d), (i,e) ])
b.setNeighbors([ (a,None), (c,None), (d,None), (e,None), (f,None), (g,None), (i,None), (h,e) ])
c.setNeighbors([ (b,None), (d,None), (e,None), (f,None), (h,None), (a,b), (g,e), (i,f) ])
d.setNeighbors([ (a,None), (b,None), (c,None), (e,None), (g,None), (h,None), (i,None), (f,e) ])
e.setNeighbors([ (a,None), (b,None), (c,None), (d,None), (f,None), (g,None), (h,None), (i,None) ])
f.setNeighbors([ (a,None), (b,None), (c,None), (e,None), (g,None), (h,None), (i,None), (d,e) ])
g.setNeighbors([ (b,None), (d,None), (e,None), (f,None), (h,None), (a,d), (c,e), (i,h) ])
h.setNeighbors([ (a,None), (c,None), (d,None), (e,None), (f,None), (g,None), (i,None), (b,e) ])
i.setNeighbors([ (b,None), (d,None), (e,None), (f,None), (h,None), (a,e), (c,f), (g,h) ])

def count_patterns_from(firstPoint, length):
    trails = []
    nodes = {'A': a, 'B': b, 'C': c, 'D': d, 'E': e, 'F': f, 'G': g, 'G': h, 'I': i}
    combinations(trails, [nodes[firstPoint]], nodes[firstPoint], length)
    return len(trails)
    for trail in trails:
        print readable(trail)

print count_patterns_from('C', 2)
print count_patterns_from('C', 2)
