import requests
import customtkinter as ctk
from PIL import Image, ImageTk
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Clés API (à remplacer par vos propres clés)
OWM_API_KEY = "#1api key here"
GEODB_API_KEY = "#2api key here"

# Fonctions pour obtenir les données des APIs
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OWM_API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    response = requests.get(base_url, params=params)
    return response.json()

def get_forecast(city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": OWM_API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    response = requests.get(base_url, params=params)
    return response.json()

def get_city_info(city):
    base_url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    headers = {
        "X-RapidAPI-Key": GEODB_API_KEY,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    params = {
        "namePrefix": city,
        "limit": 1
    }
    response = requests.get(base_url, headers=headers, params=params)
    return response.json()

# Fonction pour afficher les informations
def show_info():
    city = city_entry.get()
    if city:
        weather = get_weather(city)
        forecast = get_forecast(city)
        city_info = get_city_info(city)

        if weather.get("cod") != 200:
            ctk.CTkMessagebox.show_error("Erreur", weather.get("message", "Erreur inconnue"))
        else:
            temp = weather["main"]["temp"]
            description = weather["weather"][0]["description"]
            humidity = weather["main"]["humidity"]
            wind_speed = weather["wind"]["speed"]
            weather_info = f"Température: {temp}°C\nDescription: {description.capitalize()}\nHumidité: {humidity}%\nVent: {wind_speed} m/s"
            weather_label.configure(text=weather_info)

            if city_info["data"]:
                city_data = city_info["data"][0]
                population = city_data["population"]
                population_label.configure(text=f"Population: {population}")

                if "mediaLinks" in city_data and city_data["mediaLinks"]:
                    image_url = city_data["mediaLinks"][0]["href"]
                    image_response = requests.get(image_url)
                    image_data = Image.open(io.BytesIO(image_response.content))
                    image = ImageTk.PhotoImage(image_data)
                    logo_label.configure(image=image)
                    logo_label.image = image
                else:
                    logo_label.configure(image="")
                    logo_label.image = None
            else:
                population_label.configure(text="Population: inconnue")
                logo_label.configure(image="")
                logo_label.image = None

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
                forecast_label.configure(text=forecast_info)

                # Créer le graphique
                fig, ax = plt.subplots()
                ax.plot(dates, temperatures, marker='o')
                ax.set_title("Prévisions des températures")
                ax.set_xlabel("Date")
                ax.set_ylabel("Température (°C)")
                ax.grid(True)
                fig.autofmt_xdate()

                # Intégrer le graphique dans la fenêtre Tkinter
                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=10)

            else:
                forecast_label.configure(text="Prévisions indisponibles")
    else:
        ctk.CTkMessagebox.show_warning("Avertissement", "Veuillez entrer un nom de ville")

# Création de l'interface utilisateur
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Application Météo")

frame = ctk.CTkFrame(root)
frame.pack(pady=20)

city_label = ctk.CTkLabel(frame, text="Ville :")
city_label.grid(row=0, column=0, padx=10)

city_entry = ctk.CTkEntry(frame)
city_entry.grid(row=0, column=1, padx=10)

get_info_button = ctk.CTkButton(frame, text="Obtenir les informations", command=show_info)
get_info_button.grid(row=0, column=2, padx=10)

weather_label = ctk.CTkLabel(root, text="", font=("Helvetica", 14))
weather_label.pack(pady=10)

population_label = ctk.CTkLabel(root, text="", font=("Helvetica", 14))
population_label.pack(pady=10)

logo_label = ctk.CTkLabel(root, image=None)
logo_label.pack(pady=10)

forecast_label = ctk.CTkLabel(root, text="", font=("Helvetica", 14))
forecast_label.pack(pady=10)

root.mainloop()
