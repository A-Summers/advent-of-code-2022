
def viewing_dist_array(matrix_data):
    """Creates a multidimensional array for each viewing distance of each tree.
    It ignores the checks for updating the border distances as the scenic scores will be 0 for these"""
    num_rows = matrix_data.shape[0]
    num_cols = matrix_data.shape[1]
    # create a multidimensional array to capture the viewing distances from all 4 directions
    dist_array = np.zeros(shape=(num_rows, num_cols, 4), dtype=int)

    # loop over rows
    for row in range(1, num_rows-1):
        dist_array = horizontal_checks_dist(matrix_data, dist_array, row, num_cols)

    # loop over cols
    for col in range(1, num_cols-1):
        dist_array = vertical_checks_dist(matrix_data, dist_array, col, num_rows)

    return dist_array


def horizontal_checks_dist(matrix_data, array, row, num_cols):
    """Looks across a given row in both directions, for distances, and updates array"""
    # loop over cols from left to right
    for col in range(1, num_cols - 1):
        val = matrix_data[row, col]
        right_view = 0
        # check for each value, all the values to the right (include border)
        for iter_col in range(col + 1, num_cols):
            right_view += 1
            if matrix_data[row, iter_col] >= val:
                break

        # update right view array
        array[row, col, 0] = right_view

    for col in range(num_cols - 2, 0, -1):
        val = matrix_data[row, col]
        right_view = 0
        # check for each value, all the values to the right (include border)
        for iter_col in range(col + 1, num_cols):
            right_view += 1
            if matrix_data[row, iter_col] >= val:
                break

        # update right view array
        array[row, col, 0] = right_view

    # loop over cols from right to left
    current_max = -1
    for col in range(num_cols - 1, -1, -1):
        val = matrix_data[row, col]
        if val > current_max:
            current_max = val
            array[row, col] = 1
        # if max in row is observed, all the remaining trees must not be visible
        if val == max_in_row:
            break

    return array