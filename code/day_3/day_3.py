import string


def run_pipeline(raw_data, calc_type):
    if calc_type == "item_rep":
        item_lists = compartments_list(raw_data)
    elif calc_type == "group_as":
        item_lists = groups_list(raw_data)
    else:
        raise ValueError('Supplied calctype is not properly defined')

    common_items = calc_common_string_list(item_lists)
    priority_map = calc_full_dict()
    priority_vals = calc_priority_list(priority_map, common_items)
    priority_sum = sum(priority_vals)

    return priority_sum


def compartments_list(data_list):
    # divide each string into separate lists
    compartment_1 = [rucksack[0:int((len(rucksack)/2))] for rucksack in data_list]
    compartment_2 = [rucksack[int(len(rucksack) / 2):int(len(rucksack))] for rucksack in data_list]
    full_list = list(zip(compartment_1, compartment_2))

    return full_list


def groups_list(data_list):
    # divide each 3 distinct item strings into groups
    groups_list = [data_list[num:num+3] for num in range(0, len(data_list), 3)]

    return groups_list


def calc_common_string_list(item_lists):
    # calculate list of common items in rucksacks
    common_list = [calc_common_string(lst) for lst in item_lists]

    return common_list


def calc_common_string(indivd_list):
    val = 0
    # for a given list of strings - calculate the total intersection
    # for 2 strings, this will do 1 check for intersection, 2 checks for 3 strings etc
    while val < len(indivd_list)-1:
        if val == 0:
            common_characters = ''.join(
                set(indivd_list[val]).intersection(indivd_list[val+1])
            )
        else:
            common_characters = ''.join(
                set(common_characters).intersection(indivd_list[val + 1])
            )
        val += 1

    return common_characters


def calc_full_dict():
    lower_dict = calc_individ_dict(list(string.ascii_lowercase), 1, 27)
    upper_dict = calc_individ_dict(list(string.ascii_uppercase), 27, 53)

    full_dict = lower_dict.copy()
    full_dict.update(upper_dict)

    return full_dict


def calc_individ_dict(keys, lower_rnge, upper_rnge):
    vals = list(range(lower_rnge, upper_rnge))
    individ_dict = {keys[i]: vals[i] for i in range(len(keys))}

    return individ_dict


def calc_priority_list(mapping, item_list):
    priority_list = [mapping[item] for item in item_list]

    return priority_list


if __name__ == "__main__":
    with open("./code/day_3/day_3_input.txt") as f:
        raw_data = [line.rstrip() for line in f]

    common_item_priority = run_pipeline(raw_data, calc_type="item_rep")
    print("The sum of priorities for items common in both compartments is", common_item_priority)

    group_priority = run_pipeline(raw_data, calc_type="group_as")
    print("The sum of priorities for items common in each group is", group_priority)


