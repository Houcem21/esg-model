# diagnostics.py

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from linearmodels.panel import PanelOLS, PooledOLS, RandomEffects, compare
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
data_path = os.path.join(os.path.dirname(__file__), '../data/cleaned_panel.csv')
df = pd.read_csv(data_path)

# Filter any outliers in RD if present (e.g., cap extreme values)
df['RD_transformed'] = df['RD_transformed'].clip(upper=df['RD_transformed'].quantile(0.99))

# Ensure proper panel indexing
df = df.set_index(['company', 'year'])

# Select variables for diagnostics
features = ['ESG_SCORE', 'log_assets', 'RD_transformed']
X = df[features]
X = sm.add_constant(X)

# ====== VIF ======
vif_data = pd.DataFrame()
vif_data['feature'] = X.columns
vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

# Plot VIF
plt.figure(figsize=(8, 5))
sns.barplot(x='VIF', y='feature', data=vif_data, palette='viridis')
plt.title('Variance Inflation Factor (VIF)')
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), '../data/vif_plot.png'))
plt.show()

# ====== Breusch-Pagan Test for Heteroscedasticity ======
model_bp = sm.OLS(df['RETURN_ON_ASSET'], X).fit()
bp_test = het_breuschpagan(model_bp.resid, model_bp.model.exog)
labels = ['LM stat', 'LM p-val', 'F stat', 'F p-val']
bp_results = dict(zip(labels, bp_test))

# Display BP visually
plt.figure(figsize=(6, 4))
bp_vals = pd.Series(bp_results)
bp_vals.drop(labels='F p-val').plot(kind='barh', color='steelblue')
plt.title(f"Breusch-Pagan Test (F p-val: {bp_results['F p-val']:.4f})")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), '../data/bp_test_plot.png'))
plt.show()

# ====== Wooldridge-style Autocorrelation Check ======
df['ROA_diff'] = df.groupby(level=0)['RETURN_ON_ASSET'].diff()
df['ESG_diff'] = df.groupby(level=0)['ESG_SCORE'].diff()
df['log_assets_diff'] = df.groupby(level=0)['log_assets'].diff()
df['RD_diff'] = df.groupby(level=0)['RD_transformed'].diff()

df_dropna = df.dropna(subset=['ROA_diff', 'ESG_diff', 'log_assets_diff', 'RD_diff'])
X_diff = sm.add_constant(df_dropna[['ESG_diff', 'log_assets_diff', 'RD_diff']])
y_diff = df_dropna['ROA_diff']
model_diff = sm.OLS(y_diff, X_diff).fit()

# Plot Wooldridge residuals
plt.figure(figsize=(8, 5))
sns.histplot(model_diff.resid, bins=30, kde=True, color='orangered')
plt.title('Residuals from Differenced OLS (Wooldridge-style Test)')
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), '../data/wooldridge_residuals.png'))
plt.show()

print("All diagnostics completed. Visual outputs saved in /data/")
