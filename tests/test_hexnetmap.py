
import mase
import dataclasses

if __name__ == '__main__':

    hnmap = mase.HexNetMap(10)
    print(hnmap)

    print(hnmap.shortest_path(hnmap.center, hnmap.positions()[-1]))

    exit()


    print()
    print(hnmap[hnmap.center])

    agents = [mase.Agent(i, None) for i in range(10)]

    for agent in agents:
        hnmap.add_agent(agent, hnmap.center)
    print(hnmap[hnmap.center])

