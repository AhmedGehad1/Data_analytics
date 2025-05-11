# from scipy.signal import butter, filtfilt, find_peaks
# import matplotlib.pyplot as plt
# import pandas as pd

# # Load the updated BCG file
# updated_bcg_df = pd.read_csv("C:\\Users\\20111\\Downloads\\capsule\\dataset\\data\\01\\BCG\\01_20231104_BCG_updated.csv")

# # Extract signal and timestamps
# bcg_signal = updated_bcg_df['BCG'].values
# timestamps = updated_bcg_df['Timestamp'].values
# fs = updated_bcg_df['fs'].iloc[0]

# # Step 1: Bandpass Filter (0.5 - 15 Hz)
# def bandpass_filter(signal, lowcut, highcut, fs, order=4):
#     nyq = 0.5 * fs
#     low = lowcut / nyq
#     high = highcut / nyq
#     b, a = butter(order, [low, high], btype='band')
#     return filtfilt(b, a, signal)

# filtered_bcg = bandpass_filter(bcg_signal, 0.5, 15, fs)

# # Step 2: Detect Peaks (J-peaks are typically the tallest upward peaks)
# # We set distance according to 40 BPM max heart rate → 60/40 * fs ≈ 210 samples apart
# min_distance = int(0.4 * fs)
# peaks, _ = find_peaks(filtered_bcg, distance=min_distance, prominence=5)

# # Extract peak timestamps
# jpeak_timestamps = timestamps[peaks]

# # Save peaks to file
# jpeaks_df = pd.DataFrame({
#     'Index': peaks,
#     'Timestamp': jpeak_timestamps,
#     'Amplitude': filtered_bcg[peaks]
# })
# jpeaks_path = "C:\\Users\\20111\\Downloads\\capsule\\dataset\\data\\01\\BCG\\J_peaks_detected.csv"
# jpeaks_df.to_csv(jpeaks_path, index=False)

# # Plot a short segment for visualization
# plt.figure(figsize=(12, 4))
# segment = slice(5000, 7000)
# plt.plot(timestamps[segment], filtered_bcg[segment], label="Filtered BCG")
# plt.plot(timestamps[peaks[(peaks > 5000) & (peaks < 7000)]],
#          filtered_bcg[peaks[(peaks > 5000) & (peaks < 7000)]], 'rx', label="J-peaks")
# plt.xlabel("Timestamp (ms)")
# plt.ylabel("Amplitude")
# plt.title("BCG Signal with J-peaks")
# plt.legend()
# plt.tight_layout()
# plt.show()

# jpeaks_path
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# from band_pass_filtering import band_pass_filtering
# from detect_peaks import detect_peaks

# # --- Load your BCG data ---
# bcg_path = "C:\\Users\\20111\\Downloads\\capsule\\dataset\\data\\01\\BCG\\BCG_resampled_50Hz.csv"
# bcg_df = pd.read_csv(bcg_path)

# # --- Extract signal and parameters ---
# signal = bcg_df['BCG']  # Adjust column name if different
# fs = bcg_df['fs'].iloc[0]  # Sampling frequency

# # --- Filter the BCG signal to isolate the heart component (J-peaks range) ---
# filtered_signal = band_pass_filtering(signal, fs, filter_type="bcg")

# # --- Detect peaks in the filtered signal (potential J-peaks) ---
# j_peak_indices = detect_peaks(
#     filtered_signal,
#     mph=np.percentile(filtered_signal, 90),  # Use top 10% height as threshold
#     mpd=int(0.5 * fs),  # Minimum peak distance of 0.5 seconds
#     threshold=0.05 * np.max(filtered_signal),  # Neighbor difference
#     edge='rising',
#     show=True
# )

# # --- Extract timestamps and peak amplitudes ---
# timestamps = bcg_df['Timestamp'].iloc[j_peak_indices].values
# j_peaks = filtered_signal[j_peak_indices]

# # --- Combine for review ---
# j_peaks_df = pd.DataFrame({
#     'Timestamp': timestamps,
#     'Amplitude': j_peaks,
#     'SampleIndex': j_peak_indices
# })

# # --- Save if needed ---
# j_peaks_df.to_csv("C:\\Users\\20111\\Downloads\\J_peaks_detected.csv", index=False)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from band_pass_filtering import band_pass_filtering
from detect_peaks import detect_peaks

# --- Load your 50Hz BCG data ---
bcg_path = "C:\\Users\\20111\\Downloads\\capsule\\dataset\\data\\01\\BCG\\BCG_resampled_50Hz.csv"
bcg_df = pd.read_csv(bcg_path)

# --- Define sampling frequency manually ---
fs = 50  # Hz

# --- Extract signal ---
signal = bcg_df['BCG']  # Make sure this is the correct column name

# --- Filter the BCG signal to isolate the heart component (J-peaks) ---
filtered_signal = band_pass_filtering(signal, fs, filter_type="bcg")

# --- Detect J-peaks in the filtered signal ---
j_peak_indices = detect_peaks(
    filtered_signal,
    mph=np.percentile(filtered_signal, 90),         # Top 10% amplitude
    mpd=int(0.5 * fs),                              # 0.5 sec spacing
    threshold=0.05 * np.max(filtered_signal),       # Relative prominence
    edge='rising',
    show=True
)

# --- Extract timestamps and amplitudes ---
timestamps = bcg_df['Timestamp'].iloc[j_peak_indices].values
j_peaks = filtered_signal[j_peak_indices]

# --- Save J-peaks ---
j_peaks_df = pd.DataFrame({
    'Timestamp': timestamps,
    'Amplitude': j_peaks,
    'SampleIndex': j_peak_indices
})
j_peaks_df.to_csv("C:\\Users\\20111\\Downloads\\J_peaks_detected50hz.csv", index=False)
