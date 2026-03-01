import matplotlib.pyplot as plt
import numpy as np

# Data
models = ['Claude Opus 4', 'w/o code seg', 'w/ code seg']

java = [1, 1, 0]
python = [1, 3, 4]
cpp = [1, 0, 1]
total = [3, 4, 5]

# Sort by total 
sorted_indices = np.argsort(total)
models_sorted = [models[i] for i in sorted_indices]
java_sorted = [java[i] for i in sorted_indices]
python_sorted = [python[i] for i in sorted_indices]
cpp_sorted = [cpp[i] for i in sorted_indices]
total_sorted = sorted(total)

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

y_pos = np.arange(len(models_sorted))

green = "#93c5ac"
yellow = "#ffbb8f"
blue = "#9dc6e0"
red = "#de425b"

java_color   = green #"#C6DBEF"  # very soft blue
python_color = yellow #"#CCEBC5"  # very soft green
cpp_color    = blue #"#D9D9F3"  # very soft lavender


# Create stacked bars
p1 = ax.barh(y_pos, java_sorted, label='Java', color=java_color)
p2 = ax.barh(y_pos, python_sorted, left=java_sorted, label='Python', color=python_color)
cpp_left = [j + p for j, p in zip(java_sorted, python_sorted)]
p3 = ax.barh(y_pos, cpp_sorted, left=cpp_left, label='C++', color=cpp_color)

# Customize
ax.set_yticks(y_pos)
ax.set_yticklabels(models_sorted, fontsize=16)
ax.set_ylim(-0.5, len(models_sorted) - 0.5)  # Add this line
ax.set_xlabel('Number of Questions Answered Completely Correctly', fontsize=16)
#ax.set_title('Binary Performance by Each Model', fontsize=14, pad=15, fontweight='bold')
ax.legend(loc='lower right', fontsize=11)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_xlim(0, max(total_sorted) + 0.8)

# Add total score at the end of each bar
for i, t in enumerate(total_sorted):
    if t > 0:
        ax.text(t + 0.15, i, str(t), va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('binary.png', format='png', bbox_inches='tight', dpi=300)
plt.show()
