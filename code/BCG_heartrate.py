import os
import matplotlib
matplotlib.use('TkAgg')  # Add this line before importing pyplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from band_pass_filtering import band_pass_filtering
from compute_vitals import vitals


def load_bcg_data(filepath: str) -> tuple[np.ndarray, np.ndarray]:
    """Load BCG data and return signal and timestamps."""
    df = pd.read_csv(filepath)
    return df['BCG'].values, df['Timestamp'].values

def compute_filtered_signal(signal: np.ndarray, fs: int) -> np.ndarray:
    """Apply bandpass filtering to the BCG signal."""
    return band_pass_filtering(signal, fs, filter_type="bcg")

def calculate_bpm_array(filtered_signal: np.ndarray, fs: int, win_sec: int = 10) -> np.ndarray:
    """Compute heart rate (BPM) over sliding windows."""
    win_size = int(win_sec * fs)
    window_limit = len(filtered_signal) // win_size
    time_ms = np.arange(len(filtered_signal)) * (1000 / fs)
    
    bpm_array = vitals(
        t1=0,
        t2=win_size,
        win_size=win_size,
        window_limit=window_limit,
        sig=filtered_signal,
        time=time_ms,
        mpd=int(0.5 * fs),  # Minimum peak distance = 0.5 sec
        plot=0
    )
    return bpm_array

def build_bpm_dataframe(bpm_array: np.ndarray, timestamps: np.ndarray, fs: int, win_sec: int = 10) -> pd.DataFrame:
    """Create a DataFrame with timestamps and BPM values."""
    win_size = int(win_sec * fs)
    timestamps = timestamps[::win_size][:len(bpm_array)]
    return pd.DataFrame({'Timestamp': timestamps, 'Heart Rate': bpm_array})

def plot_bpm_over_time(df: pd.DataFrame, output_path: str):
    """Plot BPM vs. Time with smoothing and improved style, and save to file."""
    import os
    plt.figure(figsize=(12, 6))
    # Plot raw data
    plt.plot(df['Timestamp'], df['Heart Rate'], marker='o', linestyle='-', color='lightcoral', markersize=2, linewidth=0.7, alpha=0.5, label='Raw HR')
    # Plot rolling mean
    if len(df) > 20:
        df['HR_Smooth'] = df['Heart Rate'].rolling(window=20, min_periods=1, center=True).mean()
        plt.plot(df['Timestamp'], df['HR_Smooth'], color='navy', linewidth=2, label='Smoothed HR')
    plt.title("Heart Rate Over Time", fontsize=16)
    plt.xlabel("Timestamp (ms)", fontsize=14)
    plt.ylabel("Heart Rate (BPM)", fontsize=14)
    plt.ylim(df['Heart Rate'].min() - 5, df['Heart Rate'].max() + 5)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    # Save plot to the same directory as output CSV, with .png extension
    plot_path = os.path.splitext(output_path)[0] + ".png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved BPM plot to: {plot_path}")

def save_bpm_to_csv(df: pd.DataFrame, output_path: str):
    """Save BPM DataFrame to CSV."""
    df.to_csv(output_path, index=False)
    print(f"Saved BPM data to: {output_path}")

# === Example usage ===
def main():
    bcg_path = r'C:\Users\ahmad\Desktop\capsule\dataset\data\09\BCG\09_20231110_BCG.csv'
    output_csv = r'code/My_results\09_20231110_BCG.csv'
    fs = 50  # Sampling rate in Hz
    
    # 1. Load & filter signal
    signal, timestamps = load_bcg_data(bcg_path)
    filtered = compute_filtered_signal(signal, fs)
    
    # 2. Compute HR (BPM) in windows
    bpm_array = calculate_bpm_array(filtered, fs, win_sec=10)
    
    # 3. Build and save DataFrame
    bpm_df = build_bpm_dataframe(bpm_array, timestamps, fs, win_sec=10)
    save_bpm_to_csv(bpm_df, output_csv)
    
    # 4. Plot
    plot_bpm_over_time(bpm_df)

if __name__ == "__main__":
    main()
