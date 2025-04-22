# correlations.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load cleaned data
data_path = os.path.join(os.path.dirname(__file__), '../data/cleaned_panel.csv')
df = pd.read_csv(data_path)

# Select variables for correlation matrix
vars_to_corr = ['RETURN_ON_ASSET', 'ESG_SCORE', 'log_assets', 'RD_transformed']
corr_matrix = df[vars_to_corr].corr(method='pearson')

# Save correlation matrix
corr_path = os.path.join(os.path.dirname(__file__), '../data/correlation_matrix.csv')
corr_matrix.to_csv(corr_path)

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('Correlation Matrix')
plt.tight_layout()
plot_path = os.path.join(os.path.dirname(__file__), '../data/correlation_heatmap.png')
plt.savefig(plot_path)
plt.show()

print("Correlation matrix saved and heatmap plotted as 'correlation_heatmap.png'")