import pandas as pd

# Lists for mapping
disk = ['NAVE-D', 'NAVE-E', 'NAVE-F', 'NAVE-H']
name = ['AD-Pan-02', 'AD-Pan-05', 'AD-Pan-04', 'AD-PAN-TR01']

# Read the input CSV file
output_file = "dataCollection.csv"
dataFile = pd.read_csv('dataCollection.csv')

# Ensure the 'Ubicacion' column exists
if 'Ubicacion' not in dataFile.columns:
    raise ValueError("Column 'Ubicacion' not found in the CSV file.")

# Function to replace multiple occurrences
def replace_locations(cell_content):
    for i, location in enumerate(disk):
        # Splitting the cell content to replace each location accurately
        if location in cell_content.split(', '):
            cell_content = cell_content.replace(location, name[i])
    return cell_content

# Apply the function to each cell in the Ubicacion column
dataFile['Ubicacion'] = dataFile['Ubicacion'].apply(replace_locations)

# Save the modified DataFrame back to a CSV file
dataFile.to_csv(output_file, index=False)
