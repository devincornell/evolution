
from libcpp.vector cimport vector

cpdef int test(int x):
    cdef int y = 0
    cdef int i
    for i in range(x):
        y += i
    return y

cdef class HexPos:
    cdef int q
    cdef int r
    cdef int s
    def __init__(self, q, r, s):
        self.q = q
        self.r = r
        self.s = s

cpdef list get_offsets(int n):
    cdef int q, r, s
    positions = list()
    for q in range(-n, n+1):
        for r in range(max(-n, -q-n), 1+min(n, -q+n)):
            s = -q - r
            positions.append((q,r,s))
    return positions


#cpdef vector[HexPos] get_offsets2(int n):
#    cdef vector[HexPos] positions
#    cdef int q, r, s
#    #positions = list()
#    for q in range(-n, n+1):
#        for r in range(max(-n, -q-n), 1+min(n, -q+n)):
#            s = -q - r
#            positions.push_back(HexPos(q,r,s))
#    return positions


