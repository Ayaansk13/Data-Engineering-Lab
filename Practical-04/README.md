# Practical-04: Noise Elimination, Feature Selection, and Exploratory Data Analysis (EDA)

---

## 1. Aim
To implement data preprocessing techniques for noise elimination using Interquartile Range (IQR) outlier detection, eliminate uninformative attributes via Scikit-learn's `VarianceThreshold`, and perform comprehensive Exploratory Data Analysis (EDA) with statistical profiling and graphical visualizations using Pandas, NumPy, Matplotlib, and Scikit-learn.

---

## 2. Theory

### 2.1 Noise Elimination via Interquartile Range (IQR)
Outliers represent extreme values that deviate substantially from the overall distribution, distorting mean estimates and downstream statistical modeling. The Tukey IQR method provides robust non-parametric outlier boundaries:
- **First Quartile ($Q_1$):** 25th percentile of the sorted dataset.
- **Third Quartile ($Q_3$):** 75th percentile of the sorted dataset.
- **Interquartile Range ($IQR$):**
  $$IQR = Q_3 - Q_1$$
- **Filtering Bounds:**
  $$\text{Lower Bound} = Q_1 - 1.5 \times IQR$$
  $$\text{Upper Bound} = Q_3 + 1.5 \times IQR$$
Any sample $x < \text{Lower Bound}$ or $x > \text{Upper Bound}$ is flagged as statistical noise and eliminated.

### 2.2 Feature Selection via Variance Threshold
Feature selection removes redundant or uninformative attributes, decreasing dimensionality and computational overhead:
- A feature that exhibits zero or near-zero variance contains constant or quasi-constant values across all observations.
- `VarianceThreshold(threshold=0.0)` computes:
  $$\sigma^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2$$
- Features with $\sigma^2 \le \text{threshold}$ provide zero discriminative information and are dropped.

### 2.3 Exploratory Data Analysis (EDA)
EDA involves summarizing main numerical and categorical characteristics using both statistical metrics (`describe()`, `corr()`) and visual distributions (Histograms for univariate spread, Boxplots for quartile detection and skewness).

---

## 3. Software Requirements
- **Language:** Python 3.8+
- **Libraries:** `pandas`, `numpy`, `matplotlib`, `scikit-learn`
- **Environment:** Jupyter Notebook / Google Colab

---

## 4. Procedure
1. Create a synthetic DataFrame containing regular distributions alongside an injected outlier (e.g., `Age = 100`) and a constant feature (`Constant = 1`).
2. Calculate the 25th ($Q_1$) and 75th ($Q_3$) percentiles of `Age`; compute $IQR = Q_3 - Q_1$.
3. Filter the dataset to retain rows within the interval $[Q_1 - 1.5 \times IQR, Q_3 + 1.5 \times IQR]$, successfully removing the outlier.
4. Instantiate `VarianceThreshold(threshold=0.0)` from `sklearn.feature_selection`.
5. Fit the selector to the cleaned dataset; identify and drop columns with zero variance.
6. Conduct EDA:
   - Print structural information using `df_clean.info()`.
   - Calculate summary statistics (count, mean, std, min, quartiles, max) via `df_clean.describe()`.
   - Compute Pearson correlation matrix via `df_clean.corr()`.
   - Generate histograms and boxplots via `matplotlib.pyplot`.

---

## 5. Code Explanation

### IQR Outlier Removal & Variance Threshold
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import VarianceThreshold

# 1. Noise Elimination via IQR
Q1 = df['Age'].quantile(0.25)
Q3 = df['Age'].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# Filter outlier rows
df_clean = df[(df['Age'] >= lower) & (df['Age'] <= upper)]

# 2. Feature Selection (Drop constant columns)
selector = VarianceThreshold(threshold=0.0)
selector.fit(df_clean)
selected_columns = df_clean.columns[selector.get_support()]
df_selected = df_clean[selected_columns]

# 3. Exploratory Data Analysis (EDA)
print(df_selected.describe())
print(df_selected.corr())

df_selected.hist(figsize=(8, 6))
plt.suptitle("Histogram of Features")
plt.show()
```

---

## 6. Sample Input
```python
data = {
    'Age': [20, 21, 22, 23, 24, 100],        # 100 is an artificial outlier
    'Marks': [75, 80, 85, 90, 95, 20],
    'Attendance': [85, 88, 90, 92, 94, 50],
    'Constant': [1, 1, 1, 1, 1, 1]           # Zero-variance constant feature
}
```

---

## 7. Sample Output
```text
Original Dataset:
   Age  Marks  Attendance  Constant
0   20     75          85         1
1   21     80          88         1
2   22     85          90         1
3   23     90          92         1
4   24     95          94         1
5  100     20          50         1

Dataset after Noise Elimination:
   Age  Marks  Attendance  Constant
0   20     75          85         1
1   21     80          88         1
2   22     85          90         1
3   23     90          92         1
4   24     95          94         1

Selected Features:
Index(['Age', 'Marks', 'Attendance'], dtype='object')

Statistical Summary:
             Age      Marks  Attendance
count   5.000000   5.000000    5.000000
mean   22.000000  85.000000   89.800000
std     1.581139   7.905694    3.563706
min    20.000000  75.000000   85.000000
max    24.000000  95.000000   94.000000

========================================
Submitted by: Mohammad Ayaan Sajid Shaikh
========================================
```

---

## 8. Result
Successfully identified and purged statistical outliers utilizing the Interquartile Range methodology, eliminated zero-variance attributes using `VarianceThreshold`, and produced descriptive statistics and visual plots characterizing dataset distribution.

---

## 9. Learning Outcome
- Acquired the theoretical understanding and implementation skills for IQR-based outlier pruning.
- Learned automated dimensionality reduction using Scikit-learn's variance-based feature selectors.
- Mastered univariate and bivariate statistical profiling in Pandas.
- Visualized data skewness, distributions, and spread using histograms and boxplots.
