Overview
This Python script is designed to detect outliers in CSV or XLSX files containing stock price data. It processes files in a specified directory, selects random data points, calculates outliers based on a predefined threshold, and generates a CSV file with the detected outliers.

Requirements
Python 2.7 or later
pandas
numpy
os

**Install dependencies:**

pip install   
 pandas numpy

Usage
Place your CSV or XLSX files in a directory.
Modify the directory_path variable in the script to point to the correct directory.
Run the script: python outlier_las.py

Output
The script will generate a CSV file for each processed file, named [filename]_outliers.csv. The output file will contain the following columns:

Name: The stock name.
Timestamp: The timestamp of the outlier.
Actual Price: The actual stock price at the timestamp.
Mean of 30 Selected Datapoints: The mean of the 30 randomly selected data points.
Price-Mean: The difference between the actual price and the mean.
% Deviation: The percentage deviation of the outlier from the mean.

Notes
The script assumes that the CSV files have the following columns: Name, Timestamp, and Price.( not necessary that we have these headings ) 
The script uses a threshold of 2 standard deviations to identify outliers.
The script handles potential errors like invalid file paths, empty files, and data format issues.

