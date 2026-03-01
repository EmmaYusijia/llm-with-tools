import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NUM_SAMPLES = 5

def _read_3_from_colB(xlsx_path, sheet_name):
    df = pd.read_excel(
        xlsx_path, sheet_name=sheet_name,
        header=None, usecols="B", skiprows=3, nrows=3
    )
    return df.iloc[:, 0].astype(float).to_numpy()  # shape (3,)



def get_scores_from_xlsx(xlsx_path):
    """
    Returns:
      scores_lang: np.ndarray shape (3, N_sheets) with values in [0, 100]
    """
    xl = pd.ExcelFile(xlsx_path)

    sheets = [s for s in xl.sheet_names][:NUM_SAMPLES]

    cols = [ _read_3_from_colB(xlsx_path, sh) * 100.0 for sh in sheets ]
    return np.stack(cols, axis=1)   


techniques = ["Claude Opus 4", "w/o code seg", "w/ code seg"]

cols = []
col_labels = []

java_scores = get_scores_from_xlsx("java_performance.xlsx")
python_scores = get_scores_from_xlsx("python_performance.xlsx")
cpp_scores = get_scores_from_xlsx("c++_performance.xlsx")

cols.append(java_scores[:, :NUM_SAMPLES])
col_labels += [f"Java {i+1}" for i in range(NUM_SAMPLES)]
cols.append(python_scores[:, :NUM_SAMPLES])
col_labels += [f"Py {i+1}" for i in range(NUM_SAMPLES)]
cols.append(cpp_scores[:, :NUM_SAMPLES])
col_labels += [f"C++ {i+1}" for i in range(NUM_SAMPLES)]



all_scores = np.column_stack(cols)  # shape (N_techniques, 5)
all_scores = np.asarray(all_scores, dtype=float)

all_scores = all_scores.T
avg_performance = all_scores.mean(axis=0)  # one number per technique


avg_per_question = all_scores.mean(axis=1)  # one number per technique
print(avg_per_question.shape)
print(avg_per_question)

order = np.argsort(-avg_performance)  # minus sign = descending
scores_sorted = all_scores[:, order]
techniques_sorted = [techniques[i] for i in order]

plt.figure(figsize=(12, 8))
img = plt.imshow(scores_sorted.T, aspect='auto', interpolation='nearest', vmin=0, vmax=100, cmap="Blues")

# Axes labels/ticks
#plt.yticks(np.arange(all_scores.shape[1]), col_labels)

plt.xticks(np.arange(len(col_labels)), col_labels, fontsize=16, rotation=45, ha='right')
plt.yticks(np.arange(len(techniques)), techniques_sorted, fontsize=16) #rotation=45,ha='right', rotation_mode='anchor')

#plt.yticks(np.arange(all_scores.shape[1]), col_labels)

plt.xlabel("Question", fontsize=16, labelpad=30)
#plt.ylabel("Model", fontsize=16, labelpad=30)
#plt.ylabel("Approach")
#plt.title("Per-Question Scores by Approach (shade = score %)")
#plt.gca().xaxis.set_label_position('top')
#plt.gca().xaxis.tick_top()

# Colorbar
cbar = plt.colorbar(img)
cbar.set_label("Score (%)", fontsize=16)

'''
# Cell annotations (optional; comment out if too dense)
for i in range(scores_10.shape[0]):
    for j in range(scores_10.shape[1]):
        val = scores_10[i, j]
        plt.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=7)
'''
plt.savefig('heatmap.png', format='png', bbox_inches='tight')


plt.tight_layout()
plt.show()

