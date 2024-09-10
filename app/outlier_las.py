import pandas as pd
import numpy as np
import os

def read_csv_with_headers(file_path):
    """Reads a CSV file and determines if it has headers.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The DataFrame containing the data.
    """

    try:
        df = pd.read_csv(file_path, nrows=1)

        if list(df.columns) == ["Name", "Timestamp", "Price"]:
            # The file has the correct headers
            df = pd.read_csv(file_path)
        else:
            # The file does not have headers, use default names
            df = pd.read_csv(file_path, names=["Name", "Timestamp", "Price"])

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")

def random_data_points(file_path, num_points=30):
    """Selects a random sample of data points from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        num_points (int, optional): The number of data points to select. Defaults to 30.

    Returns:
        pandas.DataFrame: A DataFrame containing the selected data points.
    """

    try:
        df = read_csv_with_headers(file_path)

        # Ensure timestamp column exists and is of datetime type
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')

        if df["Timestamp"].isnull().all():
            raise ValueError("All Timestamp values are invalid dates.")

        # Get the index of the last 29 data points
        last_29_index = df.index[-29:]

        # Randomly select a starting index from the remaining data
        start_index = df.index.difference(last_29_index).sample(1).item()

        # Ensure the starting index allows for selecting 30 points
        start_index = max(0, start_index - num_points + 1)

        # Extract 30 consecutive data points starting from the selected index
        selected_data = df.iloc[start_index:start_index + num_points]

        # Check if there are enough data points
        if len(selected_data) < num_points:
            raise ValueError("Insufficient data points in the file.")

        return selected_data

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except ValueError as e:
        raise ValueError(f"Error processing file: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")

def detect_outliers(data):
    """Detects outliers in a DataFrame based on mean and standard deviation.

    Args:
        data (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.DataFrame: A DataFrame containing the detected outliers.
    """

    try:
        # Check for missing or invalid data
        if data.isnull().values.any():
            raise ValueError("Data contains missing or invalid values.")

        # Ensure data is numeric
        data["Price"] = pd.to_numeric(data["Price"])

        # Calculate mean and standard deviation
        mean = data["Price"].mean()
        std_dev = data["Price"].std()

        # Handle infinite values
        if np.isinf(mean) or np.isinf(std_dev):
            raise ValueError("Infinite mean or standard deviation.")

        # Calculate threshold and identify outliers
        threshold = 2 * std_dev
        data['Price-Mean'] = data['Price'] - mean
        data['% Deviation'] = (data['Price-Mean'] / mean) * 100
        outliers = data[(data["Price-Mean"]) > threshold]

        if not outliers.empty:
            outliers['Mean of 30 Selected Datapoints'] = mean
            outliers['% Deviation'] = (outliers['Price-Mean'] / threshold) * 100

        return outliers

    except ValueError as e:
        raise ValueError(f"Error detecting outliers: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")

def process_file(file_path):
    """Processes a single CSV file and identifies outliers.

    Args:
        file_path (str): The path to the CSV file.
    """

    try:
        df = read_csv_with_headers(file_path)

        if df.empty:
            raise ValueError(f"File '{file_path}' is empty.")

        sampled_data = random_data_points(file_path)
        outliers = detect_outliers(sampled_data)

        if not outliers.empty:
            outliers['Actual Price'] = outliers['Price']
            outliers['Name'] = outliers['Name']
            outliers['Timestamp'] = outliers['Timestamp']
            outliers['Mean of 30 Selected Datapoints'] = sampled_data["Price"].mean()
            outliers['Price-Mean'] = outliers['Actual Price'] - outliers['Mean of 30 Selected Datapoints']
            outliers['% Deviation'] = (outliers['Price-Mean'] / outliers['Mean of 30 Selected Datapoints']) * 100
            outliers.to_csv(f"{file_path[:-4]}_outliers.csv", index=False, columns=["Name", "Timestamp", "Actual Price", "Mean of 30 Selected Datapoints", "Price-Mean", "% Deviation"])
            print(f"Outliers found in {file_path}")
        else:
            print(f"No outliers found in {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_files_in_directory(directory):
    """Processes multiple CSV files in a directory.

    Args:
        directory (str): The path to the directory containing the files.
    """

    try:
        # Count the number of CSV files in the directory
        file_count = len([file for file in os.listdir(directory) if file.endswith(".csv")])

        # Check if the number of files is valid
        if file_count not in (1, 2):
            raise ValueError(f"Invalid number of files in the directory: {file_count}. Expected 1 or 2 files.")

        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)

            # Check if the file has a supported format
            if file.endswith(".csv"):
                process_file(file_path)

    except FileNotFoundError:
        raise FileNotFoundError(f"Directory '{directory}' not found.")
    except Exception as e:
        raise Exception(f"Error processing files: {e}")

# Usage example:
#directory_path = "path_to_dir"
#directory_path = "/home/ec2-user/api-testing/app/LSE"
#directory_path = "/home/ec2-user/api-testing/app/NASDAQ"
#directory_path = "/home/ec2-user/api-testing/app/NYSE"
try:
    process_files_in_directory(directory_path)
except Exception as e:
    print(f"Error: {e}")