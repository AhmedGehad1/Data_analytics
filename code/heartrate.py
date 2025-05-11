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
    return pd.DataFrame({'Timestamp': timestamps, 'BPM': bpm_array})

def plot_bpm_over_time(df: pd.DataFrame):
    """Plot BPM vs. Time."""
    plt.figure(figsize=(10, 5))
    plt.plot(df['Timestamp'], df['BPM'], marker='o', linestyle='-', color='r')
    plt.title("Heart Rate Over Time")
    plt.xlabel("Timestamp (ms)")
    plt.ylabel("Heart Rate (BPM)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def save_bpm_to_csv(df: pd.DataFrame, output_path: str):
    """Save BPM DataFrame to CSV."""
    df.to_csv(output_path, index=False)
    print(f"Saved BPM data to: {output_path}")

# === Example usage ===
def main():
    bcg_path = r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\09_20231110_BCG.csv"
    output_csv = r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\Heart_Rate_20231110.csv"
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
