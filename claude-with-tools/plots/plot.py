import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_scores_from_xlsx(xlsx_path):
    """
    Returns:
      scores_lang: np.ndarray shape (3, N_sheets) with values in [0, 100]
    """
    xl = pd.ExcelFile(xlsx_path)

    candidate_sheets = [s for s in xl.sheet_names][:5]

    cols = []

    for i, sh in enumerate(candidate_sheets):
        # Column B, rows 4..6 (inclusive): skip first 3 rows, read 3 rows
        df_scores = pd.read_excel(
            xlsx_path, sheet_name=sh,
            header=None, usecols="B", skiprows=3, nrows=3
        )
        col = df_scores.iloc[:, 0].astype(float).to_numpy()
        col = col * 100.0

        cols.append(col)

    scores_lang = np.column_stack(cols)  # shape (3, N_sheets)
    return scores_lang



java_scores = get_scores_from_xlsx("java_performance.xlsx")
# print(java_scores)
python_scores = get_scores_from_xlsx("python_performance.xlsx")
# print(python_scores)
cpp_scores = get_scores_from_xlsx("c++_performance.xlsx")
# print(cpp_scores)

# for each lang, 3 model types
mean_java = java_scores.mean(axis=1)
#std_A  = java_scores.std(axis=1)
mean_py = python_scores.mean(axis=1)
#std  = python_scores.std(axis=1)
mean_cpp = cpp_scores.mean(axis=1)

# per model type
mean_all = np.vstack([mean_java, mean_py, mean_cpp]).mean(axis=0)

print(mean_java)
print(mean_py)
print(mean_cpp)

# per lang
overall_java = mean_java.mean()
overall_py   = mean_py.mean()
overall_cpp  = mean_cpp.mean()
overall_all  = mean_all.mean()

#scores = np.hstack([java_scores, python_scores])

techniques = ['Claude', 'P', 'PC']

# Assume first 5 samples = Lang A, next 5 = Lang B
idx = np.arange(0, 5)
#idx_B = np.arange(5, 10)

# Prepare data per technique, per language
#data_A = [scores[i, idx_A] for i in range(scores.shape[0])]
#data_B = [scores[i, idx_B] for i in range(scores.shape[0])]

# sort indices by descending avg
sorted_idx = np.argsort(-mean_all)

# reorder everything
# techniques_sorted = techniques
# mean_java_sorted   = mean_java[sorted_idx]
# mean_py_sorted     = mean_py[sorted_idx]
# mean_cpp_sorted    = mean_cpp[sorted_idx]
# mean_all_sorted    = mean_all[sorted_idx]


# print(mean_java_sorted)
# print(mean_py_sorted)
# print(mean_cpp_sorted)
# print(mean_all_sorted)

x = np.arange(len(techniques))

# X-axis positions (shifted for side-by-side plotting)
#x = np.arange(len(techniques))
#positions = x * 2.0 - 0.25
#positions_B = x * 2.0 + 0.25

# Plot
width = 0.2
plt.figure(figsize=(14, 6))
#bp_A = plt.boxplot(data_A, positions=positions_A, widths=0.4,
#                   patch_artist=False, manage_ticks=False)
#bp_B = plt.boxplot(data_B, positions=positions_B, widths=0.4,
#                   patch_artist=False, manage_ticks=False)

# muted palette for per-language
# distinct muted colors
#green = "#6d9d86"
green = "#93c5ac"
yellow = "#ffbb8f"
blue = "#9dc6e0"
red = "#de425b"

java_color   = green #"#C6DBEF"  # very soft blue
python_color = yellow #"#CCEBC5"  # very soft green
cpp_color    = blue #"#D9D9F3"  # very soft lavender
avg_color    = red #"#E41A1C"  # bold red

bar_colors = [java_color, python_color, cpp_color, avg_color]

plt.bar(x - 1.5*width, mean_java, width, color=bar_colors[0], label="java", alpha=0.5)
plt.bar(x - 0.5*width, mean_py,   width, color=bar_colors[1], label="python", alpha=0.5)
plt.bar(x + 0.5*width, mean_cpp,  width, color=bar_colors[2], label="c++", alpha=0.5)
plt.bar(x + 1.5*width, mean_all,  width, color=bar_colors[3], label="avg all")
print(mean_all)

plt.axhline(overall_java, color=bar_colors[0], linestyle="--", alpha=0.9)
plt.axhline(overall_py,   color=bar_colors[1], linestyle="--", alpha=0.9)
plt.axhline(overall_cpp,  color=bar_colors[2], linestyle="--", alpha=0.9)
plt.axhline(overall_all,  color=bar_colors[3], linestyle="-.", alpha=0.9)

'''
plt.bar(x - 1.5*width, mean_java, width, capsize=4, label="java")
plt.bar(x - 0.5*width, mean_py, width, capsize=4, label="python")
plt.bar(x + 0.5*width, mean_cpp, width, capsize=4, label="c++")
plt.bar(x + 1.5*width, mean_cpp, width, capsize=4, label="average")

plt.axhline(overall_java, color="C0", linestyle="--", linewidth=1, label="avg java")
plt.axhline(overall_py,   color="C1", linestyle="--", linewidth=1, label="avg python")
plt.axhline(overall_cpp,  color="C2", linestyle="--", linewidth=1, label="avg c++")
plt.axhline(overall_all,  color="C3", linestyle="-.", linewidth=1, label="avg all")
'''


# Style and labels
plt.xticks(x, techniques, rotation=45, ha='right', fontsize=14)
plt.ylim(0, 100)
plt.ylabel("Score (%)", fontsize=14)
#plt.xlabel("Model")
plt.title("Score per Model", fontsize=14)

# Legend using median line handles
#median_A = bp_A["medians"][0]
#median_B = bp_B["medians"][0]
plt.legend(["Java", "Python", "C++", "Average"], loc="upper right", fontsize=14)


plt.tight_layout()

#plt.savefig("finding1.pdf", format='pdf', bbox_inches="tight")  # save 

plt.savefig("finding1.png", bbox_inches="tight")  # save 
plt.show()



