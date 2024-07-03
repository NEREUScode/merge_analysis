import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys
from datetime import datetime, timedelta
from pandas.plotting import table

# Constants
DESCRIPTION_COL = 'DESCRIPTION'
TIME_COL = 'TIME (ISO-8601)'
EMAIL_COL = 'EMAIL ADDRESS'
TOP_DESCRIPTIONS_COUNT = 5
FILTER_EMAIL = 'factory.qbase@ceva.com'
FILTER_DESCRIPTION_CONTAINS = 'Factory QBASE called the api API_DoQuery on table Professionals in app WP - Web Platform'

# Ensure correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python analysis.py <path_to_csv_file>")
    sys.exit(1)

# Parse command-line arguments
input_csv_path = sys.argv[1]

# Function to read the CSV file
def read_csv_file(file_path, email_filter):
    dtype_specification = {10: 'str'}  # Assuming you want to force column 10 to be read as strings.
    
    # Read the CSV file with dtype specifications
    df = pd.read_csv(file_path, parse_dates=[TIME_COL], dtype=dtype_specification, low_memory=False)
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], errors='coerce')
    # Filter by email if needed
    if email_filter and EMAIL_COL in df.columns:
        df = df[df[EMAIL_COL] == email_filter]
    
    return df

# Function to fill missing days with -1
def fill_missing_days(df, date_column):
    df = df.drop_duplicates(subset=[date_column])  # Drop duplicates based on the date column
    df.set_index(date_column, inplace=True)
    min_date = df.index.min()
    max_date = df.index.max()
    all_days = pd.date_range(start=min_date, end=max_date, freq='D')
    df = df.reindex(all_days, fill_value=0).rename_axis(date_column).reset_index()
    return df


# Tableau 1 [Graph]
# Description, Day, Total Calls Per Day (Description,time, filter = {user : factory.qbase@ceva.com})
"""
def generate_data_tableau_1(df):
    df_filtered = df[df[EMAIL_COL] == FILTER_EMAIL]
    df_filtered = df_filtered.groupby([TIME_COL, DESCRIPTION_COL]).size().reset_index(name='Total Calls')
    df_filtered = fill_missing_days(df_filtered, TIME_COL)
    return df_filtered
"""

# Tableau 2
# Description, Total Calls by Description (Description , filter = {user : factory.qbase@ceva.com})
def generate_data_tableau_2(df):
    # Assuming EMAIL_COL and DESCRIPTION_COL are defined elsewhere
    # Filter data by email
    df_filtered = df[df[EMAIL_COL] == FILTER_EMAIL]  
    # Remove "Factory QBASE " from each description
    df_filtered[DESCRIPTION_COL] = df_filtered[DESCRIPTION_COL].str.replace("Factory QBASE ", "")   
    # Count total calls by (now modified) description
    total_calls_by_description = df_filtered.groupby(DESCRIPTION_COL).size().reset_index(name='Total Calls')
    
    return total_calls_by_description.sort_values('Total Calls', ascending=False)


# Tableau 3 [Graph]
# Day, Total Calls by Day (day)
def generate_data_tableau_3(df):
    total_calls_by_day = df.groupby(df[TIME_COL].dt.date).size().reset_index(name='Total Calls')
    total_calls_by_day = fill_missing_days(total_calls_by_day, TIME_COL)
    return total_calls_by_day

# Tableau 4 [Graph]
# Day, Total Calls by Day for Pro (description = professional, day)
def generate_data_tableau_4(df):
    df_pro = df[df[DESCRIPTION_COL].str.contains(FILTER_DESCRIPTION_CONTAINS)]
    total_calls_by_day_pro = df_pro.groupby(df_pro[TIME_COL].dt.date).size().reset_index(name='Total Calls')
    total_calls_by_day_pro = fill_missing_days(total_calls_by_day_pro, TIME_COL)
    return total_calls_by_day_pro

# Functions to plot each tableau
def plot_tableau_1(data):
    plt.figure(figsize=(10, 5))
    for description in data[DESCRIPTION_COL].unique():
        subset = data[data[DESCRIPTION_COL] == description]
        plt.plot(subset[TIME_COL], subset['Total Calls'], label=description)
    plt.yscale('log')  # Set the y-axis to a logarithmic scale
    plt.xlabel('Day')
    plt.ylabel('Total Calls (Log Scale)')
    plt.title('Total Calls Per Day for Each Description on Log Scale')
    plt.legend()

def plot_tableau_2(data):
    # Set up the figure. The figsize will need to be adjusted by your table's aspect ratio
    fig, ax = plt.subplots(figsize=(11.7, 8.3))  # Landscape orientation (A4 size)
    ax.axis('tight')
    ax.axis('off')
    
    # Create the table
    the_table = table(ax, data, loc='center', cellLoc = 'center', rowLoc = 'center')

    # Perhaps set font size of the table if necessary
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)
    the_table.scale(1.2, 0.8)  # You may need to adjust the scaling to fit your data

    plt.title('Total Calls by Description')

    return fig  # Return the figure to be saved into the PDF

def plot_tableau_3(data):
    plt.figure(figsize=(10, 5))
    plt.plot(data[TIME_COL], data['Total Calls'])
    plt.xlabel('Day')
    plt.ylabel('Total Calls')
    plt.title('Total Calls by Day')

def plot_tableau_4(data):
    plt.figure(figsize=(10, 5))
    plt.plot(data[TIME_COL], data['Total Calls'])
    plt.xlabel('Day')
    plt.ylabel('Total Calls')
    plt.title('Total Calls by Day for Professionals Segments')

# Main script execution
if __name__ == "__main__":
    # Read CSV file with filter applied
    df = read_csv_file(input_csv_path, FILTER_EMAIL)
    
    # Generate data for each tableau
    #data_tableau_1 = generate_data_tableau_1(df)
    data_tableau_2 = generate_data_tableau_2(df)
    data_tableau_3 = generate_data_tableau_3(df)
    data_tableau_4 = generate_data_tableau_4(df)
    
    # Plot each tableau
    with PdfPages(f'QuickbaseAnalysis-{datetime.now().strftime("%Y-%m-%d")}.pdf') as pdf:
        """
        plt.figure(figsize=(11.7, 8.3))  # Landscape orientation A4
        plot_tableau_1(data_tableau_1)
        pdf.savefig()
        plt.close()
        """
        
        plt.figure(figsize=(8.3,11.7))
        plot_tableau_2(data_tableau_2)
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(11.7, 8.3))
        plot_tableau_3(data_tableau_3)
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(11.7, 8.3))
        plot_tableau_4(data_tableau_4)
        pdf.savefig()
        plt.close()
