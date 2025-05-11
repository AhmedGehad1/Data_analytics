import pandas as pd
import numpy as np

def load_and_expand_timestamps(file_path: str) -> pd.DataFrame:
    """Loads BCG CSV, fills in missing timestamps using fs."""
    df = pd.read_csv(file_path, header=0, names=['BCG', 'Timestamp', 'fs'],
                     dtype={'BCG': float, 'Timestamp': float, 'fs': float})
    
    t0 = df.loc[0, 'Timestamp']
    fs = df.loc[0, 'fs']
    dt_ms = 1000.0 / fs
    offsets = np.arange(len(df)) * dt_ms
    df['Timestamp'] = t0 + offsets
    df['fs'] = fs
    df['Timestamp'] = df['Timestamp'].astype(np.int64)
    df['BCG'] = df['BCG'].astype(np.int64)
    df['fs'] = df['fs'].astype(np.int64)
    
    return df

def save_dataframe(df: pd.DataFrame, output_path: str):
    """Saves the DataFrame to CSV."""
    df.to_csv(output_path, index=False)
    print(f"Saved file: {output_path}")

def resample_signal(df: pd.DataFrame, fs_new: float) -> pd.DataFrame:
    """Resamples the BCG signal to a new sampling rate."""
    timestamps = df['Timestamp'].values.astype(np.float64)
    signal = df['BCG'].values
    
    dt_new_ms = 1000.0 / fs_new
    t_start, t_end = timestamps[0], timestamps[-1]
    new_timestamps = np.arange(t_start, t_end, dt_new_ms)
    new_signal = np.interp(new_timestamps, timestamps, signal)
    
    df_resampled = pd.DataFrame({
        'BCG': new_signal.astype(np.int64),
        'Timestamp': new_timestamps.astype(np.int64),
        'fs': int(fs_new)
    })
    
    return df_resampled

# === Example Usage ===
input_path = r'C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\09_20231110_BCG.csv'
output_path = input_path  # overwrite or provide a new path

# Step 1: Load and rebuild timestamps
df_original = load_and_expand_timestamps(input_path)

# Step 2: Resample the signal to 50 Hz
df_resampled = resample_signal(df_original, fs_new=50.0)

# Step 3: Save the resampled signal
save_dataframe(df_resampled, output_path)

print(f"Original samples: {len(df_original)}, Resampled to: {len(df_resampled)} at 50 Hz")
