#!/usr/bin/env python3

from main import ConwaysWorld

def test_empty_population():
    grid_size = (5,5)
    initial_population = set()

    cw = ConwaysWorld(initial_population, grid_size)
    cw.progogate_life()
    next_gen = cw.population
    assert next_gen == set()

def test_single_cell():
    grid_size = (5,5)
    initial_population = {(0,0)}
    cw = ConwaysWorld(initial_population, grid_size)
    cw.progogate_life()
    first_gen = cw.population
    assert first_gen == set()

    initial_population = {(5,5)}
    cw = ConwaysWorld(initial_population, grid_size)
    cw.progogate_life()
    first_gen = cw.population
    assert first_gen == set()

    initial_population = {(2,2)}
    cw = ConwaysWorld(initial_population, grid_size)
    cw.progogate_life()
    first_gen = cw.population
    assert first_gen == set()

def test_tetromino():
    grid_size = (5,5)
    initial_population = {(2,2), (1,3), (2,4)}
    expected_first_gen = {(1,3), (2,3)}
    expected_second_gen = set()
    expected_gens = [expected_first_gen, expected_second_gen]
    cw = ConwaysWorld(initial_population, grid_size)
    for item in expected_gens:
        cw.progogate_life()
        assert cw.population == item

def test_block():
    grid_size = (5,5)
    initial_population = {(0,0), (1,0), (0,1), (1,1)}
    expected_population = {(0,0), (1,0), (0,1), (1,1)}
    cw = ConwaysWorld(initial_population, grid_size)
    for _ in range(5):
        cw.progogate_life()
        assert cw.population == expected_population

def test_blinker():
    grid_size = (5,5)
    initial_population = {(2,2), (3,2), (4,2)}
    expected_first_gen = {(3,1), (3,2), (3,3)}
    cw = ConwaysWorld(initial_population, grid_size)
    cw.progogate_life()
    assert cw.population == expected_first_gen
    cw.progogate_life()
    assert cw.population == initial_population


