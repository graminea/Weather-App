import python_weather
import asyncio
import datetime
import os
from collections import Counter
from database import Database

class WeatherService:
    def __init__(self):
        self.returned_city = None
        self.db = Database()
        self.ensure_logs_file()

    async def get_weather(self, city, start_date, end_date):
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(city)
            self.returned_city = weather.location.title()
            start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
            end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y").date()

            forecasts = []
            for daily in weather.daily_forecasts:
                forecast_date = daily.date
                if start_date <= forecast_date <= end_date:
                    avg_temp = daily.temperature
                    min_temp = daily.lowest_temperature
                    max_temp = daily.highest_temperature
                    moon_phase = daily.moon_phase
                    sunrise = daily.sunrise
                    sunset = daily.sunset

                    descriptions = []
                    rain_probs = []
                    humidity = []

                    for hourly in daily.hourly_forecasts:
                        descriptions.append(hourly.description)
                        rain_probs.append(hourly.chances_of_rain)
                        humidity.append(hourly.humidity)

                    most_common_description = Counter(descriptions).most_common(1)[0][0] if descriptions else "No data"
                    avg_rain_prob = sum(rain_probs) / len(rain_probs) if rain_probs else 0
                    avg_humidity = sum(humidity) / len(humidity) if humidity else 0

                    forecasts.append({
                        "Date": forecast_date.strftime('%d/%m/%Y'),
                        "Average Temperature": f"{avg_temp}°C",
                        "Minimum Temperature": f"{min_temp}°C",
                        "Maximum Temperature": f"{max_temp}°C",
                        "Weather Condition": most_common_description,
                        "Rain Probability": f"{avg_rain_prob}%",
                        "Average Humidity": f"{avg_humidity}%",
                        "Sunrise": f"{sunrise}hrs",
                        "Sunset": f"{sunset}hrs",
                        "Moon Phase": str(moon_phase)
                    })

            return forecasts

    def log_weather(self, username, city, forecasts):
        # Save to text file (existing functionality)
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
        try:
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"User: {username}\n")
                log_file.write(f"City: {self.returned_city}\n")
                for forecast in forecasts:
                    log_file.write("----------------------------------------\n")
                    for key, value in forecast.items():
                        log_file.write(f"{key}: {value}\n")
                    log_file.write("----------------------------------------\n\n")
            print(f"Logged weather data to {log_file_path}")
        except Exception as e:
            print(f"Failed to log weather data to file: {e}")

        # Save to database
        try:
            log_entry = {
                "username": username,
                "city": self.returned_city,
                "query_date": datetime.datetime.now(),
                "forecasts": forecasts,
                "forecast_count": len(forecasts)
            }
            self.db.insert_one('weather_logs', log_entry)
            print(f"Logged weather data to database for user: {username}")
        except Exception as e:
            print(f"Failed to log weather data to database: {e}")

    def ensure_logs_file(self):
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w') as log_file:
                log_file.write("Weather logs:\n")

    def get_logs(self):
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                return log_file.read()
        return "No logs found"

    def get_logs_from_db(self, username=None, limit=50):
        """Get logs from database with optional filtering by username"""
        try:
            query = {}
            if username:
                query['username'] = username
            
            logs = list(self.db.find_many('weather_logs', query).sort('query_date', -1).limit(limit))
            return logs
        except Exception as e:
            print(f"Failed to get logs from database: {e}")
            return []

    def get_user_stats(self, username):
        """Get statistics for a specific user"""
        try:
            total_queries = self.db.get_collection('weather_logs').count_documents({'username': username})
            cities_queried = len(self.db.get_collection('weather_logs').distinct('city', {'username': username}))
            
            # Get recent activity
            recent_logs = list(self.db.find_many('weather_logs', {'username': username})
                             .sort('query_date', -1).limit(5))
            
            return {
                'total_queries': total_queries,
                'cities_queried': cities_queried,
                'recent_activity': recent_logs
            }
        except Exception as e:
            print(f"Failed to get user stats: {e}")
            return {'total_queries': 0, 'cities_queried': 0, 'recent_activity': []}

