import numpy as np


def visibility_out_array(matrix_data):
    """Creates an array on what trees are visible from outside the grid (1 yes, 0 no)"""
    num_rows = matrix_data.shape[0]
    num_cols = matrix_data.shape[1]
    bool_array = np.zeros(shape=(num_rows, num_cols), dtype=int)

    # loop over rows
    for row in range(num_rows):
        bool_array = horizontal_vis_pipe(matrix_data, bool_array, row, num_cols)

    # loop over cols
    for col in range(num_cols):
        bool_array = vertical_vis_pipe(matrix_data, bool_array, col, num_rows)

    return bool_array


def viewing_dist_array(matrix_data):
    """Creates a multidimensional array for each viewing distance of each tree.
    It ignores the checks for updating the border distances as the scenic scores will be 0 for these"""
    num_rows = matrix_data.shape[0]
    num_cols = matrix_data.shape[1]
    # create a multidimensional array to capture the viewing distances from all 4 directions
    dist_array = np.zeros(shape=(num_rows, num_cols, 4), dtype=int)

    # loop over rows
    for row in range(1, num_rows - 1):
        dist_array = horizontal_dist_pipe(matrix_data, dist_array, row, num_cols)

    # loop over cols
    for col in range(1, num_cols - 1):
        dist_array = vertical_dist_pipe(matrix_data, dist_array, col, num_rows)

    return dist_array


def horizontal_vis_pipe(matrix_data, array, row, num_cols):
    """Pipeline for checking row in both directions for tree visibility, and updates bool array"""
    # loop over cols from left to right
    array = visibility_iterator(matrix_data, array, row,
                                start=0, to=num_cols, by=1, type="col")
    # loop over cols from right to left
    array = visibility_iterator(matrix_data, array, row,
                                start=num_cols-1, to=-1, by=-1, type="col")

    return array


def vertical_vis_pipe(matrix_data, array, col, num_rows):
    """Pipeline for checking column in both directions for tree visibility, and updates bool array"""
    # loop over rows from top to bottom
    array = visibility_iterator(matrix_data, array, col,
                                start=0, to=num_rows, by=1, type="row")

    # loop over rows from bottom to top
    array = visibility_iterator(matrix_data, array, col,
                                start=num_rows-1, to=-1, by=-1, type="row")

    return array


def horizontal_dist_pipe(matrix_data, array, row, num_cols):
    """Looks across a given row in both directions, for distances, and updates array"""
    # loop over cols from left to right (dim represents the layer in the array representing a single distance type)
    array = distance_iterator(matrix_data, array, row,
                              start=1, to=num_cols - 1, by=1, type="col", dim=0)

    # loop over cols from right to left (dim represents the layer in the array representing a single distance type)
    array = distance_iterator(matrix_data, array, row,
                              start=num_cols - 2, to=0, by=-1, type="col", dim=1)

    return array


def vertical_dist_pipe(matrix_data, array, col, num_rows):
    """Looks across a given column in both directions, for distances, and updates array"""
    # loop over rows from top to bottom (dim represents the layer in the array representing a single distance type)
    array = distance_iterator(matrix_data, array, col,
                              start=1, to=num_rows - 1, by=1, type="row", dim=2)

    # loop over rows from bottom to top (dim represents the layer in the array representing a single distance type)
    array = distance_iterator(matrix_data, array, col,
                              start=num_rows - 2, to=0, by=-1, type="row", dim=3)

    return array


def visibility_iterator(matrix_data, array, fixed_val, start, to, by, type):
    """Contains the method for iterating over either rows or columns, and in either direction
    (based on what is supplied in the range arguments). This is only for the visibility calculation in part1"""
    current_max = -1
    # loop over cols
    if type == "col":
        max_in_row = max(matrix_data[fixed_val, 0:])
        for col in range(start, to, by):
            val = matrix_data[fixed_val, col]
            if val > current_max:
                current_max = val
                array[fixed_val, col] = 1
            # if max in row is observed, all the remaining trees must not be visible
            if val == max_in_row:
                break
    # loop over rows
    elif type == "row":
        max_in_col = max(matrix_data[0:, fixed_val])
        for row in range(start, to, by):
            val = matrix_data[row, fixed_val]
            if val > current_max:
                current_max = val
                array[row, fixed_val] = 1
            # if max in column is observed, all the remaining trees must not be visible
            if val == max_in_col:
                break

    return array


def distance_iterator(matrix_data, array, fixed_val, start, to, by, type, dim):
    """Contains the method for iterating over either rows or columns, and in either direction
    (based on what is supplied in the range arguments). This is for the distance calculation in part2"""
    # loop over cols
    if type == "col":
        for col in range(start, to, by):
            val = matrix_data[fixed_val, col]
            tree_view = 0
            # check for each tree, all the trees to the right or left
            for iter_col in range(col + by, to + by, by):
                tree_view += 1
                if matrix_data[fixed_val, iter_col] >= val:
                    break
            # update view array
            array[fixed_val, col, dim] = tree_view

    if type == "row":
        for row in range(start, to, by):
            val = matrix_data[row, fixed_val]
            tree_view = 0
            # check for each tree, all the trees above or below
            for iter_row in range(row + by, to + by, by):
                tree_view += 1
                if matrix_data[iter_row, fixed_val] >= val:
                    break
            # update view array
            array[row, fixed_val, dim] = tree_view

    return array


def calc_scenic_array(dist_array):
    """Calculates an array of scenic scores, based on the multidimensional array of all viewing distances"""
    scenic_array = dist_array[0:, 0:, 0]
    for dim in range(1, 4):
        scenic_array *= dist_array[0:, 0:, dim]

    return scenic_array


if __name__ == "__main__":
    with open("./code/day_8/day_8_input.txt") as f:
        raw_data = [line.rstrip() for line in f]
    matrix = np.array([[int(val) for val in line] for line in raw_data])

    visible_array = visibility_out_array(matrix)
    print("The number of trees visible from outside the grid is", sum(sum(visible_array)))

    distance_array = viewing_dist_array(matrix)
    scenic_array = calc_scenic_array(distance_array)
    print("The highest scenic score possible for any tree is", np.max(scenic_array))



