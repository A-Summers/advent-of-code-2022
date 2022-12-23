def generate_dict(raw_data):
    """Create dictionary where keys represent all directories (in full),
     and the values represent the file sizes in that dir + full paths of child directories.
     The first value in the list will be the depth of the associated key path"""
    current_dir = "/"
    current_dir_lst = [current_dir]
    full_dict = {current_dir: [1]}

    for val in raw_data:
        # we can ignore the ls command, as it doesn't add any extra information
        if val[0:7] == "$ cd ..":
            current_dir_lst.pop()
            current_dir = "/" + '/'.join(current_dir_lst[1:])
        # if above not satisfied, but still cd, then it is changing to a new folder
        elif val[0:4] == "$ cd":
            new_folder = val.split("$ cd ", 1)[1]
            current_dir_lst.append(new_folder)
            current_dir = "/" + '/'.join(current_dir_lst[1:])
            full_dict.update({current_dir: [int(len(current_dir_lst))]})
        elif val[0:3] == "dir":
            full_dict = add_child_obj(val, current_dir_lst,
                                      current_dir, full_dict, type="folder")

        elif val.split()[0].isnumeric():
            full_dict = add_child_obj(val, current_dir_lst,
                                      current_dir, full_dict, type="file")

    # sort dict so that first keys are the lowest level of folder structure (i.e. only files)
    sorted_dict = {k: v for k, v in sorted(full_dict.items(), key=lambda item: item[1][0], reverse=True)}

    return sorted_dict


def add_child_obj(val, current_dir_lst, current_dir, full_dict, type):
    """Adds either a folder or file size (based on type), to a parents value in dict"""
    if type == "file":
        new_object = str(val.split()[0])
    elif type == "folder":
        new_folder = val.split("dir ", 1)[1]
        # not changing current dir, so copy list to append new dir to dict
        temp_dir_lst = current_dir_lst.copy()
        temp_dir_lst.append(new_folder)
        new_object = "/" + '/'.join(temp_dir_lst[1:])

    # append this folder/file to their parents key value
    full_dict[current_dir].append(new_object)

    return full_dict


def calc_total_sizes_dict(full_dict):
    """Calculate the size of each directory, exclude first element in values as this is just the depth of the folder"""
    totals_dict = {}
    for keys in full_dict:
        all_values = [totals_dict[values] if not values.isnumeric() else values for values in full_dict[keys][1:]]
        totals_dict.update({keys: sum(list(map(int, all_values)))})

    return totals_dict


def calc_total_size(totals_dict, max):
    """Calculate the total size of the directories for all directory sizes <= max"""
    size_lst = [totals_dict[key] for key in totals_dict if totals_dict[key] <= max]
    total_size = sum(size_lst)

    return total_size


def calc_smallest_size(totals_dict, total_space, needed_space):
    """Calculate the smallest file size that is sufficient for the provided criteria"""
    available_space = total_space - totals_dict["/"]
    min_del_size = needed_space - available_space
    sufficient_dirs = [totals_dict[key] for key in totals_dict if totals_dict[key] >= min_del_size]

    smallest_size = min(sufficient_dirs)

    return smallest_size


if __name__ == "__main__":
    with open("./code/day_7/day_7_input.txt") as f:
        raw_data = [line.rstrip() for line in f][1:]
    full_dict = generate_dict(raw_data)
    total_sizes_dict = calc_total_sizes_dict(full_dict)

    greater_than_100k = calc_total_size(total_sizes_dict, max=100000)
    print("Total sum of directory sizes, where the directories are at most 100000 is", greater_than_100k)

    smallest_dir = calc_smallest_size(total_sizes_dict,
                                      total_space=70000000, needed_space=30000000)
    print("Total size of directory that is the smallest directory needed to be deleted is", smallest_dir)
