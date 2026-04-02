import seaborn as sns
from matplotlib.colors import to_hex

palette = sns.color_palette()
hex_colors = [to_hex(c) for c in palette]

print(hex_colors)