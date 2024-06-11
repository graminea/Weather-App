import tkinter as tk
import tkinter.messagebox as messagebox
import python_weather
import asyncio
import datetime
from collections import Counter

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("400x300")

        self.label_city = tk.Label(self, text="Cidade:")
        self.label_city.pack()
        self.entry_city = tk.Entry(self)
        self.entry_city.pack()

        self.label_start_date = tk.Label(self, text="Data de Início (AAAA-MM-DD):")
        self.label_start_date.pack()
        self.entry_start_date = tk.Entry(self)
        self.entry_start_date.pack()

        self.label_end_date = tk.Label(self, text="Data de Fim (AAAA-MM-DD):")
        self.label_end_date.pack()
        self.entry_end_date = tk.Entry(self)
        self.entry_end_date.pack()

        self.button_fetch_weather = tk.Button(self, text="Buscar Previsão do Tempo", command=self.fetch_weather)
        self.button_fetch_weather.pack()

    async def get_weather(self, city, start_date, end_date):
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            # Fetch the weather forecast for the specified city
            weather = await client.get(city)

            # Parse dates
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

            # Filter and display the forecasts within the specified date range
            forecasts = []
            for daily in weather.daily_forecasts:
                forecast_date = daily.date
                if start_date <= forecast_date <= end_date:
                    avg_temp = daily.temperature
                    min_temp = daily.lowest_temperature
                    max_temp = daily.highest_temperature

                    # Aggregate description and chances_of_rain from hourly forecasts
                    descriptions = []
                    rain_probs = []
                    humidity = []

                    for hourly in daily.hourly_forecasts:
                        descriptions.append(hourly.description)
                        rain_probs.append(hourly.chances_of_rain)
                        humidity.append(hourly.humidity)

                    if descriptions:
                        most_common_description = Counter(descriptions).most_common(1)[0][0]
                    else:
                        most_common_description = "Sem dados"

                    if rain_probs:
                        avg_rain_prob = sum(rain_probs) / len(rain_probs)
                    else:
                        avg_rain_prob = 0
                    
                    if humidity:
                        avg_humidity = sum(humidity) / len(humidity)
                    else:
                        avg_humidity = 0

                    forecasts.append({
                        "Data": forecast_date.strftime('%Y-%m-%d'),
                        "Temperatura Média": avg_temp,
                        "Temperatura Mínima": min_temp,
                        "Temperatura Máxima": max_temp,
                        "Condição do Tempo Mais Comum": most_common_description,
                        "Probabilidade Média de Chuva": avg_rain_prob,
                        "Umidade Média": avg_humidity
                    })

            return forecasts

    async def fetch_weather(self):
        city = self.entry_city.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()

        if not city or not start_date or not end_date:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            forecasts = await self.get_weather(city, start_date, end_date)
            self.show_weather(forecasts)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar a previsão do tempo: {e}")

    def show_weather(self, forecasts):
        if not forecasts:
            messagebox.showinfo("Informação", "Não foram encontradas previsões para o período especificado.")
            return

        result_text = ""
        for forecast in forecasts:
            result_text += "----------------------------------------\n"
            for key, value in forecast.items():
                result_text += f"{key}: {value}\n"
            result_text += "----------------------------------------\n"

        messagebox.showinfo("Previsão do Tempo", result_text)

if __name__ == '__main__':
    app = WeatherApp()

    # Create and run the event loop
    loop = asyncio.get_event_loop()
    loop.run_forever()
