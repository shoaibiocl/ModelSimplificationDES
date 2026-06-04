"""
Sampling Sensitivity Test & Statistical Validation

Conducts a sensitivity analysis using a One-way ANOVA and 95% Confidence 
Interval (CI) profiling. Verifies if varying the number of entities sampled 
causes a statistically significant difference in the recorded metric: 
'Number of Instructions per Arrival'.

Inputs:
    - 'ModelSimplification-NI-Sensitivity.xlsx' (Sheet2): Experimental logs 
      where columns represent different entity sampling thresholds.

Outputs:
    - Terminal: F-statistic and p-value from the One-way ANOVA.
    - Visual: Saves a 95% CIs plot
      across groups to 'figures/sampling_sensitivity_ci.png'.
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.stats import f_oneway

"The code for conducting one-way ANOVA on the group means as a sensitivity test. 
The code also generates 95% CI plots for the means."

# 1. Load data
xl = pd.read_excel('ModelSimplification-NI-Sensitivity.xlsx', sheet_name='Sheet2', header=None)

# Row 1 = group labels, rows 2+ = data
labels = [str(x) for x in xl.iloc[1].tolist()]
group_data = {}
for col_idx, label in enumerate(labels):
    vals = pd.to_numeric(xl.iloc[2:, col_idx], errors='coerce').dropna().values
    group_data[label] = vals

groups = list(group_data.keys())

# 2. ANOVA
f_stat, anova_p = f_oneway(*group_data.values())
print(f"One-way ANOVA: F = {f_stat:.4f}, p = {anova_p:.6f}")

# 3. 95% Confidence intervals 
means, ci_low, ci_high = [], [], []
for g in groups:
    d = group_data[g]
    m = np.mean(d)
    se = stats.sem(d)
    ci = stats.t.ppf(0.975, df=len(d) - 1) * se
    means.append(m)
    ci_low.append(m - ci)
    ci_high.append(m + ci)

#  Palette (extend or replace colours as needed) 
PALETTE = ['#378ADD', '#1D9E75', '#D85A30', '#7F77DD', '#BA7517', '#E05FA0', '#5BBFBF']
PALETTE = (PALETTE * 5)[:len(groups)]  # cycle if more than 7 groups

# Figure 
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

for i, (g, m, lo, hi, color) in enumerate(zip(groups, means, ci_low, ci_high, PALETTE)):
    ax.plot([i + 1, i + 1], [lo, hi], color=color, linewidth=2, solid_capstyle='round', zorder=3)
    ax.plot([i + 0.85, i + 1.15], [lo, lo], color=color, linewidth=1.5, zorder=3)
    ax.plot([i + 0.85, i + 1.15], [hi, hi], color=color, linewidth=1.5, zorder=3)
    ax.plot(i + 1, m, 'o', color=color, markersize=8, zorder=4,
            markeredgecolor='white', markeredgewidth=1.5)

# Axes
y_all = ci_low + ci_high
pad = (max(y_all) - min(y_all)) * 0.8
ax.set_ylim(min(y_all) - pad, max(y_all) + pad)
ax.set_xlim(0.4, len(groups) + 0.6)

ax.set_xticks(range(1, len(groups) + 1))
ax.set_xticklabels(groups, fontsize=11)
ax.set_ylabel('No. of instructions/arrival', fontsize=11, labelpad=8, color='#444444')
ax.set_xlabel('Sample Size', fontsize=11, labelpad=8, color='#444444')
ax.tick_params(axis='both', length=0, labelcolor='#444444', labelsize=10)

for spine in ['top', 'right', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_linewidth(0.6)
ax.spines['left'].set_color('#cccccc')
ax.yaxis.grid(True, linestyle='-', linewidth=0.4, color='#eeeeee', zorder=0)
ax.set_axisbelow(True)

# ── ANOVA annotation
p_str = '< 0.001' if anova_p < 0.001 else f'= {anova_p:.3f}'
sig_str = '— significant differences exist' if anova_p < 0.05 else '— no significant differences between groups'
anova_label = f'One-way ANOVA  F = {f_stat:.3f},  p {p_str}  {sig_str}'
ax.text(0.5, -0.13, anova_label, transform=ax.transAxes,
        fontsize=8.5, ha='center', color='#888888')

plt.tight_layout()
plt.savefig('ci_plot.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
print("\nSaved: ci_plot.png")
