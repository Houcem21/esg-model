# regression.py

import pandas as pd
import numpy as np
import os
from linearmodels.panel import PanelOLS
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
data_path = os.path.join(os.path.dirname(__file__), '../data/cleaned_panel.csv')
df = pd.read_csv(data_path)

# Set panel index
df = df.set_index(['company', 'year'])

# Define dependent and independent variables
# Step 5 model: ROA_it = β0 + β1*ESG_SCORE_it + β2*log_assets_it + β3*R&D_it + α_i + ε_it
y = df['RETURN_ON_ASSET']
X = df[['ESG_SCORE', 'log_assets', 'RD_transformed']]
X = sm.add_constant(X)

# Fit Fixed Effects model with robust standard errors
model = PanelOLS(y, X, entity_effects=True)
results = model.fit(cov_type='robust')

# Save regression summary to text file
with open(os.path.join(os.path.dirname(__file__), '../data/regression_summary.txt'), 'w') as f:
    f.write(results.summary.as_text())

# Extract and plot coefficients (exclude const)
coefs = results.params.drop('const')
errors = results.std_errors.loc[coefs.index]

plt.figure(figsize=(8, 5))
sns.barplot(
    x=coefs.values,
    y=coefs.index,
    hue=coefs.index,
    palette='crest',
    dodge=False,
    legend=False
)
plt.errorbar(
    x=coefs.values,
    y=np.arange(len(coefs)),
    xerr=errors.values,
    fmt='none',
    ecolor='gray',
    capsize=5,
    capthick=1
)
plt.axvline(0, color='gray', linestyle='--')
plt.title('Fixed Effects Regression Coefficients (Robust SE)')
plt.xlabel('Coefficient Value')
plt.ylabel('Variable')
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), '../data/regression_coefficients.png'))
plt.show()

print("Step 5 complete: Fixed Effects regression finished. Summary and visuals saved.")
