import requests
import pandas as pd
import pgeocode
import json
import matplotlib.pyplot as plt
import tabulate
import os
from dotenv import load_dotenv
from pprint import pprint


def get_coord(zip_code):
    nomi = pgeocode.Nominatim('us')
    query = nomi.query_postal_code(zip_code)
    if query is None or query.empty or pd.isnull(query['latitude']) or pd.isnull(query['longitude']):
        raise ValueError("Invalid ZIP code or unable to retrieve coordinates")
    lat = query["latitude"]
    lon = query["longitude"]
    return lat, lon

def get_baseline(lat, lon):
    try:
        url = f'https://api.weather.gov/points/{lat},{lon}'
        response = requests.get(url)
        if response.status_code == 200:
            response_json = response.json()
            forecast_url = response_json['properties']['forecast']
        else:
            # Print an error message if the request was not successful
            print(f"Error: Unable to fetch data, status code {response.status_code}")
        return forecast_url
    except ValueError as e:
        print(e)

def get_forecast(forecast_url):
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code==200:
        forecast_json = forecast_response.json()
        
        periods = forecast_json['properties']['periods']
        
        dates = []
        is_day_time = []
        temps = []
        short_forecasts = []
        detailed_forecasts = []
        
        for period in periods:
            start_time = period['startTime']
            date = start_time.split('T')[0]
            date = pd.to_datetime(date).strftime('%m/%d/%Y')

            dates.append(date)
            is_day_time.append(period['isDaytime'])
            temps.append(period['temperature'])
            short_forecasts.append(period['shortForecast'])
            detailed_forecasts.append(period['detailedForecast'])

        weather_df = pd.DataFrame({
            'Date': dates,
            'Day Time': is_day_time,
            'Temp': temps,
            'Short Forecast': short_forecasts,
            'Detailed Forecast': detailed_forecasts
        })
        return weather_df
    else:
        print(f"Error: Unable to fetch data, status code {forecast_response.status_code}")

def plot_temperature_trends(weather_df):
    daytime_temps = weather_df[weather_df['Day Time'] == True]
    nighttime_temps = weather_df[weather_df['Day Time'] == False]
    weather_df['Date'] = pd.to_datetime(weather_df['Date'])
    plt.figure(figsize=(10, 6))
    plt.plot(daytime_temps['Date'], daytime_temps['Temp'], label='Highs (Daytime)', color='orange', marker='o')
    plt.plot(nighttime_temps['Date'], nighttime_temps['Temp'], label='Lows (Nighttime)', color='blue', marker='o')
    plt.title('Temperature Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (F)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

"""def show_weather_details(weather_df):
    weather_df['Day/Night'] = weather_df['Day Time'].apply(lambda x: 'Day' if x else 'Night')
    weather_df['Date'] = pd.to_datetime(weather_df['Date']).dt.strftime('%m/%d/%Y')

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(weather_df[['Date', 'Day/Night', 'Short Forecast', 'Detailed Forecast']].columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[weather_df['Date'], weather_df['Day/Night'], weather_df['Short Forecast'], weather_df['Detailed Forecast']],
                fill_color='lightblue',
                align='left'))
    ])
    fig.update_layout(title='Weather Forecast', title_x=0.5)
    fig.show()"""

def show_weather_details_table(weather_df):
    weather_df['Day/Night'] = weather_df['Day Time'].apply(lambda x: 'Day' if x else 'Night')
    weather_df['Date'] = pd.to_datetime(weather_df['Date']).dt.strftime('%m/%d/%Y')

    display_df = weather_df[['Date', 'Day/Night', 'Short Forecast', 'Detailed Forecast']]
    pprint(display_df)

def main():
    try:
        zip_code = input("Enter ZIP code ('#####'): ")
        lat, lon = get_coord(zip_code)
        forecast_url = get_baseline(lat, lon)
        
        if forecast_url:
            weather_df = get_forecast(forecast_url)
            
            if not weather_df.empty:
                plot_temperature_trends(weather_df)
                #show_weather_details(weather_df)
                show_weather_details_table(weather_df)
            else:
                print("No forecast data available.")
        else:
            print("Unable to retrieve the forecast URL.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()