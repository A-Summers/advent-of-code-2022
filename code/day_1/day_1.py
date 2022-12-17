import itertools


def format_input(list_data):
    lists_by_elf = [list(x[1]) for x in
                    itertools.groupby(list_data, lambda x: x == '') if
                    not x[0]]

    return lists_by_elf


def calculate_totals(lists_by_elf):
    # map list values to integer lists, and sum over individual lists
    sum_list = [sum(list(map(int, ls))) for ls in lists_by_elf]

    return sum_list


def largest_n_cals(totals, n):
    # sort list in desc order
    totals.sort(reverse=True)
    top_n_list = totals[:n]

    return top_n_list


if __name__ == "__main__":
    with open("./code/day_1/day_1_input.txt") as f:
        raw_data = [line.rstrip() for line in f]
    lists_by_elf = format_input(raw_data)
    totals_list = calculate_totals(lists_by_elf)

    largest_cal = largest_n_cals(totals_list, 1)
    print("The elf with the largest calories is ", largest_cal)

    largest_3_cals_tot = sum(largest_n_cals(totals_list, 3))
    print("The total calories of the largest 3 elves is ", largest_3_cals_tot)





