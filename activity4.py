




import requests
from datetime import datetime
import pytemperature

def get_weather_data(city, apikey):
    api_start = 'https://api.tomorrow.io/v4/timelines?'
    params = {
        'location': city,
        'fields': ['temperature', 'cloudCover', 'humidity', 'precipitationProbability', 'windDirection', 'windSpeed'],
        'units': 'metric',
        'timesteps': '1h',
        'apikey': apikey
    }
    try:
        response = requests.get(api_start, params=params)
        if response.status_code == 200:
            json_data = response.json()
            if 'data' not in json_data or not json_data['data']['timelines']:
                raise ValueError("Invalid city name or no data available.")
            return json_data
        else:
            response.raise_for_status()
    except (requests.RequestException, ValueError) as err:
        return {"error": str(err)}

def main():
    print("ISQA 3900 Weather API\n")
    choice = "y"

    while choice.lower() == "y":
        city = input("Enter City Name: ")
        apikey = 'rhX80J4KuqVSSicucCt2uifF2VQ21slW'  # Your actual API key
        json_data = get_weather_data(city, apikey)

        if 'error' in json_data:
            print(f"An error occurred: {json_data['error']}")
        elif 'data' in json_data:
            now = datetime.now()
            timeline = json_data['data']['timelines'][0]
            interval = timeline['intervals'][0]
            temp_c = interval['values']['temperature']
            temp_f = pytemperature.c2f(temp_c)
            cloud_cover = interval['values']['cloudCover']
            humidity = interval['values']['humidity']
            precip_prob = interval['values']['precipitationProbability']
            wind_dir = interval['values']['windDirection']
            wind_speed = interval['values']['windSpeed']

            output = (
                f"Current weather for {city}: {now.strftime('%A, %B %d, %Y, %I:%M%p')}\n"
                f"time = {interval['startTime']}\n"
                f"temp in C = {temp_c}\n"
                f"temp in F = {temp_f}\n"
                f"% Cloud Cover: {cloud_cover}\n"
                f"Humidity: {humidity}\n"
                f"Precipitation Probability: {precip_prob}\n"
                f"Wind Direction: {wind_dir}\n"
                f"Wind Speed: {wind_speed}\n"
            )

            print(output)

            filename = input("Enter the output filename: ")
            with open(filename, 'w') as file:
                file.write(output)
        else:
            print("An error occurred or no data available.")

        choice = input("Would you like to enter a new city (y or n): ")

    print("\nBye")

if __name__ == "__main__":
    main()
