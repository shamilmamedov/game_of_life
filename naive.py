#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools

from numpy.core.fromnumeric import repeat


def initial_population(type, size):
    if type == "random":
        ip = np.random.choice([True, False], size=size)
    elif type == "blinker":
        ip = np.zeros(size, dtype=bool)
        ip[4,4:7] = True
    elif type == "toad":
        ip = np.zeros(size, dtype=bool)
        ip[4,4:7] = True
        ip[5,3:6] = True

    return ip

if __name__ == "main":
    arr = []
    # original population
    no_cols = 20
    no_rows = 20
    arr.append(initial_population("toad", (no_rows, no_cols)))

    for k in range(1,30):
        arr.append(np.copy(arr[k-1]))
        for i in range(no_rows):
            for j in range(no_cols):
                cell_ij = arr[k-1][i,j]
                neighbors = set((a,b) for a in (i-1, i, i+1) for b in (j-1, j, j+1))
                neighbors.remove((i,j))
                alive_neighbors = 0
                for ni, nj in neighbors:
                    if (ni >= 0 and ni <no_rows) and (nj >= 0 and nj < no_cols):
                        if arr[k-1][ni,nj] == True:
                            alive_neighbors += 1
                if (cell_ij == True) and (alive_neighbors <2 or alive_neighbors >3): 
                    arr[k][i,j] = False
                if (cell_ij == False) and alive_neighbors==3:
                    arr[k][i,j] = True
                    

    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    im = plt.imshow(arr[0], animated=True)
    def updatefig(i):
        if (i<99):
            i += 1
        else:
            i=0
        im.set_array(arr[i])
        return im,

    ani = animation.FuncAnimation(fig, updatefig, blit=True, repeat=False)
    plt.show()