# descriptives.py

import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure correct working directory
print("Current working directory:", os.getcwd())

# Load cleaned data from relative path
data_path = os.path.join(os.path.dirname(__file__), '../data/cleaned_panel.csv')
df = pd.read_csv(data_path)

# Convert boolean columns to integers (for sector dummies)
bool_cols = df.select_dtypes(include=['bool']).columns
df[bool_cols] = df[bool_cols].astype(int)

# 1. Descriptive statistics
variables = ['RETURN_ON_ASSET', 'ESG_SCORE', 'log_assets', 'RD_transformed', 'has_RD', 'small_firm']
desc = df[variables].describe().T

# 2. Add skewness and kurtosis (exclude binary vars)
skewed_kurt_vars = ['RETURN_ON_ASSET', 'ESG_SCORE', 'log_assets', 'RD_transformed']
desc['skewness'] = df[skewed_kurt_vars].apply(skew)
desc['kurtosis'] = df[skewed_kurt_vars].apply(kurtosis)

# 3. Save summary table
summary_path = os.path.join(os.path.dirname(__file__), '../data/descriptive_statistics.csv')
desc.to_csv(summary_path)

# 4. Plot histograms (exclude binary vars)
plt.figure(figsize=(12, 8))
for i, col in enumerate(skewed_kurt_vars):
    plt.subplot(2, 2, i+1)
    sns.histplot(df[col], kde=True, bins=30)
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plot_path = os.path.join(os.path.dirname(__file__), '../data/variable_distributions.png')
plt.savefig(plot_path)
plt.show()

print("Descriptive statistics saved. Histograms plotted as 'variable_distributions.png'")
