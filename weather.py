import tkinter as tk
import tkinter.messagebox as messagebox
import python_weather
import asyncio
import datetime
from collections import Counter

class WeatherApp(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Weather App")
        self.geometry("400x350")
        self.user = user

        self.label_welcome = tk.Label(self, text=f"Bem-vindo, {self.user}!")
        self.label_welcome.pack()

        self.label_city = tk.Label(self, text="Cidade:")
        self.label_city.pack()
        self.entry_city = tk.Entry(self)
        self.entry_city.pack()

        self.label_start_date = tk.Label(self, text="Data de Início (DD-MM-AAAA):")
        self.label_start_date.pack()

        default_start_date = (datetime.datetime.now()).strftime("%d-%m-%Y")
        self.entry_start_date = tk.Entry(self)
        self.entry_start_date.insert(0, default_start_date)
        self.entry_start_date.pack()

        self.label_end_date = tk.Label(self, text="Data de Fim (DD-MM-AAAA):")
        self.label_end_date.pack()

        default_end_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
        self.entry_end_date = tk.Entry(self)
        self.entry_end_date.insert(0, default_end_date)
        self.entry_end_date.pack()

        info_text = f"A previsão do tempo está disponível até {default_end_date}."
        self.label_info = tk.Label(self, text=info_text)
        self.label_info.pack()

        self.button_fetch_weather = tk.Button(self, text="Buscar Previsão do Tempo", command=self.run_fetch_weather)
        self.button_fetch_weather.pack()

    async def get_weather(self, city, start_date, end_date):
        async with python_weather.Client(unit=python_weather.METRIC) as client:
            weather = await client.get(city)

            start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
            end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y").date()

            forecasts = []
            for daily in weather.daily_forecasts:
                forecast_date = daily.date
                if start_date <= forecast_date <= end_date:
                    avg_temp = daily.temperature
                    min_temp = daily.lowest_temperature
                    max_temp = daily.highest_temperature

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
                        "Temperatura Média": f"{avg_temp}°C",
                        "Temperatura Mínima": f"{min_temp}°C",
                        "Temperatura Máxima": f"{max_temp}°C",
                        "Condição do Tempo": most_common_description,
                        "Probabilidade de Chuva": f"{avg_rain_prob}%",
                        "Umidade Média": f"{avg_humidity}%"
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
            self.show_weather(forecasts, city)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar a previsão do tempo: {e}")

    def run_fetch_weather(self):
        asyncio.run(self.fetch_weather())

    def show_weather(self, forecasts, city):
        if not forecasts:
            messagebox.showinfo("Informação", "Não foram encontradas previsões para o período especificado.")
            return

        result_text = ""
        for forecast in forecasts:
            result_text += "----------------------------------------\n"
            for key, value in forecast.items():
                result_text += f"{key}: {value}\n"
            result_text += "----------------------------------------\n"
        print(result_text)
        weather_window = tk.Toplevel(self)
        weather_window.title(f"Previsão do Tempo para {city}")
        weather_window.geometry("600x400")

        scrollbar = tk.Scrollbar(weather_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(weather_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(expand=True, fill=tk.BOTH)

        text_widget.insert(tk.END, result_text)

        scrollbar.config(command=text_widget.yview)

