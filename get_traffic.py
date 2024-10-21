import os
import googlemaps
import csv
import schedule
import time
from datetime import datetime, timedelta

# Read API key and environment from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')
ENV = os.getenv('ENV', 'prod')  # Defaults to 'prod' if ENV is not set

if not API_KEY:
    raise ValueError("No API key found in the environment. Please set the GOOGLE_API_KEY environment variable.")

gmaps = googlemaps.Client(key=API_KEY)

# Define your origin and destination
origin = os.getenv("LOCATION_START",'Stettfurt')
destination = os.getenv("LOCATION_DESTINATION", 'Überlandstrasse 1, Dübendorf')

# Path to the CSV file
csv_file = 'out/data/traffic_data_'+time.strftime("%Y%m%d-%H%M%S")+'.csv'

# Function to round time to the nearest quarter hour
def round_time_to_quarter_hour(dt):
    """Rounds a datetime object to the nearest quarter hour."""
    minute = (dt.minute // 15) * 15
    if dt.minute % 15 >= 8:
        minute += 15
    rounded_time = dt.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minute)
    return rounded_time.strftime('%H:%M')

# Function to get travel time and write it to a CSV file
def get_travel_time():
    now = datetime.now()
    # Request directions
    result = gmaps.distance_matrix(origins=origin, 
                                   destinations=destination, 
                                   mode='driving', 
                                   departure_time='now')
    
    # Parse the result
    try:
        # Extracting the travel time in minutes
        travel_time_text = result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        travel_time_minutes = int(travel_time_text.split()[0])  # Extract only the number part

        # Prepare data for CSV
        day_of_week = now.strftime('%A')  # Day of the week (e.g., Monday)
      

        print(f'{day_of_week} | {now} | {travel_time_minutes} minutes')

        # Write to CSV
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([day_of_week, now, travel_time_minutes])
            
    except KeyError:
        print("Error fetching the travel time, check your API response.")

# Create the CSV file with headers if it doesn't exist
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Day Of Week", "Time", "Travel Time (minutes)"])

# Schedule the job
def schedule_traffic_updates():
    current_day = datetime.now().weekday()
    current_time = datetime.now().time()

    if ENV == 'dev':
        # In development mode, run immediately and every 10 seconds
        print("Development mode: Running immediately and every 10 seconds.")
        schedule.every(10).seconds.do(get_travel_time)
    else:
        # In production mode, schedule only between 7 AM to 10 AM, Monday to Friday
        # if current_day < 5 and current_time >= datetime.strptime('07:00:00', '%H:%M:%S').time() and current_time <= datetime.strptime('10:00:00', '%H:%M:%S').time():
        print("Production mode: Scheduling every 5 minutes between 7 AM and 10 AM.")
        schedule.every(5).minutes.do(get_travel_time)

schedule_traffic_updates()
get_travel_time()
# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
