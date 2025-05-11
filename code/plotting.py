import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def plot_hr_analysis(reference_csv_path, estimated_csv_path, column_name='Heart Rate'):
    """
    Perform Bland–Altman analysis and visual comparison of heart rate estimates.

    Parameters:
    - reference_csv_path (str): Path to the reference HR CSV file.
    - estimated_csv_path (str): Path to the estimated HR CSV file.
    - column_name (str): Name of the HR column in both files (default: 'Heart Rate').
    """

    # Load data
    ref_df = pd.read_csv(reference_csv_path)
    est_df = pd.read_csv(estimated_csv_path)

    # Extract HR columns
    ref_hr = ref_df[column_name].values
    est_hr = est_df[column_name].values

    # Length check
    if len(ref_hr) != len(est_hr):
        raise ValueError("Length mismatch: reference and estimated HR arrays are not equal.")

    # Build combined DataFrame
    df = pd.DataFrame({
        'Reference_HR': ref_hr,
        'Estimated_HR': est_hr
    })

    # Bland–Altman statistics
    mean_hr = df.mean(axis=1)
    diff_hr = df['Estimated_HR'] - df['Reference_HR']
    bias = np.mean(diff_hr)
    sd_diff = np.std(diff_hr, ddof=1)
    loa_upper = bias + 1.96 * sd_diff
    loa_lower = bias - 1.96 * sd_diff

    # Plotting
    plt.figure(figsize=(16, 4))

    # 1. Bland–Altman plot
    plt.subplot(1, 3, 1)
    plt.scatter(mean_hr, diff_hr, alpha=0.6)
    plt.axhline(bias, color='gray', linestyle='--', label=f'Bias={bias:.2f}')
    plt.axhline(loa_upper, color='gray', linestyle=':', label=f'+1.96 SD={loa_upper:.2f}')
    plt.axhline(loa_lower, color='gray', linestyle=':', label=f'-1.96 SD={loa_lower:.2f}')
    plt.title('Bland–Altman Plot')
    plt.xlabel('Mean HR (bpm)')
    plt.ylabel('Difference (Est – Ref)')
    plt.legend()

    # 2. Pearson correlation
    plt.subplot(1, 3, 2)
    sns.regplot(x='Reference_HR', y='Estimated_HR', data=df, ci=95, scatter_kws={'alpha': 0.6})
    r, p = stats.pearsonr(df['Reference_HR'], df['Estimated_HR'])
    plt.title(f'Pearson r = {r:.2f}, p = {p:.3f}')
    plt.xlabel('Reference HR (bpm)')
    plt.ylabel('Estimated HR (bpm)')

    # 3. Boxplot comparison
    plt.subplot(1, 3, 3)
    df_melt = df.melt(var_name='Type', value_name='HR')
    sns.boxplot(x='Type', y='HR', data=df_melt)
    plt.title('HR Distribution Comparison')
    plt.ylabel('Heart Rate (bpm)')
    plt.xlabel('')

    plt.tight_layout()
    plt.show()

# Example usage:
plot_hr_analysis(
    reference_csv_path=r'C:\Users\20111\Downloads\capsule\dataset\data\09\Reference\RR\RR_sync_with_hr.csv',
    estimated_csv_path=r'C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\hr_sync.csv'
)
