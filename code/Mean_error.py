import numpy as np
import pandas as pd

def evaluate_heart_rate(reference_csv_path, estimated_csv_path, column_name='Heart Rate'):
    """
    Evaluate estimated heart rate data against reference heart rate data.

    Parameters:
    - reference_csv_path (str): Path to the reference heart rate CSV file.
    - estimated_csv_path (str): Path to the estimated heart rate CSV file.
    - column_name (str): Column name for heart rate values in both files (default: 'Heart Rate').

    Returns:
    - dict: A dictionary containing MAE, RMSE, and MAPE values.
    """

    # Load CSV files
    ref_df = pd.read_csv(reference_csv_path)
    est_df = pd.read_csv(estimated_csv_path)

    # Extract heart rate columns
    y_ref = ref_df[column_name].values
    y_est = est_df[column_name].values

    # Check alignment
    if len(y_ref) != len(y_est):
        raise ValueError(f"Length mismatch: reference={len(y_ref)}, estimated={len(y_est)}")

    # Compute error metrics
    mae = np.mean(np.abs(y_est - y_ref))
    rmse = np.sqrt(np.mean((y_est - y_ref) ** 2))
    mape = np.mean(np.abs((y_est - y_ref) / y_ref)) * 100

    # Print results
    print(f"MAE:  {mae:.2f} bpm")
    print(f"RMSE: {rmse:.2f} bpm")
    print(f"MAPE: {mape:.2f}%")

    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}

#MAE (Mean Absolute Error):
# Calculates the absolute difference between each pair of estimated and reference values.
# Then, it computes the average of these absolute differences. MAE gives an idea of the average magnitude of the errors.

# RMSE (Root Mean Squared Error): 
# Calculates the difference between each pair of values.
# Squares these differences (this penalizes larger errors more heavily).
# Computes the average of these squared differences (this is the Mean Squared Error, MSE).
# Takes the square root of the MSE to bring the error back to the original units of heart rate. RMSE is sensitive to large errors.

# MAPE (Mean Absolute Percentage Error): 
# Calculates the absolute difference between each pair.
# Divides this difference by the actual reference value to get a percentage error for each point.
# Computes the average of these absolute percentage errors.
# Multiplies by 100 to express it as a percentage. MAPE indicates the average error relative to the true values.