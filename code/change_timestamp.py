import pandas as pd
from pathlib import Path

def convert_timestamp_ms_to_str(
    input_csv: str | Path,
    output_csv: str | Path,
    timestamp_col: str = 'Timestamp',
    time_format: str = '%Y/%m/%d %H:%M:%S'
) -> None:

    # 1) Load CSV, forcing integer type for timestamp column
    df = pd.read_csv(
        input_csv,
        dtype={timestamp_col: 'Int64'}
    )

    # 2) Convert ms → datetime, then format to string
    df[timestamp_col] = (
        pd.to_datetime(df[timestamp_col], unit='ms')
          .dt.strftime(time_format)
    )

    # 3) Save out the new CSV (only 'Time' and other columns remain)
    df.to_csv(output_csv, index=False)

# Example usage:
if __name__ == '__main__':
    convert_timestamp_ms_to_str(
        input_csv=r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\Heart_Rate_20231110.csv",
        output_csv=r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\Heart_Rate_20231110_new_timestamp.csv",
        timestamp_col='Timestamp'
    )