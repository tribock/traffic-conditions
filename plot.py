import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
csv_file = 'sample/Sample_Travel_Time_Data.csv'
df = pd.read_csv(csv_file)

# Convert 'Time' column to datetime to make it easier to work with
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M')

# Round the time to the nearest quarter hour
df['Time'] = df['Time'].dt.floor('15T')

# Sort by day of the week and time
df['Day Of Week'] = pd.Categorical(df['Day Of Week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], ordered=True)
df = df.sort_values(by=['Day Of Week', 'Time'])

# Group by day of the week and time, then calculate the mean travel time for each group
average_df = df.groupby(['Day Of Week', 'Time'])['Travel Time (minutes)'].mean().reset_index()

# Convert 'Time' column to string for plotting
average_df['Time'] = average_df['Time'].dt.strftime('%H:%M')

# Create the plot
plt.figure(figsize=(10, 6))

# Group by day of the week to plot separate lines for each day
for day in average_df['Day Of Week'].unique():
    day_data = average_df[average_df['Day Of Week'] == day]
    plt.plot(day_data['Time'], day_data['Travel Time (minutes)'], marker='o', label=day)

# Customize the plot
plt.title('Average Travel Time from Stettfurt to Dübendorf by Day and Time')
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
