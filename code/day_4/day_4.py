def run_pipeline(raw_data, calc_type):
    processed_input = process_input(raw_data)
    if calc_type == "subset":
        indicator_list = calc_subset_ind_list(processed_input)
    elif calc_type == "overlap":
        indicator_list = calc_overlap_ind_list(processed_input)
    else:
        raise ValueError('Supplied calctype is not properly defined')

    # ind is 1 if subset/overlap and 0 otherwise so can just sum over whole list
    subset_total_val = sum(indicator_list)

    return subset_total_val


def process_input(raw_data):
    # create list of lists of lists - two lists for each elf within a list for each pair
    # split each string in 2 lists by comma
    split_list = [list(sections.split(',')) for sections in raw_data]
    ranges_list = [[range_calc(lst_ele) for lst_ele in pair] for pair in split_list]

    return ranges_list


def range_calc(range_string):
    # create list of two integers that define range boundaries, then create a list of total range
    boundaries = list(map(int, range_string.split('-')))
    range_list = list(range(boundaries[0], boundaries[1]+1))

    return range_list


def calc_subset_ind_list(pair_lists):
    # create list of subset indicators
    subset_ind_list = [check_subset(individ[0], individ[1]) for individ in pair_lists]

    return subset_ind_list


def check_subset(list_1, list_2):
    # check if one of 2 given lists is a subset of the other
    if set(list_1).issubset(set(list_2)) or set(list_2).issubset(set(list_1)):
        flag = 1
    else:
        flag = 0

    return flag


def calc_overlap_ind_list(pair_lists):
    # create list of overlap indicators
    subset_ind_list = [check_overlap(individ[0], individ[1]) for individ in pair_lists]

    return subset_ind_list


def check_overlap(list_1, list_2):
    # check if a pair of lists has any overlap
    if set(list_1) & set(list_2):
        flag = 1
    else:
        flag = 0

    return flag


if __name__ == "__main__":
    with open("./code/day_4/day_4_input.txt") as f:
        raw_data = [line.rstrip() for line in f]

    subset_total_val = run_pipeline(raw_data, calc_type="subset")
    print("Number of assignment pairs where one range fully covers the other is", subset_total_val)

    overlap_total_val = run_pipeline(raw_data, calc_type="overlap")
    print("Number of assignment pairs where there is any overlap is", overlap_total_val)


