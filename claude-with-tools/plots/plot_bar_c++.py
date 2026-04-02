import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_tool_types_from_xlsx(xlsx_path):

    xl = pd.ExcelFile(xlsx_path)

    candidate_sheets = [s for s in xl.sheet_names][:5]

    row0_comp1 = []
    row0_comp2 = []
    row0_comp3 = []
    row1_comp1 = []
    row1_comp2 = []
    row1_comp3 = []

    for i, sh in enumerate(candidate_sheets):
        # Column B, rows 4..5 (inclusive): skip first 3 rows, read 2 rows
        df_scores = pd.read_excel(
            xlsx_path, sheet_name=sh,
            header=None, usecols="B:D", skiprows=3, nrows=2
        )
        row0 = df_scores.iloc[0, :].to_numpy()
        row1 = df_scores.iloc[1, :].to_numpy()
        
        row0_comp1.append(row0[0])
        row0_comp2.append(row0[1])
        row0_comp3.append(row0[2])
        row1_comp1.append(row1[0])
        row1_comp2.append(row1[1])
        row1_comp3.append(row1[2])

    return row0_comp1, row0_comp2, row0_comp3, row1_comp1, row1_comp2, row1_comp3

def bar_plot(lang, lst1, lst2, lst3, lst4, lst5, lst6):
    find = "cornflowerblue"
    grep = "sandybrown"
    read = "salmon"
    color1   = find 
    color2   = grep 
    color3   = read 

    labels = ['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4', 'Sample 5']

    x = np.arange(len(labels)) # the label locations
    width = 0.25 # the width of the bars in a group

    fig, ax = plt.subplots(figsize=(20, 12))

    
    components(lst1, lst2, lst3, lst4, lst5, lst6, ax, width, x, color1, color2, color3)

    # Add labels, title, and legend
    ax.set_xlabel('Samples')
    ax.set_ylabel('# of tools used')
    ax.set_title(f'Types of tools used in {lang}')
    ax.set_xticks(x)
    labels = ['Claude        P               PC', 
              'Claude        P               PC', 
              'Claude        P               PC', 
              'Claude        P               PC',  
              'Claude        P               PC']
    ax.set_xticklabels(labels)
    ax.legend()
    plt.savefig(f"{lang}_bar_plot.png", bbox_inches="tight")  # save
    plt.show()


def components(comp1, comp2, comp3, comp4, comp5, comp6, ax, width, x, color1, color2, color3):
    wo_x = x 

    no_tools_x = x - width
    no_data = [20.37, 72.22, 74.07, 62.5, 66.67]
    ax.plot(wo_x, no_data, color='black', linestyle='solid', marker='o', label='No tools')


    comp1 = np.array(comp1)
    comp2 = np.array(comp2)
    comp3 = np.array(comp3)

    ax.bar(wo_x, comp1, width, label="find", color=color1)
    ax.bar(wo_x, comp2, width, bottom = comp1, label="grep", color=color2)
    ax.bar(wo_x, comp3, width, bottom = comp1 + comp2, label="read", color=color3)

    git = np.array([3, 0, 0, 0, 0])
    ls = np.array([0, 1, 0, 0, 0])
    edit = np.array([0, 0, 0, 0, 1])

    arr = [git, ls, edit]
    labels     = ["git", "ls", "edit"]
    colors     = ["deepskyblue", "yellowgreen", "paleturquoise"]

    bottom = comp1 + comp2 + comp3

    for comp, label, color in zip(arr, labels, colors):
        ax.bar(wo_x, comp, width, bottom=bottom, label=label, color=color)
        bottom += comp  

    wo_data = [25, 52.38, 66.67, 66.67, 38.89]
    ax.plot(wo_x, wo_data, color='black', linestyle='dashed', marker='o', label='Prompt w/o context')


    w_x = x + width
    comp4 = np.array(comp4)
    comp5 = np.array(comp5)
    comp6 = np.array(comp6)

    ax.bar(w_x, comp4, width, color=color1)
    ax.bar(w_x, comp5, width, bottom = comp4, color=color2)
    ax.bar(w_x, comp6, width, bottom = comp4 + comp5, color=color3)

    wx_data = [25, 76.19, 71.43, 66.67, 33.33]
    ax.plot(wo_x, wx_data, color='black', linestyle='dotted', marker='o', label='Prompt w/ context')
    

lst1, lst2, lst3, lst4, lst5, lst6 = get_tool_types_from_xlsx("c++_tool_types.xlsx")
bar_plot("c++", lst1, lst2, lst3, lst4, lst5, lst6)