import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

NUM_SAMPLES = 5

def _read_3_from_colB(xlsx_path, sheet_name):
    df = pd.read_excel(
        xlsx_path, sheet_name=sheet_name,
        header=None, usecols="B", skiprows=3, nrows=3
    )
    return df.iloc[:, 0].astype(float).to_numpy()  # shape (3,)


def get_costs_from_xlsx(xlsx_path):
    """
    Returns:
      scores_lang: np.ndarray shape (3, N_sheets) 
    """
    xl = pd.ExcelFile(xlsx_path)

    sheets = [s for s in xl.sheet_names][:NUM_SAMPLES]

    cols = [ _read_3_from_colB(xlsx_path, sh) for sh in sheets ]
    
    return np.stack(cols, axis=1)


def get_scores_from_xlsx(xlsx_path):
    """
    Returns:
      scores_lang: np.ndarray shape (3, N_sheets) with values in [0, 100]
    """
    xl = pd.ExcelFile(xlsx_path)

    sheets = [s for s in xl.sheet_names][:NUM_SAMPLES]

    cols = [ _read_3_from_colB(xlsx_path, sh) * 100.0 for sh in sheets ]
    return np.stack(cols, axis=1)   



java_scores = get_scores_from_xlsx("java.xlsx")
mean_java_scores = java_scores.mean(axis=1)

python_scores = get_scores_from_xlsx("python.xlsx")
mean_python_scores = python_scores.mean(axis=1)

cpp_scores = get_scores_from_xlsx("cpp.xlsx")
mean_cpp_scores = cpp_scores.mean(axis=1)

java_costs = get_costs_from_xlsx("java_cost.xlsx")
python_costs = get_costs_from_xlsx("python_cost.xlsx")
cpp_costs = get_costs_from_xlsx("cpp_cost.xlsx")

mean_scores = np.vstack([mean_java_scores, mean_python_scores, mean_cpp_scores]).mean(axis=0)

total_costs = java_costs.sum(axis=1) + python_costs.sum(axis=1)  + cpp_costs.sum(axis=1)# shape (20,)

print("Java costs", java_costs[5])
print("cpp cost", cpp_costs[5])
print("java cost", java_costs[5])
print(total_costs[5])

#mean_costs = np.vstack([mean_java_costs, mean_python_costs]).mean(axis=0)

#std_A  = java_scores.std(axis=1)
#mean = python_scores.mean(axis=1)
#std  = python_scores.std(axis=1)

#scores = np.hstack([java_scores, python_scores])
scores = mean_scores
costs = total_costs #mean_costs

techniques = ["Claude Opus 4", "Claude Opus 4.1", "Claude Sonnet 3.7", "Claude Sonnet 4", "Deepseek-r1-70B",  "Gemini 2.0 Flash", "Gemini 2.5 Flash", "Gemini 2.5 Pro", "Gpt-4.1", "Gpt-5", "Gpt-oss-120B", "Gpt-oss-20B", "o3", "Grok 3", "Grok 4",  "Llama3.3-70", "Llama 4 Scout", "Mistral Large", "Qwen3", "Qwen3 Coder"]

# Assume first 5 samples = Lang A, next 5 = Lang B
idx = np.arange(0, 5)

x = np.arange(len(techniques))
positions = x * 2.0 - 0.25

# Plot
#width = 0.38
#plt.figure(figsize=(8, 6))


family_colors = {
    "OpenAI":   "royalblue",
    "Anthropic": "seagreen",
    "Google":   "darkorange",
    "xAI":     "purple",
    "Other":    "pink"
}

def get_family(name: str) -> str:
    name = name.lower()
    if "gpt" in name or name == "o3": return "OpenAI"
    if "claude" in name: return "Anthropic"
    if "gemini" in name: return "Google"
    if "grok" in name: return "xAI"
    return "Other"

