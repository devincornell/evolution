

def get_offsets(n: int):
    positions = list()
    for q in range(-n, n+1):
        for r in range(max(-n, -q-n), 1+min(n, -q+n)):
            s = -q - r
            positions.append((q,r,s))
    return positions


