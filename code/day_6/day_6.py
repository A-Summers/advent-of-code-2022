def run_pipeline(raw_data, num_char):
    orig_flags = calc_unique_flags(raw_data, num_char)
    char_num_orig = retrieve_char_num_req(orig_flags)

    return char_num_orig


def calc_unique_flags(raw_data, num_char):
    # creates a list of list of unique flags, for each sequential set of num_char characters,
    # with the final character position in that set
    flags = [[check_if_string_unique(raw_data[i:i + num_char]), i + num_char]
             for i in range(0, len(raw_data)) if len(raw_data[i:i + num_char]) == num_char]

    return flags


def check_if_string_unique(char):
    # checks if a string of letters contains only unique letters
    x = list(set(char))
    x.sort()
    y = list(char)
    y.sort()
    if x == y:
        flag = True
    else:
        flag = False

    return flag


def retrieve_char_num_req(flags):
    # retrieves the number of characters needed to be processed before the first marker is detected
    char_num = next(x[1] for x in flags if x[0] is True)

    return char_num


if __name__ == "__main__":
    with open("./code/day_6/day_6_input.txt") as f:
        raw_data = [line.strip('\n') for line in f][0]

    char_num_marker = run_pipeline(raw_data, num_char=4)
    print("The characters needed to be processed before the first start of packet marker is", char_num_marker)

    char_num_message = run_pipeline(raw_data, num_char=14)
    print("The characters needed to be processed before the first start of message marker is", char_num_message)
