import pandas as pd
import matplotlib.pyplot as plt
import utils

def plot_deductions():
    """
    Plots a horizontal stacked bar chart showing points deducted
    for hallucinations vs incompleteness per model/technique.
    """
    deduction_summary = utils.get_all_deducted()

    df = pd.DataFrame.from_dict(deduction_summary, orient='index')

    df = df[["hallucination", "incompleteness"]]

    df['total'] = df["incompleteness"] + df["hallucination"]
    df = df.sort_values(by="total", ascending=False)
    df = df.drop(columns=['total'])
    new_names_mapping = {"w/o code seg w/ tools": "Prompt w/o context",
                            "Claude Opus 4": "No tools",
                            "w/ code seg & tools": "Prompt w/ context"}
    df = df.rename(index=new_names_mapping)

    print(df)

    # Create horizontal stacked bar chart
    ax = df.plot(
        kind="barh",
        stacked=True,
        #color=["#d4a5a5", "#a59fd4"],  # dusty rose and periwinkle
        #color=["#cc9999", "#c0c0c0"],  # soft burgundy and silver
        color=["#d9b3b3", "#c0c0c0"],  # light burgundy and silver
        #color=["#d8b4c4", "#b4a8c8"],  # dusty rose and muted purple
        #color=["#d8c8c4", "#c4b8d8"],  # warm gray and dusty lavender
        #color=["#f4b8c8", "#c8b8f4"],  # soft coral and soft lilac
        #color=["#e8b4d4", "#d4b4e8"],  # light rose and light lavender
        #color=["#b8d4e8", "#e8ba9a"],  # light periwinkle and apricot
        #color=["#9cc5d9", "#d9a87a"],  # cornflower and tan
        #color=["#c5d9e8", "#e8c3a8"],  # pale blue and sand
        #color=["#708090", "#bc8f8f"],  # slate gray and rosy brown
        #color=["#a8c5dd", "#f4b183"],  # light steel blue and peach
        figsize=(14, 10)
    )

    ax.tick_params(axis='y', labelsize=16)
    ax.tick_params(axis='x', labelsize=16)

    plt.xlabel("Average Points Per Error Type")
    #plt.ylabel("Model")
    #plt.title("Average Points by Type of Error")
    plt.legend(title="Error Type", loc="upper right", fontsize=16)
    plt.tight_layout()

    # Add labels for total deductions
    for i, (idx, row) in enumerate(df.iterrows()):
        incomp = row["incompleteness"]
        hall = row["hallucination"]

        # Label for incompleteness (at the center of its segment)
        ax.text(incomp + hall / 2, i, f"{incomp:.1f}", va='center', ha='center', fontsize=16, fontweight='bold')
        
        # Label for hallucination (at the center of its segment)
        ax.text(hall  / 2, i, f"{hall:.1f}", va='center', ha='center', fontsize=16, fontweight='bold')

        total = round(incomp, 1) + round(hall, 1)
        ax.text(total, i, f"{total:.1f}", va='center', fontsize=16, fontweight='bold')

    plt.savefig("deductions.png")
    plt.savefig("deductions.pdf")

plot_deductions()

