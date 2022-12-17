def run_score_pipeline(list_data, strategy):
    score_map = score_mapping(strategy)
    score_list = calc_score_list(list_data, score_map)
    total_score = sum(score_list)

    return total_score


def score_mapping(strategy):
    if strategy == "original":
        dict_map = {
            "A X": 4,  # rock + draw
            "A Y": 8,  # paper + win
            "A Z": 3,  # scissors + loss
            "B X": 1,  # rock + loss
            "B Y": 5,  # paper + draw
            "B Z": 9,  # scissors + win
            "C X": 7,  # rock + win
            "C Y": 2,  # paper + loss
            "C Z": 6,  # scissors + draw
        }
    elif strategy == "intended":
        dict_map = {
            "A X": 3,  # lose with scissors
            "A Y": 4,  # draw with rock
            "A Z": 8,  # win with paper
            "B X": 1,  # lose with rock
            "B Y": 5,  # draw with paper
            "B Z": 9,  # win with scissors
            "C X": 2,  # lose with  paper
            "C Y": 6,  # draw with scissors
            "C Z": 7,  # win with rock
        }
    else:
        raise ValueError('Supplied strategy is not properly defined')

    return dict_map


def calc_score_list(data_list, mapping):
    sum_list = [mapping[strat] for strat in data_list]

    return sum_list


if __name__ == "__main__":
    with open("./code/day_2/day_2_input.txt") as f:
        raw_data = [line.rstrip() for line in f]

    original_score = run_score_pipeline(raw_data, strategy="original")
    print("Expected score with original strategy is", original_score)

    new_score = run_score_pipeline(raw_data, strategy="intended")
    print("Expected score with new strategy is", new_score)
