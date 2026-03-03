import json
import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
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

'''
def get_scores_from_csv(csv_path):
    """
    Reads scores from CSV and averages across the 3 trials for each question.
    Returns:
      scores: np.ndarray shape (n_models, 15) with values in [0, 100]
      model_names: list of model names
    """
    df = pd.read_csv(csv_path)
    # Extract model names
    model_names = df['model name'].tolist()
    # Get all score columns (excluding 'model name')
    score_cols = [col for col in df.columns if col != 'model name']
    # Convert percentages to floats (remove % and divide by 100, then multiply by 100 to get 0-100 scale)
    for col in score_cols:
        df[col] = df[col].str.rstrip('%').astype(float)
    # Group columns by question (Java 1.1, Java 1.2, Java 1.3 -> Java 1)
    question_groups = {}
    for col in score_cols:
        # Extract base question name (e.g., "Java 1" from "Java 1.1")
        parts = col.rsplit('.', 1)
        base_name = parts[0]
        if base_name not in question_groups:
            question_groups[base_name] = []
        question_groups[base_name].append(col)
    # Calculate average for each question across its 3 trials
    averaged_scores = []
    question_names = []
    # Custom sorting function
    def sort_key(question):
        parts = question.split()
        lang = parts[0]  # C++, Java, Py
        num = parts[1].split(".")[0]   # Could be "1", "2", etc.
        # Language priority
        lang_order = {"Java": 0, "Py": 1, "C++": 2}
        return (lang_order.get(lang, 999), int(num))
    for question in sorted(question_groups.keys(), key=sort_key):
        trial_cols = question_groups[question]
        avg_scores = df[trial_cols].mean(axis=1).values
        averaged_scores.append(avg_scores)
        question_names.append(question)
    # Stack into array: shape (n_questions, n_models)
    scores = np.stack(averaged_scores, axis=0)
    # Transpose to (n_models, n_questions)
    scores = scores.T
    return scores, model_names, question_names
'''


PREFIX = "rubrics/"
all_lang_scores = defaultdict(list)
col_labels = []
for LANG in ["java", "py", "c++"]:
    all_q_scores = defaultdict(list)

    for SAMPLE_NUM in range(1,6):
        col_labels += [LANG.capitalize() + " " + str(SAMPLE_NUM)]
        f_csv = f"{LANG}{SAMPLE_NUM}.csv"
        f_results = f_csv
        f_rubrics = PREFIX + f"{LANG}/{SAMPLE_NUM}.json"

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


# Question categories
question_categories = {
    "Java 1": "Project Behavior", "Java 2": "Library Behavior", "Java 3": "Value",
    "Java 4": "Value", "Java 5": "Project Behavior",
    "Py 1": "Library Behavior", "Py 2": "Project Behavior", "Py 3": "Library Behavior",
    "Py 4": "Library Behavior", "Py 5": "Value",
    "Cpp 1": "Performance", "Cpp 2": "Value", "Cpp 3": "Library Behavior",
    "Cpp 4": "Performance", "Cpp 5": "Project Behavior"
}

# Read data from CSV
#print(all_q_scores)
#print(all_lang_scores.values())

all_scores = np.array(list(all_lang_scores.values()))
techniques = ['No tools', 'Prompt w/o context', 'Prompt w/ context']
#col_labels = get_scores_from_csv("raw_data.csv")
print(f"Loaded {len(techniques)} models and {len(col_labels)} questions")
print(f"Questions: {col_labels}")

#print(all_scores.shape)
#print(col_labels)


# Get unique categories
categories = sorted(list(set(question_categories.values())))

# Print header
header = f"{'Model':<30}"
for cat in categories:
    header += f"{cat:<25}"
header += f"{'Overall':<10}"
print(header)
print("-" * 130)

# Print each model's performance
for i, model in enumerate(techniques):
    row = f"{model:<30}"
    
    # Calculate score for each category
    for category in categories:
        category_indices = [j for j, label in enumerate(col_labels)
                          if question_categories.get(label) == category]
        if category_indices:
            # print(all_scores.shape, category_indices)
            category_score = all_scores[i, category_indices].mean()
            row += f"{category_score:>6.2f}%               "
        else:
            row += f"{'N/A':<25}"
    
    # Overall average
    overall = all_scores[i, :].mean()
    row += f"{overall:>6.2f}%"
    print(row)

