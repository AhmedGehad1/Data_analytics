import pandas as pd

def synchronize_signals(bcg_path, rr_path, output_bcg_path, output_rr_path):
    """
    Synchronize two time-series CSV files based on exact timestamp overlap.
    - Ensures both outputs have identical timestamps and row count.
    - Resolves duplicate timestamps in RR using median.
    """

    # Load CSVs and parse timestamps
    bcg = pd.read_csv(bcg_path, parse_dates=["Timestamp"]).set_index("Timestamp")
    rr = pd.read_csv(rr_path, parse_dates=["Timestamp"]).set_index("Timestamp")

    # Handle duplicate timestamps using median
    bcg = bcg.groupby(bcg.index).median()
    rr = rr.groupby(rr.index).median()

    # Determine common timestamp range
    start = max(bcg.index.min(), rr.index.min())
    end = min(bcg.index.max(), rr.index.max())

    # Trim to common range
    bcg = bcg.loc[start:end]
    rr = rr.loc[start:end]

    # Intersect timestamps to ensure identical index
    common_index = bcg.index.intersection(rr.index)

    bcg_sync = bcg.loc[common_index].sort_index()
    rr_sync = rr.loc[common_index].sort_index()

    # Save to specified output paths
    bcg_sync.to_csv(output_bcg_path)
    rr_sync.to_csv(output_rr_path)

    print(f"Synchronized from {start} to {end}, with {len(common_index)} exact-matching timestamps.")

# Example usage:
synchronize_signals(
    bcg_path=r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\Heart_Rate_20231110_new_timestamp.csv",
    rr_path=r"C:\Users\20111\Downloads\capsule\dataset\data\09\Reference\RR\09_20231110_RR.csv",
    output_bcg_path=r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\hr_sync.csv",
    output_rr_path=r"C:\Users\20111\Downloads\capsule\dataset\data\09\Reference\RR\RR_sync_with_hr.csv"
)
