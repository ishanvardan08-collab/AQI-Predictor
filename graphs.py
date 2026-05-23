import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from data_loader import get_single_city_data


def generate_city_graph(city):
    df = get_single_city_data(city)

    if df is None or df.empty:
        return None

    PM10 = df['PM10'].tolist()
    PM2_5 = df['PM2.5'].tolist()
    aqi = df['AQI Value'].tolist()
    ozone = df['Ozone'].tolist()

    x = np.arange(1, len(aqi) + 1)

    if len(aqi) < 3:
        return None

    # Polynomial fit
    poly1 = np.poly1d(np.polyfit(x, PM10, 2))
    poly2 = np.poly1d(np.polyfit(x, PM2_5, 2))
    poly3 = np.poly1d(np.polyfit(x, aqi, 2))
    poly4 = np.poly1d(np.polyfit(x, ozone, 2))

    future_x = np.arange(len(aqi) + 1, len(aqi) + 4)

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(f"{city} Air Quality Trends")

    # PM10
    axs[0,0].plot(x, PM10, marker='o', color='blue')
    axs[0,0].plot([x[-1]] + list(future_x),
                  [PM10[-1]] + list(poly1(future_x)),
                  '--', color='red')
    axs[0,0].set_title("PM10")
    axs[0,0].grid(True)

    # PM2.5
    axs[0,1].plot(x, PM2_5, marker='o', color='violet')
    axs[0,1].plot([x[-1]] + list(future_x),
                  [PM2_5[-1]] + list(poly2(future_x)),
                  '--', color='orange')
    axs[0,1].set_title("PM2.5")
    axs[0,1].grid(True)

    # AQI
    axs[1,0].plot(x, aqi, marker='o', color='red')
    axs[1,0].plot([x[-1]] + list(future_x),
                  [aqi[-1]] + list(poly3(future_x)),
                  '--', color='blue')
    axs[1,0].set_title("AQI")
    axs[1,0].grid(True)

    # Ozone
    axs[1,1].plot(x, ozone, marker='o', color='green')
    axs[1,1].plot([x[-1]] + list(future_x),
                  [ozone[-1]] + list(poly4(future_x)),
                  '--', color='purple')
    axs[1,1].set_title("Ozone")
    axs[1,1].grid(True)

    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode('utf-8')
