# generate_report.py

import os

# Paths
base_path = os.path.join(os.path.dirname(__file__), '../data')
summary_path = os.path.join(base_path, 'regression_summary.txt')
report_path = os.path.join(base_path, 'final_report.md')

# Read regression output
with open(summary_path, 'r') as f:
    regression_text = f.read()

# Build markdown report
report = f"""
# Final Report: ESG and Financial Performance in Danish Firms

## 1. Overview
This analysis evaluates how ESG scores relate to financial performance (ROA) in publicly listed Danish companies from 2021 to 2024.

## 2. Key Steps
- Outliers removed (ROA < -30%)
- R&D zeros replaced with random values between 1–3
- Log transformation of assets and R&D
- Sector dummies generated

## 3. Descriptive Statistics
![Variable Distributions](variable_distributions.png)

## 4. Correlation Matrix
![Correlation Heatmap](correlation_heatmap.png)

## 5. Multicollinearity (VIF)
![VIF Plot](vif_plot.png)

## 6. Regression Model
**Model Estimated:**
\[ ROA_{{it}} = \beta_0 + \beta_1 ESG_{{it}} + \beta_2 \log(Assets_{{it}}) + \beta_3 RD_{{it}} + \alpha_i + \epsilon_{{it}} \]

### Regression Output
```
{regression_text}
```

### Coefficients (Visual)
![Regression Coefficients](regression_coefficients.png)

## 7. Summary Dashboard
![Dashboard](final_dashboard.png)

---
**✅ Analysis Complete.** All plots, models, and diagnostics are now part of this report.
"""

with open(report_path, 'w') as f:
    f.write(report)

print("✅ Markdown report saved as 'final_report.md'")