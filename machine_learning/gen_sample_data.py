import pandas as pd
import numpy as np

# Define frequency and decibel ranges
frequency_range = np.arange(30, 141, 10)  # Frequencies from 30Hz to 140Hz
decibel_range = np.arange(-45, -29, 5)    # Decibels from -45dB to -30dB

# Create a list for the tones
tones = [f"{freq}_{dB}" for freq in frequency_range for dB in decibel_range]

# Create an empty list to store the data
data = []

# Define the number of users
num_users = 100  # You can adjust the number of users

# Loop to generate data for each user
for _ in range(num_users):
    # Generate binary responses for each tone
    responses = np.random.randint(0, 2, size=len(tones)).tolist()  # 0 or 1 for each tone
    data.append(responses)

# Create a DataFrame with the first row as tones
df = pd.DataFrame(data, columns=tones)

# Add a new column for age at the end
df['Age'] = np.random.randint(18, 60, size=num_users)  # Random age between 18 and 60

# Reorder the columns to have 'Age' as the last column
columns = df.columns.tolist()
columns = columns[-1:] + columns[:-1]  # Move 'Age' to the end
df = df[columns]

# Save the dataset to a CSV file
df.to_csv('./database/audiometric_test_dataset.csv', index=False)

print("Dataset generated and saved to database folder file named audiometric_test_dataset.csv")