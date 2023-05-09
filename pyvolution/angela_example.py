import multiprocessing

class CustomFunction:
    def __init__(self, somedata):
        self.somedata = somedata
    
    def __call__(self, ray):
        self.somedata # can access that data
        ray # and also the input ray
        return ray * self.somedata

custom_func = CustomFunction(500)

with multiprocessing.Pool(5) as p:
    out = p.map(custom_func, [1, 2, 3, 4, 5, 6, 7])
    
print(out)