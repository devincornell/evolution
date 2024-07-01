
#example_cython.pyx
cpdef int test(int x):
    cdef int y = 0
    cdef int i
    for i in range(x):
        y += i
    return y

cpdef int test2(int x):
    cdef int y = 0
    cdef int i
    for i in range(x):
        y += i
    return y


