import regex

def read_from_file(file_name):
    f = open(file_name, "r", encoding="utf8")
    return f.read().strip().split("\n")

def generate_regex_score_function(examples_positive, examples_negative):
    def validate_score(string):
        score_positive = 0
        score_negative = 0
        min_score = -(len(examples_negative) + 1)

        string = string.replace("ª", "")

        for example in examples_positive:
            try:
                result = regex.search(string, example)
            except:
                return min_score
            if result and result[0] == example:
                score_positive += 1
        score_positive /= len(examples_positive)

        for example in examples_negative:
            try:
                result = regex.search(string, example)
            except:
                return min_score
            if result and result[0] == example:
                score_negative += 1
        score_negative /= len(examples_negative)

        return score_positive - score_negative

    return validate_score

def generate_target_string_score_function(target):
    def validate_score(string):
        fitness = 0
        for gs, gt in zip(string, target): 
            if gs == gt: 
                fitness += 1
        return fitness 
    return validate_score