label_positions = {
    'o3': (5, 8, 'left', 'bottom'),
    'Gpt-5': (-5, -10, 'right', 'top'),
    'Claude Opus 4.1': (-35, 10, 'left', 'bottom'),
    'Claude Opus 4': (-15, -10, 'left', 'top'),
    'Claude Sonnet 4': (5, 8, 'left', 'bottom'),
    'Claude Sonnet 3.7': (5, -10, 'left', 'top'),
    'Gemini 2.5 Pro': (-10, -20, 'left', 'bottom'),
    'Gemini 2.0 Flash': (50, 10, 'right', 'bottom'),
    'Gemini 2.5 Flash': (50, 10, 'right', 'bottom'),
    'Gpt-4.1': (5, -10, 'left', 'top'),
    'Grok 4': (-5, -20, 'left', 'bottom'),
    'Grok 3': (8, 5, 'left', 'bottom'),
}

plt.figure(figsize=(12, 8))  # Larger figure for 20 points

texts = []
for i, label in enumerate(techniques):
    fam = get_family(label)

    plt.scatter(costs[i], scores[i], color=family_colors[fam], marker='o', s=150,  edgecolor="k", linewidth=1.5, alpha=0.8)

    plt.scatter(costs[i], scores[i], color=family_colors[fam], marker='o', s=150, 
        edgecolor="k", linewidth=1.5, alpha=0.8, zorder=3)
    #plt.scatter(costs[i], scores[i], xytext=(3, 7), textcoords="offset points",  fontsize=9, ha='left', va='bottom') #, arrowprops=dict(arrowstyle='-', lw=0.3, alpha=0.5))  # add labels near points
    #txt = plt.text(costs[i], scores[i], label, fontsize=8, ha='left', va='bottom')
    #texts.append(txt)

#adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5, alpha=0.6))

#xytext=(5, 7), 
#textcoords="offset points",  fontsize=8, ha='left', va='bottom', alpha=0.9) #, arrowprops=dict(arrowstyle='-', lw=0.3, alpha=0.5))  # add labels near points

#plt.xscale("log")

for i, label in enumerate(techniques):
    # Get custom position or use default
    if label in label_positions:
        x_off, y_off, ha, va = label_positions[label]
    else:
        x_off, y_off, ha, va = (5, 7, 'left', 'bottom')
    
    plt.annotate(label, (costs[i], scores[i]), 
                xytext=(x_off, y_off), 
                textcoords="offset points",  
                fontsize=9, 
                ha=ha, 
                va=va,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.7))


plt.xlabel("Cost ($ in USD)")
plt.ylabel("Score (%)")
plt.title("Cost vs Score")

#plt.legend(["Java", "Python"], loc="upper right")
plt.grid(True, linestyle="--", alpha=0.6)

'''
sorted_idx = np.argsort(costs)
pareto_costs, pareto_scores, best_score = [], [], -1
for i in sorted_idx:
    if scores[i] > best_score:
        pareto_costs.append(costs[i])
        pareto_scores.append(scores[i])
        best_score = scores[i]
plt.plot(pareto_costs, pareto_scores, linestyle="--", color="red", alpha=0.7)
'''

# Plot diagonal
#plt.plot([low, high], [low, high], linestyle="--", color="black", alpha=0.7, label="x = y")
#plt.plot([0,0.5], [40,80], linestyle="--", color="black", alpha=0.3)


handles = []
labels = []
for fam, color in family_colors.items():
    if fam == "Other": continue
    handles.append(plt.Line2D([], [], marker="o", color=color, linestyle="",
                              markeredgecolor="k", markersize=8))
    labels.append(fam)

plt.legend(handles, labels, title="Model Family")


plt.tight_layout()
plt.axis("tight")
plt.margins(0)
plt.xlim(-0.05, 0.65)
plt.ylim(40, 80)

#plt.savefig("finding4.png", dpi=300, bbox_inches="tight", pad_inches=0.2)
plt.savefig("finding4.pdf", format="pdf", bbox_inches="tight")  # save as PNG


plt.show()

