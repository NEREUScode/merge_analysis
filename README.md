# merge_analysis
# Quickbase CSV Merge and Convert Tool

This tool automates the process of unzipping a ZIP file, merging all CSV files found within (including those in subdirectories), and then splitting and converting the merged CSV into one or more Excel files, each with up to 1 million rows to comply with Excel's limitations.

## Prerequisites

- Python 3.6 or newer. The script is not compatible with Python 2.x.
- pip (Python package installer)

## Setup Instructions

### 1. Verify Python Installation

Ensure that Python 3 and pip are installed on your system. Open a terminal or command prompt and run:

```bash
python3 --version
pip3 --version
```

If these commands do not return version numbers, please install Python 3 from [the official Python website](https://www.python.org/downloads/).

### 2. Clone Repository or Download Script

Download the script and the accompanying files (`requirements.txt`, `README.md`) to a directory on your machine.

### 3. Install Required Python Packages

Navigate to the directory containing the script and run the following command to install the necessary Python packages:

```bash
pip3 install -r requirements.txt
```

This will install `pandas` for data manipulation and `openpyxl` for writing Excel files.

## Usage

To use the script, run it from the command line, passing the path to the ZIP file as an argument:

```bash
python3 merge_csv.py <path_to_your_zip_file.zip>
```

Replace `<path_to_your_zip_file.zip>` with the actual path to your ZIP file.



## Output Structure

The script will create a directory with the same name as the ZIP file (without the `.zip` extension) in the same location as the ZIP file. Inside this directory, the following will be created:

- A single combined CSV file (`combined.csv`) containing all data merged from the found CSV files.
- One or more Excel files (`combined_part1.xlsx`, `combined_part2.xlsx`, ...) each containing up to 1 million rows of data from the combined CSV. The number of Excel files depends on the total rows in the combined CSV.

The script ensures that no data exceeds Excel's maximum row limit per sheet by splitting the data across multiple Excel files as necessary.

## Troubleshooting

- Ensure you have read and write permissions for the directory containing the ZIP file and its contents.
- Verify that the ZIP file is not corrupted and contains CSV files.
- If you encounter any errors related to Python versions, ensure that `python3` and `pip3` are correctly installed and aliased on your system.

To extend an existing README file to include documentation for `analysis.py` and its usage, follow these steps to create a clear, informative section. Assuming `analysis.py` is a script related to data analysis, such as the one you've described for generating a data tableau based on specific filters and modifications, here's a template you can adapt:

---

## Analysis Script: `analysis.py`

### Overview

`analysis.py` is a Python script designed for data analysis within our project. It filters data based on specific criteria, manipulates data according to predefined rules, and generates insightful tabular reports. This script is particularly useful for summarizing call data by description, after adjusting descriptions to remove unnecessary prefixes.

### Requirements

- Python 3.x
- Pandas library

Ensure you have Python installed on your system, and you can install Pandas using pip:

```bash
pip install pandas
```

### Usage

To use `analysis.py`, you'll need a CSV file or a DataFrame loaded into your Python environment that adheres to the expected structure (i.e., it must contain columns that match the `EMAIL_COL` and `DESCRIPTION_COL` used in the script).

1. **Prepare Your Data**: Ensure your data is in a CSV file or a DataFrame with the necessary columns. For `analysis.py`, the essential columns are:
   - An email column (specified by `EMAIL_COL`)
   - A description column (specified by `DESCRIPTION_COL`)

2. **Edit Script Constants**: Before running `analysis.py`, modify the constants at the top of the script to match your data column names:
   ```python
   EMAIL_COL = 'your_email_column_name'
   DESCRIPTION_COL = 'your_description_column_name'
   FILTER_EMAIL = 'email_to_filter@example.com'
   ```

3. **Run the Script**: If your data is in a CSV file, soe

   Then, call the function `generate_data_tableau_2(df)` to process the data:
   ```bash
   python3 analysis.py your_file.csv
   ```

### Output

The script outputs a PDF Report
