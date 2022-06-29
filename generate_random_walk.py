import numpy as np
import mase
import random

if __name__ == '__main__':
    #mm = first.ModelMap(10, 5)



    for i in range(5):

        loc_info = mase.random_walk(30, i, include_path=True)

        import json
        with open(f'tmp/walk_{i}.json', 'w') as f:
            json.dump(loc_info, f)



