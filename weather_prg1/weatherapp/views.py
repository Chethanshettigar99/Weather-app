from django.shortcuts import render
import requests
from collections import defaultdict
from datetime import datetime

def index(request):
    api_key = 'cff24430cafc071bd92b2ec247332ffe'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST.get('city1')
        if city1:
            weather_data1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)
        else:
            weather_data1 = None
    else:
        weather_data1 = None

    context = {
        'weather_data1': weather_data1,
    }
    return render(request, 'index.html', context)

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    try:
        # Fetch current weather data
        current_response = requests.get(current_weather_url.format(city, api_key))
        current_data = current_response.json()

        if current_data.get('cod') != 200:
            return {'error': current_data.get('message', 'Error fetching current weather data')}

        # Extract latitude and longitude from current weather data
        lat, lon = current_data['coord']['lat'], current_data['coord']['lon']

        # Fetch 5-day forecast data using coordinates
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key))
        forecast_data = forecast_response.json()

        if forecast_data.get('cod') != '200':
            return {'error': forecast_data.get('message', 'Error fetching forecast data')}

        # Process the forecast data
        forecast_list = forecast_data.get('list', [])

        # Group forecast by date
        forecast_by_date = defaultdict(list)
        for forecast_item in forecast_list:
            dt = datetime.strptime(forecast_item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            date = dt.date()
            forecast_by_date[date].append({
                'time': dt.strftime('%H:%M'),
                'temperature': round(forecast_item['main']['temp'] - 273.15, 2),
                'description': forecast_item['weather'][0]['description'],
                'icon': forecast_item['weather'][0]['icon'],
                'wind_speed': forecast_item['wind']['speed'],
                'humidity': forecast_item['main']['humidity']
            })

        # Prepare forecast for the next 5 days
        forecast = []
        for date, forecasts in forecast_by_date.items():
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'forecasts': forecasts
            })

        # Extract current weather data
        weather_data = {
            'city': city,
            'temperature': round(current_data['main']['temp'] - 273.15, 2),
            'description': current_data['weather'][0]['description'],
            'icon': current_data['weather'][0]['icon'],
            'forecast': forecast[:5]  # Limit forecast to the next 5 days
        }

        return weather_data

    except Exception as e:
        return {'error': str(e)}