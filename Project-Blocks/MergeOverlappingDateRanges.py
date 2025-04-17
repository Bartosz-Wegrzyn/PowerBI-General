import pandas as pd
from datetime import datetime
# Load the CSV file
dataset = pd.read_csv('input.csv')

# Load the CSV file into a DataFrame
df = dataset

# Convert date columns to datetime format
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

# Sort data by ID and start date
df = df.sort_values(by=['ID', 'Start'])

# Function to merge overlapping intervals
def merge_intervals(group):
    merged = []
    group = group.sort_values(by='Start')
    
    current_start = group.iloc[0]['Start']
    current_end = group.iloc[0]['End']
    assignment_count = int(group.iloc[0]['A'])

    for i in range(1, len(group)):
        row = group.iloc[i]
        if row['Start'] <= current_end:
            # Merge intervals
            current_end = max(current_end, row['End'])
            assignment_count += int(row['A'])
        else:
            # Add the completed interval
            merged.append({
                'ID': group.iloc[0]['ID'],
                'Start Date': current_start,
                'End Date': current_end,
                'No. of As': assignment_count
            })
            # Reset for the new interval
            current_start = row['Start']
            current_end = row['End']
            assignment_count = int(row['A'])

    # Add the last interval
    merged.append({
        'ID': group.iloc[0]['ID'],
        'Start Date': current_start,
        'End Date': current_end,
        'No. of As': assignment_count
    })

    return pd.DataFrame(merged)

# Group by ID and apply the merge_intervals function
result = df.groupby('ID').apply(merge_intervals).reset_index(drop=True)

# Split the ID column into two columns: Consultant and Client
# Use expand=True and set a default value for Client when ID does not contain ":"
split_ids = result['ID'].str.split(':', n=1, expand=True)
split_ids.columns = ['Consultant', 'Client']
result = pd.concat([result, split_ids], axis=1)

# Drop the old ID column if it is no longer needed
result = result.drop(columns=['ID'])

# Save the result to an Excel file
result
