import pandas as pd

def check_duplicate_ids(file_path):
    # Read the CSV file
    try:
        data = pd.read_csv(file_path)
    except FileNotFoundError:
        print("The specified file was not found.")
        return
    except pd.errors.EmptyDataError:
        print("The file is empty.")
        return
    except pd.errors.ParserError:
        print("Error parsing the file. Please check the format.")
        return

    # Check for duplicates in the 'Add ID' column
    duplicates = data[data.duplicated(subset='Add ID', keep=False)]

    if not duplicates.empty:
        print("Duplicate IDs found:")
        print(duplicates)
    else:
        print("No duplicate IDs found.")

# Example usage
file_path = 'merged.csv'  # Replace with your actual CSV file path
check_duplicate_ids(file_path)