from ortools.sat.python import cp_model
import pandas as pd
import numpy as np
import json
import sys

print("\n HERE")
print(sys.argv[1:])

input_grid = json.loads(sys.argv[1])
print(input_grid)

print("👩‍🚀")
print(input_grid[0])
print(input_grid[0][2])
print(type(input_grid[0][2]))

#!/usr/bin/env python3
# Copyright 2010-2024 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This model implements a sudoku solver."""


def solve_sudoku():
    """Solves the sudoku problem with the CP-SAT solver."""
    # Create the model.
    model = cp_model.CpModel()

    cell_size = 3
    line_size = cell_size**2
    line = list(range(0, line_size))
    cell = list(range(0, cell_size))

    # initial_grid = [
    #     [0, 6, 0, 0, 5, 0, 0, 2, 0],
    #     [0, 0, 0, 3, 0, 0, 0, 9, 0],
    #     [7, 0, 0, 6, 0, 0, 0, 1, 0],
    #     [0, 0, 6, 0, 3, 0, 4, 0, 0],
    #     [0, 0, 4, 0, 7, 0, 1, 0, 0],
    #     [0, 0, 5, 0, 9, 0, 8, 0, 0],
    #     [0, 4, 0, 0, 0, 1, 0, 0, 6],
    #     [0, 3, 0, 0, 0, 8, 0, 0, 0],
    #     [0, 2, 0, 0, 4, 0, 0, 5, 0],
    # ]
    
    # initial_grid = [
    #     [0, 0, 0, 8, 0, 6, 0, 0, 0],
    #     [0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [5, 0, 0, 0, 0, 0, 0, 7, 0],
    #     [0, 4, 0, 0, 0, 0, 0, 2, 0],
    #     [0, 1, 0, 0, 0, 0, 0, 0, 3],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 3, 0, 0, 0, 0],
    #     [0, 0, 0, 4, 0, 8, 0, 0, 0],
    # ]
    
    initial_grid = input_grid
    
    
    A="A"
    B="B"
    C="C"
    D="D"
    E="E"
    
    clone_grid = [
        [0, 0, 0, 0, 0, 0, A, 0, 0],
        [0, A, 0, 0, 0, B, C, D, 0],
        [B, C, D, 0, 0, 0, E, 0, 0],
        [0, E, 0, 0, A, 0, 0, 0, 0],
        [0, 0, 0, B, C, D, 0, 0, 0],
        [0, 0, 0, 0, E, 0, 0, A, 0],
        [0, 0, A, 0, 0, 0, B, C, D],
        [0, B, C, D, 0, 0, 0, E, 0],
        [0, 0, E, 0, 0, 0, 0, 0, 0],
    ]
    
    # get list of unique nonzero clone elements
    clone_elements = set([x for xs in clone_grid for x in xs if x != 0])

    grid = {}
    for i in line:
        for j in line:
            grid[(i, j)] = model.new_int_var(1, line_size, f"grid {i} {j}")

    # AllDifferent on rows.
    for i in line:
        model.add_all_different(grid[(i, j)] for j in line)

    # AllDifferent on columns.
    for j in line:
        model.add_all_different(grid[(i, j)] for i in line)

    # AllDifferent on cells.
    for i in cell:
        for j in cell:
            one_cell = []
            for di in cell:
                for dj in cell:
                    # print((i * cell_size + di, j * cell_size + dj))
                    one_cell.append(grid[(i * cell_size + di, j * cell_size + dj)])

            model.add_all_different(one_cell)

    # Initial values.
    for i in line:
        for j in line:
            if initial_grid[i][j]:
                model.add(grid[(i, j)] == initial_grid[i][j])
                
    # clone sudoku
    for clone_letter in clone_elements:
        # get index of first clone element
        locations = list(zip(*np.where(np.array(clone_grid) == clone_letter)))
        first_location = locations[0]
        for location in locations[1:]:
            model.add(grid[first_location] == grid[location])

            # print(location)
        # locations = np.argwhere(np.array(clone_grid) == clone_letter)
        # clone_grid.find
        print(locations)
        
        
        

    # Solves and prints out the solution.
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    print('status:', status)
    if status == cp_model.OPTIMAL:
        for i in line:
            print([int(solver.value(grid[(i, j)])) for j in line])
            


solve_sudoku()