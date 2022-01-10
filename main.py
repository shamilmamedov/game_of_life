#!/usr/bin/env python3

import copy
import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class ConwaysWorld:
    """
    Implements Conways's World. In original game the world is endless
    but in this implementation the world size (the grid size) is
    fixed beforehand.
    The grid axes are like that Y is horizonta (---->) and 
    X is vertical with axis pointing down i.e. Y axis rotated  90
    degrees clockwise

    For storing alive cells set is used.
    """
    def __init__(self, initial_polulation, grid_size) -> None:
        """
        :param initial_population: a set containng initial population
        :param grid_size: size of the world given as a tuple 
        """
        self._current_population = initial_polulation
        self._previous_population = set()
        self.max_x = grid_size[0]
        self.max_y = grid_size[1]
        self.min_x = 0
        self.min_y = 0
        self.no_iter = 0

    @property
    def population(self):
        return self._current_population

    def get_neighbors(self, cell_ij):
        """
        Get neighboring cells of a given cell
        :parameter cell_ij: location of a cell neighbors of which to be found
        """
        i, j = cell_ij
        neighbors = set((a,b) for a in (i-1, i, i+1) if self.min_x <= a <= self.max_x 
                                for b in (j-1, j, j+1) if self.min_y <= b <=self.max_y)
        neighbors.remove((i,j))
        return neighbors

    def count_alive_neighbors(self, cell_ij):
        """
        Counts alive cells in a neighborhood of a given cell
        :parameter cell_ij: location of a cell
        """
        neighbors = self.get_neighbors(cell_ij)
        neighbors.intersection_update(self._previous_population)
        return len(neighbors)

    def possible_newborns(self):
        """
        Locations where new cells can be born. Those cells are
        non-alive neighbors of alive cells.
        """
        pn = set()
        for item in self._previous_population:
            neighbors = self.get_neighbors(item)
            pn = set.union(pn, neighbors)
        pn.difference_update(self._previous_population)
        return pn

    def progogate_life(self):
        """
        Propogates life forward.
        """
        if len(self._current_population) == 0:
            return 

        self.no_iter += 1
        self._previous_population = copy.copy(self._current_population)
        pn = self.possible_newborns()

        for item in self._previous_population:
            no_alive_neighbors = self.count_alive_neighbors(item)
            if no_alive_neighbors < 2 or no_alive_neighbors > 3:
                self._current_population.remove(item)

        for item in pn:
            if self.count_alive_neighbors(item) == 3:
                self._current_population.add(item)


class GameOfLife(ConwaysWorld):
    """
    Class inherits ConwaysWorld class and implements visualization
    on top of it.
    Visualization is done using FuncAnimation of matplotlib. Based on 
    grid size and current population sparse boolean matrix is created
    and converted into dense array for visualization. 
    """
    def __init__(self, initial_polulation, grid_size) -> None:
        super().__init__(initial_polulation, grid_size)
        self.fig, self.ax = plt.subplots(figsize=(7,7))
        self.set_visualization_params()
        self.grid = plt.imshow(self.init_grid(), animated=True, cmap='binary')

    def set_visualization_params(self):
        """
        Sets axis parameters for visualization
        """
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

    def create_sparse_population_matrix(self):
        """
        Creates sparse matrix our of current population
        """
        rows = [item[0] for item in self._current_population]
        cols = [item[1] for item in self._current_population]
        data = [True for _ in self._current_population]
        sparse_grid = csr_matrix((data, (rows, cols)), 
                        shape=(self.max_x+1, self.max_y+1), dtype=bool)
        return sparse_grid

    def init_grid(self):
        """
        Initial population to be visualized
        """
        sparse_pop_grid = self.create_sparse_population_matrix()
        return sparse_pop_grid.toarray()

    def play(self):
        """
        Starts the game
        """
        self.ani = animation.FuncAnimation(self.fig, self.update_grid)
        plt.show()

    def update_grid(self,i):
        """
        Updates plots of animation
        """
        if len(self._current_population) > 0:
            sparse_pop_grid = self.create_sparse_population_matrix()
            self.grid.set_array(sparse_pop_grid.toarray())
            self.progogate_life()
        else:
            self.ani.event_source.stop()
            plt.close()
        return self.grid,


def glider(left, grid_size):
    i,j = left
    if i < 0 or (i+1) > grid_size[0] or (j+2) > grid_size[1]:
        raise ValueError("Glider is outside the grid!")
    return {left, (i+1,j+1), (i+1,j+2), (i,j+2), (i-1,j+2)}

def gun(left, grid_size):
    i,j = left
    if ((j-10) < 0 or (j+25) > grid_size[1] or 
        (i-3) <0 or (i+3) > grid_size[0]):
        raise ValueError("Gun is outside the grid!")

    block1 = {(i,j-9), (i,j-10), (i-1,j-9), (i-1,j-10)}
    block2 = {(i-2,j+24), (i-2,j+25), (i-3,j+24), (i-3,j+25)}
    gun_part1 = {left, (i+1,j), (i+2,j+1), (i+3,j+2), (i+3,j+3), (i,j+4), 
                (i+2,j+5), (i,j+6), (i,j+7), (i+1,j+6), (i-1,j+6),
                (i-1,j), (i-2,j+1), (i-3,j+2), (i-3,j+3), (i-2,j+5)}
    gun_part2 = {(i-1,j+10), (i-2,j+10), (i-3,j+10),
                (i-1,j+11), (i-2,j+11), (i-3,j+11),
                (i,j+12), (i-4,j+12), (i,j+14), (i+1,j+14),
                (i-4,j+14), (i-5,j+14)}
    return set.union(gun_part1, gun_part2, block1, block2)


def visulize_population(population, shape):
    rows = [item[0] for item in population]
    cols = [item[1] for item in population]
    data = [True for _ in population]
    sparse_grid = csr_matrix((data, (rows, cols)), 
                    shape=shape, dtype=bool)

    fig, ax = plt.subplots()
    plt.imshow(sparse_grid.toarray(), cmap='binary')
    plt.show()

if __name__ == "__main__":
    # initial_population = {(2,2), (1,3), (2,4)}
    # initial_population = {(2,2), (3,2), (4,2)}
    # initial_population = glider((2,2))
    grid_size = (101,101)
    initial_population = gun((15,25), grid_size)
    print(initial_population)

    # visulize_population(initial_population, grid_size)

    gl = GameOfLife(initial_population, (100,100))
    gl.play()   