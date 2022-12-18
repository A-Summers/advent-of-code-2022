import itertools
import re


def split_data(raw_data):
    # split data into two objects, one representing original position, the other for instructions

    list_of_list = [list(x[1]) for x in
                    itertools.groupby(raw_data, lambda x: x == '') if not x[0]]

    orig_position = list_of_list[0]
    instructions = list_of_list[1]
    return orig_position, instructions


def format_instructions(instructions):
    # create lists of lists, of integers for defining the "move" to make at each state
    formatted_lst = [list(map(int, re.findall(r'\d+', ele))) for ele in instructions]

    return formatted_lst


def format_orig_position(orig_position):
    # reverse order so we start from the bottom row and work up
    orig_position.reverse()
    len_line = len(orig_position[0])
    char_ref_dict = create_pos_ref_dict(len_line)
    pos_dict = {}
    # box number is character 2, 6, 10 etc in each string
    for val in range(2, len_line, 4):
        stack_num = list(char_ref_dict.keys())[list(char_ref_dict.values()).index(val)]
        crate_list = create_list_individ_stack(orig_position, val)
        pos_dict[stack_num] = crate_list

    return pos_dict


def create_list_individ_stack(orig_position, string_pos_val):
    # create a list of lists denoting all of the crates and their position for a given stack,
    # where the stack number is determined by the string_pos_val
    crate_list = []
    row_num = 1
    for row in orig_position[1:]:
        # create list of crate types and row position
        crate_type = row[string_pos_val - 1]
        if crate_type.rstrip() != '':
            crate = [crate_type, row_num]
            row_num += 1
            crate_list.append(crate)

    return crate_list


def create_pos_ref_dict(len_line):
    # maps the original stack number (keys) to the position in character string (values)
    values_str_pos = list(range(2, len_line, 4))
    keys_stack = list(range(1, 10))
    ref_dict = {keys_stack[i]: values_str_pos[i] for i in range(len(keys_stack))}

    return ref_dict


if __name__ == "__main__":
    with open("./code/day_5/day_5_input.txt") as f:
        raw_data = [line.strip('\n') for line in f]

    orig_position, instructions = split_data(raw_data)
    formatted_pos = format_orig_position(orig_position)

