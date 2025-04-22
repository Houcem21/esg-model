# summary_dashboard.py

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define paths
base_path = os.path.join(os.path.dirname(__file__), '../data')
image_files = [
    'variable_distributions.png',
    'correlation_heatmap.png',
    'vif_plot.png',
    'regression_coefficients.png'
]

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, filename in enumerate(image_files):
    path = os.path.join(base_path, filename)
    if os.path.exists(path):
        img = mpimg.imread(path)
        axes[i].imshow(img)
        axes[i].axis('off')
        axes[i].set_title(filename.replace('_', ' ').replace('.png', '').title())
    else:
        axes[i].text(0.5, 0.5, f"Missing: {filename}", ha='center', va='center', fontsize=12)
        axes[i].axis('off')

plt.tight_layout()
plt.savefig(os.path.join(base_path, 'final_dashboard.png'))
plt.show()

print("📊 Summary dashboard created as 'final_dashboard.png'")
