import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

cities = [
    "Patna", "New Delhi", "Mumbai", "Gandhinagar", "Surat",
    "Chennai", "Kolkata", "Lucknow", "Bengaluru", "Ahmedabad",
    "Kanpur", "Jaipur", "Indore", "Nagpur", "Srinagar",
    "Thane", "Hyderabad", "Visakhapatnam", "Bhopal", "Pune"
]

if not os.path.exists("Cities"):
    os.makedirs("Cities")

def generate_city_data(city):
    days = 30
    
    # Generate dates as YYYY-MM-DD without time, ending yesterday
    end_date = datetime.now().date() - timedelta(days=1)
    dates = pd.date_range(end=end_date, periods=days, freq='D')

    pm10 = np.random.randint(80, 200, days)
    pm25 = np.random.randint(50, 150, days)
    ozone = np.random.randint(20, 60, days)

    # AQI calculation 
    aqi = (pm25 * 0.6 + pm10 * 0.4).astype(int)

    df = pd.DataFrame({
        "Date": dates.strftime('%Y-%m-%d'), 
        "PM10": pm10,      
        "PM2.5": pm25,     
        "AQI Value": aqi,
        "Ozone": ozone
    })

    df.to_csv(f"Cities/{city}_final.csv", index=False)
    print(f"{city} CSV created")

# generate all
for city in cities:
    generate_city_data(city)

print("All CSV files created successfully!")
