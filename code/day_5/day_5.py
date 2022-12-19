import itertools
import re
from copy import deepcopy


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


def movement_pipeline(formatted_instr, formatted_pos, move_type):
    # high level pipeline for the movement process
    current_pos = deepcopy(formatted_pos)
    for instr in formatted_instr:
        current_pos = move_to_engine(move_to=instr[2], move_from=instr[1],
                                     num_move=instr[0], current_pos=current_pos,
                                     move_type=move_type)

    return current_pos


def move_to_engine(move_to, move_from, num_move, current_pos, move_type):
    # adds the new crates and removes from old, for a given movement
    # the last list will always be the top row, with the last element in that list the row number
    crates_in_new_stack = current_pos[move_to]
    # if empty, there are no crates in stack that we are moving to
    if not crates_in_new_stack:
        top_row = 0
    else:
        top_row = crates_in_new_stack[-1][-1]
    i = 1
    while i <= num_move:
        stack_crates_from = current_pos[move_from]
        if move_type == "9000":
            crate_to_move = stack_crates_from[-i]  # the top crate to move
        elif move_type == "9001":
            crate_to_move = stack_crates_from[-(num_move - i + 1)]  # the earlier crates to move first
        else:
            raise ValueError('Supplied calctype is not properly defined')

        crate_to_move[1] = top_row + i  # update row number
        current_pos[move_to].append(crate_to_move)  # add crate to new position
        i += 1

    current_pos = clean_old_pos(current_pos, move_from, num_move)

    return current_pos


def clean_old_pos(new_dict, move_from, num_move):
    # clean the total crates moved from the old position
    # this is done at the end so it is independent of the move type, which changes the order boxes are added
    i = 1
    while i <= num_move:
        new_dict[move_from].pop()
        i += 1

    return new_dict


def calc_top_row(final_pos):
    # calculates the top row from the final positions
    answer_str = ""
    for key in final_pos:
        crate = final_pos[key][-1][0]
        answer_str += crate

    return answer_str


def move_and_calc_pipe(formatted_instructions, parsed_pos, move_type):
    final_pos = movement_pipeline(formatted_instructions, parsed_pos, move_type)
    top_row = calc_top_row(final_pos)

    return top_row


if __name__ == "__main__":
    with open("./code/day_5/day_5_input.txt") as f:
        raw_data = [line.strip('\n') for line in f]

    orig_position, instructions = split_data(raw_data)

    parsed_pos = format_orig_position(orig_position)
    formatted_instructions = format_instructions(instructions)

    top_row_9000 = move_and_calc_pipe(formatted_instructions, parsed_pos, move_type="9000")
    print("After the original arrangement procedure, the crates on the top are", top_row_9000)

    top_row_9001 = move_and_calc_pipe(formatted_instructions, parsed_pos, move_type="9001")
    print("After the new arrangement procedure, the crates on the top are", top_row_9001)


