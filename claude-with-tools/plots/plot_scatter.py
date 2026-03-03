import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_scores_from_xlsx(xlsx_path):

    xl = pd.ExcelFile(xlsx_path)

    candidate_sheets = [s for s in xl.sheet_names][:5]

    cols = []   

    for i, sh in enumerate(candidate_sheets):
        # Column B, rows 5..6 (inclusive): skip first 4 rows, read 2 rows
        df_scores = pd.read_excel(
            xlsx_path, sheet_name=sh,
            header=None, usecols="B", skiprows=4, nrows=2
        )
        col = df_scores.iloc[:, 0].astype(float).to_numpy()
        col = col * 100.0

        cols.append(col)

    scores_lang = np.column_stack(cols)  # shape (2, N_sheets)
    
    return scores_lang

def get_tools_from_xlsx(xlsx_path):

    xl = pd.ExcelFile(xlsx_path)

    candidate_sheets = [s for s in xl.sheet_names][:5]

    cols = [] 

    for i, sh in enumerate(candidate_sheets):
        # Column B, rows 4..5 (inclusive): skip first 3 rows, read 2 rows
        df_scores = pd.read_excel(
            xlsx_path, sheet_name=sh,
            header=None, usecols="B", skiprows=3, nrows=2
        )
        col = df_scores.iloc[:, 0].astype(float).to_numpy()
        
        cols.append(col)

    tools_lang = np.column_stack(cols)  # shape (2, N_sheets)
    
    return tools_lang


x1 = []
x2 = []
y1 = []
y2 = []
lang_list = ["java", "python", "c++"]

for lang in lang_list:
    scores = get_scores_from_xlsx(f"{lang}_performance.xlsx")
    tools = get_tools_from_xlsx(f"{lang}_tools.xlsx")
    x1.append(tools[0,:])
    x2.append(tools[1,:])
    y1.append(scores[0,:]) 
    y2.append(scores[1,:])


# Style and labels
plt.scatter(x1, y1, color='orange', label='Prompt w/o context')
plt.scatter(x2, y2, color='blue', label='Prompt w/ context')
plt.xlim(-0.1, 10)
plt.ylim(0, 102)
plt.ylabel("Score (%)", fontsize=14)
plt.xlabel("# of tool calls")
plt.title("performance vs. # of tools called", fontsize=14)

# Legend using median line handles
#median_A = bp_A["medians"][0]
#median_B = bp_B["medians"][0]
plt.legend(loc="lower right", fontsize=14)


plt.tight_layout()

#plt.savefig("finding1.pdf", format='pdf', bbox_inches="tight")  # save 

plt.savefig("scatter_plot.png", bbox_inches="tight")  # save 
plt.show()