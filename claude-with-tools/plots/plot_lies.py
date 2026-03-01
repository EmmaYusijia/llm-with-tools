import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import utils

models = ['Claude Opus 4', 'w/o code seg', 'w/ code seg']

lies = utils.get_total_lies()


values = list(lies.values())
totals = [sum(v) for v in values]
averages = [sum(v)/len(v) for v in values]


print(lies.keys())
print(totals)
print(averages)
#averages = [0.8, 0.7, 0.7, 0.7, 0.7, 0.7, 0.6, 0.6, 0.6, 0.6, 
#            0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4, 0.3, 0.2, 0.2]

# Sort ascending
sorted_indices = np.argsort(averages)
models_sorted = [models[i] for i in sorted_indices]
averages_sorted = [averages[i] for i in sorted_indices]

# Color code by severity (green = good/low lies, red = bad/high lies)
colors = ['#27ae60' if v <= 0.3 else '#f39c12' if v <= 0.5 else '#e74c3c' 
          for v in averages_sorted]
#colors = ['#27ae60' if v <= 0.3 else '#1e8449' if v <= 0.5 else '#145a32' 
#          for v in averages_sorted]



fig, ax = plt.subplots(figsize=(8, 8))
y_pos = np.arange(len(models_sorted))

# Draw lollipop stems
ax.hlines(y=y_pos, xmin=0, xmax=averages_sorted, color='gray', alpha=0.4, linewidth=2)

# Draw lollipop heads
ax.scatter(averages_sorted, y_pos, color=colors, s=150, zorder=3, edgecolors='white', linewidth=1.5)

# Customize
ax.set_yticks(y_pos)
ax.set_yticklabels(models_sorted, fontsize=16)
ax.set_ylim(-0.5, len(models_sorted) - 0.5)
ax.set_xlabel('Average Number of Lies per Question', fontsize=12)
ax.set_xlim(0, 1.0)
ax.grid(axis='x', alpha=0.3, linestyle='--')
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
#ax.spines['left'].set_visible(False)

# Add values next to dots
for i, v in enumerate(averages_sorted):
    ax.text(v + 0.03, i, f'{v:.1f}', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('lies_lollipop.png', format='png', bbox_inches='tight', dpi=300)
plt.savefig('lies_lollipop.pdf', format='pdf', bbox_inches='tight')
#plt.show()
