import csv
import json
import os
from collections import defaultdict


def calculate_score(rubric, r_deducted):
    totals = []
    points = []
    for rubric_item in rubric:
        totals += [rubric_item["points"]]
        points += [rubric_item["points"]]

    if r_deducted:
        for rubric_item_deducted in r_deducted.split(","):
            #print(rubric_item_deducted)
            r_number = int(rubric_item_deducted[0])-1 #index from 0

            points[r_number] -= get_points_from_ritem(rubric, rubric_item_deducted)

    score = 0
    for total, point in zip(totals, points):
        score += float(point) / float(total)

    return score / len(totals)

def get_points_from_ritem(rubric, r_item):
    assert len(r_item) == 2

    r_number = int(r_item[0])-1 #index from 0
    sub_item = ord(r_item[1])-ord('a')

    return rubric[r_number]["subitems"][sub_item]["points"]

def get_average_score_by_language():
    PREFIX = "../artifact/"
    average_lang_scores = {"java": 0, "py": 0, "cpp": 0}
    col_labels = []
    for LANG in ["java", "py", "cpp"]:
        all_q_scores = defaultdict(list)

        for SAMPLE_NUM in range(1,6):
            col_labels += [LANG.capitalize() + " " + str(SAMPLE_NUM)]
            f_csv = f"{LANG}{SAMPLE_NUM}.csv"
            f_results = PREFIX + f"results/rubric-applications/{f_csv}"
            f_rubrics = PREFIX + f"dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"

            if not os.path.exists(f_results):
                continue

            rubric = json.load(open(f_rubrics))

            all_scores = defaultdict(list)

            with open(f_results) as f:
                reader = csv.reader(f)

                next(reader)

                for row in reader:
                    model = row[0]
                    trial_num = row[1]
                    r_deducted = row[2]

                    all_scores[model].append(calculate_score(rubric, r_deducted))

            for k, v in all_scores.items():
                average = sum(v) / len(v)
                all_q_scores[k].append(average)
        
        for _, v in all_q_scores.items():
            average_lang_scores[LANG] += sum(v)

    #print("Average lang scores", average_lang_scores)
    #for k, v in average_lang_scores.items():
    #    average_lang_scores[k] /= 20 

    average_lang_scores["total"] = (average_lang_scores["java"] + average_lang_scores["cpp"]  + average_lang_scores["py"]) / 3
    return average_lang_scores


def default_bin_dict():
    return {"java": 0, "py": 0, "cpp": 0, "total": 0}

def get_binary_scores(all_trials):
    PREFIX = "../artifact/"
    col_labels = []
    binary_scores = defaultdict(default_bin_dict)
    for LANG in ["java", "py", "cpp"]:

        for SAMPLE_NUM in range(1,6):
            col_labels += [LANG.capitalize() + " " + str(SAMPLE_NUM)]
            f_csv = f"{LANG}{SAMPLE_NUM}.csv"
            f_results = PREFIX + f"results/rubric-applications/{f_csv}"
            f_rubrics = PREFIX + f"dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"

            if not os.path.exists(f_results):
                continue

            rubric = json.load(open(f_rubrics))

            all_scores = defaultdict(list)

            with open(f_results) as f:
                reader = csv.reader(f)

                next(reader)

                for row in reader:
                    model = row[0]
                    trial_num = row[1]
                    r_deducted = row[2]

                    all_scores[model].append(calculate_score(rubric, r_deducted))

            for k, v in all_scores.items():
                if not all_trials:
                    if any(x == 1.0 for x in v):
                        binary_scores[k]["total"] += 1
                        binary_scores[k][LANG] += 1
                    else:
                        binary_scores[k]["total"] += 0
                        binary_scores[k][LANG] += 0

                else:
                    average = sum(v) / len(v)
                    if average == 1.0:
                        binary_scores[k]["total"] += 1
                        binary_scores[k][LANG] += 1
                    else:
                        binary_scores[k]["total"] += 0
                        binary_scores[k][LANG] += 0


    return binary_scores



