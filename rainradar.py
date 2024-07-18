from abc import ABC, abstractmethod
from matplotlib.figure import Figure
import requests
import customtkinter as ctk
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Classe abstraite pour définir l'interface des fetchers de données
class DataFetcher(ABC):
    def __init__(self, owm_api_key, geodb_api_key):
        self.owm_api_key = owm_api_key
        self.geodb_api_key = geodb_api_key

    @abstractmethod
    def get_weather(self, city):
        pass

    @abstractmethod
    def get_forecast(self, city):
        pass

    @abstractmethod
    def get_city_info(self, city):
        pass

# Classe concrète pour gérer les interactions avec les API
class WeatherFetcher(DataFetcher):
    def __init__(self, owm_api_key, geodb_api_key):
        super().__init__(owm_api_key, geodb_api_key)

    def get_weather(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.owm_api_key,
            "units": "metric",
            "lang": "fr"
        }
        response = requests.get(base_url, params=params)
        return response.json()

    def get_forecast(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": self.owm_api_key,
            "units": "metric",
            "lang": "fr"
        }
        response = requests.get(base_url, params=params)
        return response.json()

    def get_city_info(self, city):
        base_url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        headers = {
            "X-RapidAPI-Key": self.geodb_api_key,
            "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
        }
        params = {
            "namePrefix": city,
            "limit": 1
        }
        response = requests.get(base_url, headers=headers, params=params)
        return response.json()

class WeatherApp(ctk.CTk):
    def __init__(self, fetcher):
        super().__init__()
        self.fetcher = fetcher
        self.setup_ui()
        self.forecast_canvas = None  # Variable pour stocker le canvas du graphique

    def setup_ui(self):
        self.title("Application Météo")

        frame = ctk.CTkFrame(self)
        frame.pack(pady=20)

        city_label = ctk.CTkLabel(frame, text="Ville :")
        city_label.grid(row=0, column=0, padx=10)

        self.city_entry = ctk.CTkEntry(frame)
        self.city_entry.grid(row=0, column=1, padx=10)

        get_info_button = ctk.CTkButton(frame, text="Obtenir les informations", command=self.show_info)
        get_info_button.grid(row=0, column=2, padx=10)

        self.weather_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.weather_label.pack(pady=10)

        self.population_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.population_label.pack(pady=10)

        self.forecast_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14))
        self.forecast_label.pack(pady=10)

    def show_info(self):
        city = self.city_entry.get()
        if not city:
            ctk.CTkMessagebox.show_warning("Avertissement", "Veuillez entrer un nom de ville")
            return

        weather = self.fetcher.get_weather(city)
        if weather.get("cod") != 200:
            ctk.CTkMessagebox.show_error("Erreur", weather.get("message", "Erreur inconnue"))
            return

        self.display_weather_info(weather)

        city_info = self.fetcher.get_city_info(city)
        self.display_city_info(city_info)

        forecast = self.fetcher.get_forecast(city)
        self.display_forecast_info(forecast)

    def display_weather_info(self, weather):
        temp = weather["main"]["temp"]
        description = weather["weather"][0]["description"]
        humidity = weather["main"]["humidity"]
        wind_speed = weather["wind"]["speed"]
        weather_info = f"Température: {temp}°C\nDescription: {description.capitalize()}\nHumidité: {humidity}%\nVent: {wind_speed} m/s"
        self.weather_label.configure(text=weather_info)

    def display_city_info(self, city_info):
        if city_info["data"]:
            city_data = city_info["data"][0]
            population = city_data["population"]
            self.population_label.configure(text=f"Population: {population}")
        else:
            self.population_label.configure(text="Population: inconnue")

    def display_forecast_info(self, forecast):
        if forecast.get("cod") == "200":
            forecast_info = ""
            temperatures = []
            dates = []
            for i in range(0, 40, 8):
                day_forecast = forecast["list"][i]
                date = day_forecast["dt_txt"]
                temp = day_forecast["main"]["temp"]
                description = day_forecast["weather"][0]["description"]
                forecast_info += f"{date}: {temp}°C, {description.capitalize()}\n"
                temperatures.append(temp)
                dates.append(date)
            self.forecast_label.configure(text=forecast_info)
            self.create_forecast_graph(dates, temperatures)
        else:
            self.forecast_label.configure(text="Prévisions indisponibles")

    def create_forecast_graph(self, dates, temperatures):
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.plot(dates, temperatures, marker='o')
        ax.set_title("Prévisions des températures")
        ax.set_xlabel("Date")
        ax.set_ylabel("Température (°C)")
        ax.grid(True)
        fig.autofmt_xdate()

        # Si un graphique existe déjà, on le détruit avant d'en créer un nouveau
        if self.forecast_canvas is not None:
            self.forecast_canvas.get_tk_widget().destroy()

        # Intégrer le graphique dans la fenêtre Tkinter
        self.forecast_canvas = FigureCanvasTkAgg(fig, master=self)
        self.forecast_canvas.draw()
        self.forecast_canvas.get_tk_widget().pack(pady=10)

if __name__ == "__main__":
    OWM_API_KEY = "7030b33350c6ad1dae513c7908983388"
    GEODB_API_KEY = "a7c5ed1b6cmsh6e4b6c731836a57p17da0cjsn9bb8081a1a6b"

    # Configuration de l'apparence
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Initialisation de l'application
    fetcher = WeatherFetcher(OWM_API_KEY, GEODB_API_KEY)
    app = WeatherApp(fetcher)
    app.mainloop()
