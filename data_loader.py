import pandas as pd
import os


def get_single_city_data(city):
    file_path = os.path.join("Cities", f"{city}_final.csv")

    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # Convert date
    if 'Day' in df.columns:
        df['Date'] = pd.to_datetime(df['Day'], errors='coerce', dayfirst=True)
    else:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Rename columns (IMPORTANT: your CSV uses PM 10 / PM 2.5)
    df.rename(columns={
        'PM 10': 'PM10',
        'PM 2.5': 'PM2.5'
    }, inplace=True)

    # Convert numeric safely
    for col in ['PM10', 'PM2.5', 'AQI Value', 'Ozone']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Clean
    df = df.dropna(subset=['Date', 'AQI Value'])
    df = df.sort_values('Date')

    return df


def get_all_cities_data():
    cities = [
        "Patna","New Delhi","Mumbai","Gandhinagar","Surat",
        "Chennai","Kolkata","Lucknow","Bengaluru","Ahmedabad",
        "Kanpur","Jaipur","Indore","Nagpur","Srinagar",
        "Thane","Hyderabad","Visakhapatnam","Bhopal","Pune"
    ]

    data = {}

    for city in cities:
        df = get_single_city_data(city)
        data[city] = None if df is None else df.to_dict("records")

    return data
