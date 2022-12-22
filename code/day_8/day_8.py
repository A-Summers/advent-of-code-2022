import numpy as np


def visbility_out_array(matrix_data):
    """Creates an array on what trees are visible from outside the grid (1 yes, 0 no)"""
    num_rows = matrix_data.shape[0]
    num_cols = matrix_data.shape[1]
    bool_array = np.zeros(shape=(num_rows, num_cols), dtype=int)

    # loop over rows
    for row in range(num_rows):
        bool_array = horizontal_checks_pipe(matrix_data, bool_array, row, num_cols)

    # loop over cols
    for col in range(num_cols):
        bool_array = vertical_checks_pipe(matrix_data, bool_array, col, num_rows)

    return bool_array


def horizontal_checks_pipe(matrix_data, array, row, num_cols):
    """Pipeline for checking row in both directions for tree visibility, and updates bool array"""

    max_in_row = max(matrix_data[row, 0:])
    # loop over cols from left to right
    array = visibility_iterator(matrix_data, array, row, max_in_row,
                                start=0, to=num_cols, by=1, type="col")
    # loop over cols from right to left
    array = visibility_iterator(matrix_data, array, row, max_in_row,
                                start=num_cols-1, to=-1, by=-1, type="col")

    return array


def vertical_checks_pipe(matrix_data, array, col, num_rows):
    """Pipeline for checking column in both directions for tree visibility, and updates bool array"""
    max_in_col = max(matrix_data[0:, col])

    # loop over rows from top to bottom
    array = visibility_iterator(matrix_data, array, col, max_in_col,
                                start=0, to=num_rows, by=1, type="row")

    # loop over rows from bottom to top
    array = visibility_iterator(matrix_data, array, col, max_in_col,
                                start=num_rows-1, to=-1, by=-1, type="row")

    return array


def visibility_iterator(matrix_data, array, fixed_val, max_val, start, to, by, type):
    """Contains the method for iterating either over rows or columns, and in either direction
    (based on what is supplied in the range arguments). This is only for the visibility calculation in part1"""
    current_max = -1
    # loop over cols
    if type == "col":
        for col in range(start, to, by):
            val = matrix_data[fixed_val, col]
            if val > current_max:
                current_max = val
                array[fixed_val, col] = 1
            # if max in row is observed, all the remaining trees must not be visible
            if val == max_val:
                break
    # loop over rows
    elif type == "row":
        for row in range(start, to, by):
            val = matrix_data[row, fixed_val]
            if val > current_max:
                current_max = val
                array[row, fixed_val] = 1
            # if max in column is observed, all the remaining trees must not be visible
            if val == max_val:
                break

    return array


if __name__ == "__main__":
    with open("./code/day_8/day_8_input.txt") as f:
        raw_data = [line.rstrip() for line in f]
    matrix = np.array([[int(val) for val in line] for line in raw_data])
    visible_array = visbility_out_array(matrix)
    print("The number of trees visible from outside the grid is", sum(sum(visible_array)))



