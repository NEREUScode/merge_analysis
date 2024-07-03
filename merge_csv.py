import sys
import subprocess
import os
import glob
import pandas as pd

# Constants
UNZIP_OVERWRITE_FLAG = '-o'
CSV_FILE_EXTENSION = '*.csv'
EXCEL_FILE_EXTENSION = 'xlsx'
COMBINED_CSV_FILENAME = "combined.csv"
COMBINED_EXCEL_FILENAME_PREFIX = "combined_part"
MAX_EXCEL_ROWS = 1000000  # Cap at 1 million rows per Excel file
USAGE_MESSAGE = "Usage: python script.py <zip_file_path>"

def unzip_file(zip_file, destination_folder):
    try:
        subprocess.check_call(['unzip', UNZIP_OVERWRITE_FLAG, zip_file, '-d', destination_folder])
        print(f"Unzipped file to {destination_folder}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to unzip file: {e}")
        sys.exit(1)

def merge_csvs(folder_path):
    csv_files = glob.iglob(os.path.join(folder_path, '**', CSV_FILE_EXTENSION), recursive=True)
    combined_df = pd.DataFrame()
    for file in csv_files:
        try:
            df = pd.read_csv(file, low_memory=False)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            print(f"Failed to process file {file}: {e}")
    return combined_df.drop_duplicates()

def convert_to_excel(df, output_excel_prefix):
    num_parts = (len(df) + MAX_EXCEL_ROWS - 1) // MAX_EXCEL_ROWS  # Ensure proper division and rounding up
    for part in range(num_parts):
        start_row = part * MAX_EXCEL_ROWS
        end_row = start_row + MAX_EXCEL_ROWS
        output_excel = f"{output_excel_prefix}_part{part + 1}.{EXCEL_FILE_EXTENSION}"
        
        try:
            df.iloc[start_row:end_row].to_excel(output_excel, index=False)
            print(f"Part {part + 1} of the data saved to {output_excel}")
        except Exception as e:
            print(f"Failed to convert CSV to Excel: {e}")
            sys.exit(1)

def main(zip_file):
    if not os.path.exists(zip_file):
        print("Zip file does not exist.")
        sys.exit(1)
    
    destination_folder = zip_file.rsplit('.', 1)[0]
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    unzip_file(zip_file, destination_folder)
    
    combined_df = merge_csvs(destination_folder)
    
    output_csv = os.path.join(destination_folder, COMBINED_CSV_FILENAME)
    combined_df.to_csv(output_csv, index=False)
    print(f"CSV files have been combined and saved to {output_csv}")
    
    output_excel_prefix = os.path.join(destination_folder, COMBINED_EXCEL_FILENAME_PREFIX)
    convert_to_excel(combined_df, output_excel_prefix)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(USAGE_MESSAGE)
        sys.exit(1)
    
    zip_file_path = sys.argv[1]
    main(zip_file_path)