print("=" * 100)

# Calculate average performance per category
category_avg_scores = {}
for category in set(question_categories.values()):
    category_indices = [i for i, label in enumerate(col_labels)
                       if question_categories.get(label) == category]
    category_scores = all_scores[:, category_indices]
    category_avg_scores[category] = category_scores.mean()

# Sort categories by average performance (best to worst)
category_order = sorted(category_avg_scores.keys(),
                       key=lambda x: category_avg_scores[x],
                       reverse=True)

print("\nCategory Average Scores:")
for cat in category_order:
    print(f"{cat}: {category_avg_scores[cat]:.2f}%")

# Group questions by category (in sorted order)
grouped_indices = []
grouped_labels = []
for category in category_order:
    # Find all questions in this category
    category_questions = [(i, label) for i, label in enumerate(col_labels)
                         if question_categories.get(label) == category]
    # Calculate average score for each question in this category
    question_avg_scores = []
    for i, label in category_questions:
        question_avg_scores.append((i, label, all_scores[:, i].mean()))
    # Sort questions within category by average score (best to worst)
    question_avg_scores.sort(key=lambda x: x[2], reverse=True)
    # Add to grouped lists
    for i, label, avg_score in question_avg_scores:
        grouped_indices.append(i)
        grouped_labels.append(label)

# Reorder scores by category
all_scores_grouped = all_scores[:, grouped_indices]

# Calculate average performance per technique
avg_performance = all_scores_grouped.mean(axis=1)

# Sort by average performance
order = np.argsort(-avg_performance)
scores_sorted = all_scores_grouped[order, :]
techniques_sorted = [techniques[i] for i in order]

# Find category boundaries and positions
category_spans = []
current_category = None
start_idx = 0
for i, label in enumerate(grouped_labels):
    cat = question_categories[label]
    if cat != current_category:
        if current_category is not None:
            category_spans.append((current_category, start_idx, i - 1))
        current_category = cat
        start_idx = i
# Add the last category
category_spans.append((current_category, start_idx, len(grouped_labels) - 1))

# Create heatmap with more space at bottom
fig, ax = plt.subplots(figsize=(15, 12))

img = ax.imshow(scores_sorted, aspect='auto', interpolation='nearest',
                 vmin=0, vmax=100, cmap="Blues")

# Add separator lines between categories
for i, label in enumerate(grouped_labels[1:], 1):
    if question_categories[label] != question_categories[grouped_labels[i-1]]:
        ax.axvline(x=i - 0.5, color='red', linewidth=4, linestyle='--')

# Main x-axis: question labels
ax.set_xticks(np.arange(len(grouped_labels)))
ax.set_xticklabels(grouped_labels, fontsize=14, rotation=45, ha='right')
ax.set_yticks(np.arange(len(techniques_sorted)))
ax.set_yticklabels(techniques_sorted, fontsize=18)

# Create second x-axis for category labels
ax2 = ax.secondary_xaxis('bottom')
ax2.spines['bottom'].set_position(('outward', 60))
ax2.set_xticks([(start + end) / 2 for _, start, end in category_spans])
ax2.set_xticklabels([f"{cat}\n(Avg: {category_avg_scores[cat]:.1f}%)" 
                      for cat, _, _ in category_spans], 
                     fontsize=18, fontweight='bold')
ax2.tick_params(length=0)  # Remove tick marks
ax2.spines['bottom'].set_visible(False)

# Colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.3)
cbar = plt.colorbar(img, cax=cax)
cbar.set_label("Score (%)", fontsize=16)

plt.tight_layout()
plt.savefig('heatmap_cat.png', format='png', dpi=300, bbox_inches='tight')
plt.savefig('heatmap_cat.pdf', format='pdf', bbox_inches='tight')
plt.show()

# Print average performance
print("\nAverage Performance by Model:")
for tech, score in zip(techniques_sorted, avg_performance[order]):
    print(f"{tech}: {score:.2f}%")
