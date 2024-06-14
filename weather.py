import tkinter as tk
import tkinter.messagebox as messagebox
import python_weather
import asyncio
import datetime
import os
from collections import Counter

class WeatherApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title(f"Previsão do Tempo - Usuário: {self.username}")
        self.geometry("400x300")

        self.label_city = tk.Label(self, text="Cidade:")
        self.label_city.pack()
        self.entry_city = tk.Entry(self)
        self.entry_city.pack()

        default_start_date = (datetime.datetime.now()).strftime("%d-%m-%Y")
        self.label_start_date = tk.Label(self, text="Data de Início (DD-MM-AAAA):")
        self.label_start_date.pack()
        self.entry_start_date = tk.Entry(self)
        self.entry_start_date.insert(0, default_start_date)
        self.entry_start_date.pack()

        default_end_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
        self.label_end_date = tk.Label(self, text="Data de Fim (DD-MM-AAAA):")
        self.label_end_date.pack()
        self.entry_end_date = tk.Entry(self)
        self.entry_end_date.insert(0, default_end_date)
        self.entry_end_date.pack()

        self.button_fetch_weather = tk.Button(self, text="Buscar Previsão do Tempo", command=self.run_fetch_weather)
        self.button_fetch_weather.pack()

        self.button_view_logs = tk.Button(self, text="View Logs", command=self.view_logs)
        self.button_view_logs.pack(pady=10)

        future_date = datetime.datetime.now().date() + datetime.timedelta(days=2)
        future_date = future_date.strftime("%d-%m-%Y")
        self.label_info = tk.Label(self, text=f"Nota: A previsão do tempo está disponível até {future_date}")
        self.label_info.pack(pady=10)

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

                    most_common_description = Counter(descriptions).most_common(1)[0][0] if descriptions else "Sem dados"
                    avg_rain_prob = sum(rain_probs) / len(rain_probs) if rain_probs else 0
                    avg_humidity = sum(humidity) / len(humidity) if humidity else 0

                    forecasts.append({
                        "Data": forecast_date.strftime('%Y-%m-%d'),
                        "Temperatura Média": f"{avg_temp}°C",
                        "Temperatura Mínima": f"{min_temp}°C",
                        "Temperatura Máxima": f"{max_temp}°C",
                        "Condição do Tempo": most_common_description,
                        "Probabilidade de Chuva": f"{avg_rain_prob}%",
                        "Umidade Média": f"{avg_humidity}%",
                        "Nascer do Sol": f"{sunrise}hrs",
                        "Pôr do Sol": f"{sunset}hrs",
                        "Fase da Lua": moon_phase

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
            self.log_weather(city, forecasts)  
            self.show_weather(forecasts, city)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar a previsão do tempo: {e}")

    def run_fetch_weather(self):
        asyncio.run(self.fetch_weather())
    
    def log_weather(self, city, forecasts):
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
        try:
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Usuário: {self.username}\n")
                log_file.write(f"Cidade: {self.returned_city}\n")
                for forecast in forecasts:
                    log_file.write("----------------------------------------\n")
                    for key, value in forecast.items():
                        log_file.write(f"{key}: {value}\n")
                log_file.write("----------------------------------------\n\n")
            print(f"Logged weather data to {log_file_path}")  # Debugging statement
        except Exception as e:
            print(f"Failed to log weather data: {e}")

    def view_logs(self):
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                logs = log_file.read()
            log_window = tk.Toplevel(self)
            log_window.title("Weather Logs")
            log_text = tk.Text(log_window)
            log_text.insert(tk.END, logs)
            log_text.pack()

    def ensure_logs_file(self):
        log_file_path = os.path.join(os.path.dirname(__file__), 'logs.txt')
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w') as log_file:
                log_file.write("Weather logs:\n")

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

        weather_window = tk.Toplevel(self)
        weather_window.title(f"Previsão do Tempo para {self.returned_city}")
        weather_window.geometry("600x400")

        scrollbar = tk.Scrollbar(weather_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(weather_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        text_widget.pack(expand=True, fill=tk.BOTH)
        text_widget.insert(tk.END, result_text)
        text_widget.config(state=tk.DISABLED)

        scrollbar.config(command=text_widget.yview)