def get_all_scores():
    PREFIX = "../artifact/"
    all_lang_scores = defaultdict(list)
    col_labels = []
    for LANG in ["java", "py", "cpp"]:
        all_q_scores = defaultdict(list)

        for SAMPLE_NUM in range(1,6):
            col_labels += [LANG.capitalize() + " " + str(SAMPLE_NUM)]
            f_csv = f"{LANG}{SAMPLE_NUM}.csv"
            f_results = PREFIX + f"results/rubric-applications/{f_csv}"
            f_rubrics = PREFIX + f"dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"

            if not os.path.exists(f_results):
                continue

            rubric = json.load(open(f_rubrics))

            all_scores = defaultdict(list)

            with open(f_results) as f:
                reader = csv.reader(f)

                next(reader)

                for row in reader:
                    model = row[0]
                    trial_num = row[1]
                    r_deducted = row[2]

                    all_scores[model].append(calculate_score(rubric, r_deducted))

            for k, v in all_scores.items():
                average = sum(v) / len(v)
                all_q_scores[k].append(average)
                all_lang_scores[k].append(average*100)

    return all_lang_scores


def calculate_deductions_by_type(rubric, r_deducted):
    """
    Given a rubric and a string of deducted rubric items (e.g., "1a,2b"),
    returns the total points deducted for:
      - incompleteness ("lie": False)
      - hallucination ("lie": True)
    """
    hallucination_points = 0
    incompleteness_points = 0

    if not r_deducted:
        return {"hallucination": 0.0, "incompleteness": 0.0}

    for r_item in r_deducted.split(","):
        if not r_item.strip():
            continue

        r_number = int(r_item[0]) - 1  # rubric index
        sub_item = ord(r_item[1]) - ord('a')  # subitem index

        sub = rubric[r_number]["subitems"][sub_item]
        pts = sub["points"]

        # total points possible for this rubric section
        total = rubric[r_number]["points"]

        # convert to proportional deduction if needed
        deduction_value = float(pts) / float(total)

        if sub.get("lie", False):
            hallucination_points += deduction_value
        else:
            incompleteness_points += deduction_value

    return {
        "hallucination": hallucination_points,
        "incompleteness": incompleteness_points
    }

def get_all_deducted():
    PREFIX = "../artifact/"
    deduction_summary = defaultdict(lambda: {"hallucination": 0, "incompleteness": 0})
    all_deductions = defaultdict(list)
    col_labels = []

    for LANG in ["java", "python", "cpp"]:

        for SAMPLE_NUM in range(1, 6):
            col_labels += [f"{LANG.capitalize()} {SAMPLE_NUM}"]
            f_csv = f"{LANG}{SAMPLE_NUM}.csv"
            f_results = PREFIX + f"results/rubric-applications/{f_csv}"
            f_rubrics = PREFIX + f"dataset/{LANG}/rubrics/{SAMPLE_NUM}.json"

            if not os.path.exists(f_results):
                continue

            rubric = json.load(open(f_rubrics))

            with open(f_results) as f:
                reader = csv.reader(f)
                next(reader)

                for row in reader:
                    model = row[0]
                    trial_num = row[1]
                    r_deducted = row[2]

                    # accumulate deduction breakdown
                    d = calculate_deductions_by_type(rubric, r_deducted)
                    all_deductions[model].append(d)


    deduction_avg = {}
    for model, deductions in all_deductions.items():
        if not deductions:
            continue

        hallucination_avg = sum(d["hallucination"] for d in deductions) / len(deductions)
        incompleteness_avg = sum(d["incompleteness"] for d in deductions) / len(deductions)

        deduction_avg[model] = {
            "hallucination": hallucination_avg,
            "incompleteness": incompleteness_avg,
        }

    #print(deduction_avg)
    return deduction_avg

