import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

# Folder containing the CSV files
folder_path = 'out/data/'

# Set Filter From to limit frames
filter_from = '06:00'

# Set Filter From to limit frames
filter_to = '23:00'

# List all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Initialize an empty list to store DataFrames
df_list = []

# Loop through all CSV files and read them into a DataFrame, then append to the list
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    df_list.append(df)

# Concatenate all DataFrames into one
df = pd.concat(df_list, ignore_index=True)

# Convert 'Time' column to datetime to make it easier to work with
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')

# Round the time to the nearest quarter hour
df['Time'] = df['Time'].dt.floor('15min')

# Filter data between 06:00 and 20:00 UTC
df = df[(df['Time'].dt.time >= pd.to_datetime(filter_from).time()) & (df['Time'].dt.time <= pd.to_datetime(filter_to).time())]


# Sort by day of the week and time
df['Day Of Week'] = pd.Categorical(df['Day Of Week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], ordered=True)
df = df.sort_values(by=['Day Of Week', 'Time'])

# Group by day of the week and time, then calculate the mean travel time for each group
average_df = df.groupby(['Day Of Week', 'Time'], observed=True)['Travel Time (minutes)'].mean().reset_index()

# Convert 'Time' column to string for plotting
average_df['Time'] = average_df['Time'].dt.strftime('%H:%M')

# Create the plot
plt.figure(figsize=(20, 12))

# Generate x-axis labels for every 15 minutes from 00:00 to 23:45
time_ticks = pd.date_range(filter_from, filter_to, freq='15min').strftime('%H:%M')


# Group by day of the week to plot separate lines for each day
for day in average_df['Day Of Week'].unique():
    day_data = average_df[average_df['Day Of Week'] == day]
    plt.plot(day_data['Time'], day_data['Travel Time (minutes)'], marker='o', label=day)

# Customize the plot
plt.title('Average Travel Time from Stettfurt to Dübendorf by Day and Time (UTC)')
plt.xlabel('Time of Day')

plt.ylabel('Average Travel Time (minutes)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)
plt.legend(title='Day of the Week')

# Save the graph as a PNG file
output_file = 'out/average_travel_time_plot.png'
plt.tight_layout()
plt.savefig(output_file)

print(f"Plot saved as {output_file}")
