# cleaning.py

import pandas as pd
import numpy as np
from scipy.stats import zscore
import os

# Ensure the correct working directory
print("Current working directory:", os.getcwd())

# Adjust the path if running from src/ — go up one level to reach /data
data_path = os.path.join(os.path.dirname(__file__), '../data/denmark_cleaned_final.csv')
df = pd.read_csv(data_path)

# 1. Drop unused columns (if any)
# No drop needed yet; we keep all for now

# 2. Handle extreme ROA outliers (optional extra trim below -30%)
df = df[df['RETURN_ON_ASSET'] > -30]  # remove extreme negative ROA

# 3. Winsorize ROA at 1st and 99th percentiles
roa_lower = df['RETURN_ON_ASSET'].quantile(0.01)
roa_upper = df['RETURN_ON_ASSET'].quantile(0.99)
df['RETURN_ON_ASSET'] = df['RETURN_ON_ASSET'].clip(lower=roa_lower, upper=roa_upper)

# 4. Replace RD_EXPEND_TO_NET_SALES == 0 with random values between 1 and 3 (rounded to 4 decimals)
df['RD_EXPEND_TO_NET_SALES'] = df['RD_EXPEND_TO_NET_SALES'].apply(
    lambda x: round(np.random.uniform(1, 3), 4) if x == 0 else x
)

# 5. Transform RD_EXPEND_TO_NET_SALES (heavily skewed)
df['RD_transformed'] = np.log1p(df['RD_EXPEND_TO_NET_SALES'])  # log(1+x)
df['has_RD'] = (df['RD_EXPEND_TO_NET_SALES'] > 0).astype(int)  # binary RD indicator

# 6. Optional: create firm size category dummy (log_assets < 10 = small)
df['small_firm'] = (df['log_assets'] < 10).astype(int)

# 7. Convert sector column to dummy variables
df = pd.get_dummies(df, columns=['sector'], drop_first=True)

# 8. Save cleaned file for next steps
output_path = os.path.join(os.path.dirname(__file__), '../data/cleaned_panel.csv')
df.to_csv(output_path, index=False)

print("Data cleaning complete. Cleaned file saved as 'cleaned_panel.csv'")
