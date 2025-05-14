from pathlib import Path
import pandas as pd
import generate_timestamp_and_resampling as gtr
import BCG_heartrate as BCG_hr
import change_timestamp as ct
import synchronization as sync
import Mean_error as er
import plotting as pl

DATA_ROOT    = Path("dataset/data")
RESULTS_ROOT = Path("code/My_results")
RESULTS_ROOT.mkdir(parents=True, exist_ok=True)

def find_csv_pairs(subject_dir: Path):
    bcg_dir = subject_dir / "BCG"
    rr_dir  = subject_dir / "Reference" / "RR"

    if not bcg_dir.is_dir() or not rr_dir.is_dir():
        return []

    bcg_files = list(bcg_dir.glob("*.csv"))
    rr_files  = list(rr_dir.glob("*.csv"))

    print(f"  Found {len(bcg_files)} BCG files, {len(rr_files)} RR files in {subject_dir.name}")

    # build map of RR by the first-11-character prefix (e.g. '01_20231104')
    rr_map = {f.stem[:11]: f for f in rr_files}

    pairs = []
    for bcg in bcg_files:
        prefix = bcg.stem[:11]
        if prefix in rr_map:
            pairs.append((bcg, rr_map[prefix]))
        else:
            print(f"    No RR match for BCG {bcg.name} (prefix {prefix})")
    return pairs


def process_pair(subject_id: str, bcg_path: Path, rr_path: Path):
    # Use first-11-character prefix to name folder
    prefix = bcg_path.stem[:11]
    out_dir = RESULTS_ROOT / subject_id / prefix
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"→ Processing {subject_id}/{prefix}")

    # 1) Timestamp generation & 50 Hz resampling
    ts_csv = out_dir / f"{prefix}_bcg_timestamp.csv"
    df0 = gtr.load_and_expand_timestamps(str(bcg_path))
    df1 = gtr.resample_signal(df0, fs_new=50.0)
    gtr.save_dataframe(df1, str(ts_csv))

    # 2) BCG → Heart rate (BPM)
    hr_csv = out_dir / f"{prefix}_bcg_hr.csv"
    sig, times = BCG_hr.load_bcg_data(str(ts_csv))
    filt = BCG_hr.compute_filtered_signal(sig, fs=50)
    bpm = BCG_hr.calculate_bpm_array(filt, fs=50, win_sec=10)
    bpm_df = BCG_hr.build_bpm_dataframe(bpm, times, fs=50, win_sec=10)
    BCG_hr.save_bpm_to_csv(bpm_df, str(hr_csv))
    BCG_hr.plot_bpm_over_time(bpm_df, str(hr_csv))

    # 3) Convert timestamp formatting
    ts_fmt_csv = out_dir / f"{prefix}_bcg_hr_ts_fmt.csv"
    ct.convert_timestamp_ms_to_str(
        input_csv = str(hr_csv),
        output_csv= str(ts_fmt_csv),
        timestamp_col='Timestamp'
    )

    # 4) Synchronize with RR
    sync_bcg = out_dir / f"{prefix}_hr_sync.csv"
    sync_rr  = out_dir / f"{prefix}_rr_sync.csv"
    sync.synchronize_signals(
        bcg_path        = str(ts_fmt_csv),
        rr_path         = str(rr_path),
        output_bcg_path = str(sync_bcg),
        output_rr_path  = str(sync_rr)
    )

    # 5) Calculate Mean error on these specific synced files
    er.evaluate_heart_rate(
        reference_csv_path = str(sync_rr),
        estimated_csv_path = str(sync_bcg)
    )

    # 6) Final analysis plot
    pl.plot_hr_analysis(
        reference_csv_path = str(sync_rr),
        estimated_csv_path = str(sync_bcg),
        save_path = str(out_dir / f"{prefix}_analysis.png")
    )
    print(f" ✔ Completed {subject_id}/{prefix}")


def main():
    for subject in sorted(DATA_ROOT.iterdir()):
        if not subject.is_dir(): 
            continue

        print(f"\nSubject {subject.name}:")
        pairs = find_csv_pairs(subject)
        if not pairs:
            print(f"[!] No BCG/RR CSVs found in {subject.name}")
            continue

        for bcg_file, rr_file in pairs:
            print(f"→ Processing subject {subject.name}, prefix {bcg_file.stem[:11]}")
            process_pair(subject.name, bcg_file, rr_file)

if __name__ == "__main__":
    main()