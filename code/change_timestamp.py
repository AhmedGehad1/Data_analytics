import pandas as pd
from pathlib import Path

def convert_timestamp_ms_to_str(
    input_csv: str | Path,
    output_csv: str | Path,
    timestamp_col: str = 'Timestamp',
    time_format: str = '%Y/%m/%d %H:%M:%S'
) -> None:
    """
    Loads a CSV, converts a millisecond Timestamp column to formatted datetime strings,
    overwrites it (or renames column to 'Time'), and writes out a new CSV.

    Parameters
    ----------
    input_csv : str or Path
        Path to the source CSV file.
    output_csv : str or Path
        Path where the converted CSV should be saved.
    timestamp_col : str
        Name of the column in the input CSV containing integer milliseconds.
    time_format : str
        Datetime format string for strftime.

    Returns
    -------
    None
    """
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


    # 4) Save out the new CSV (only 'Time' and other columns remain)
    df.to_csv(output_csv, index=False)


# Example usage:
if __name__ == '__main__':
    convert_timestamp_ms_to_str(
        input_csv=r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\Heart_Rate_20231110.csv",
        output_csv=r"C:\Users\20111\Downloads\capsule\dataset\data\09\BCG\Heart_Rate_20231110_new_timestamp.csv",
        timestamp_col='Timestamp'
    )