import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import datetime
import os
import pytz
from datetime import timezone

def get_city_id(api_key, city_name):
    api_url = "http://api.openweathermap.org/data/2.5/find"
    params = {
        "q": city_name,
        "appid": api_key
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['count'] > 0:
            return data['list'][0]['id']
        else:
            messagebox.showerror("Error", "City not found.")
            return None
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    return None

def get_weather_data(api_key, city_id):
    api_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "id": city_id,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    return None

def get_air_quality_data(api_key, lat, lon):
    api_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    return None

def get_uv_index_data(api_key, lat, lon):
    api_url = "http://api.openweathermap.org/data/2.5/uvi"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    return None


def display_weather_data(data, air_quality_data, uv_index_data):
    if data:
        city_name = data['city']['name']
        timezone_offset = data['city']['timezone']  # Timezone offset in seconds
        
        # Get current UTC time
        utc_now = datetime.datetime.now(datetime.UTC)
        
        # Calculate local time using the timezone offset
        city_time = utc_now + datetime.timedelta(seconds=timezone_offset)
        local_time_str = city_time.strftime('%Y-%m-%d %H:%M:%S')

        weather_info = f"City: {city_name}\n"
        weather_info += f"Current Local Time: {local_time_str}\n"
        weather_info += f"Temperature (Celsius): {data['list'][0]['main']['temp']}°C\n"
        weather_info += f"Temperature (Fahrenheit): {(data['list'][0]['main']['temp'] * 9/5) + 32}°F\n"
        weather_info += f"Humidity: {data['list'][0]['main']['humidity']}%\n"
        weather_info += f"Pressure: {data['list'][0]['main']['pressure']} hPa\n"
        weather_info += f"Wind Speed: {data['list'][0]['wind']['speed']} m/s\n"
        weather_info += f"Weather: {data['list'][0]['weather'][0]['description'].capitalize()}\n"

        high_temp = data['list'][0]['main']['temp']
        low_temp = data['list'][0]['main']['temp']

        for item in data['list']:
            if item['main']['temp'] > high_temp:
                high_temp = item['main']['temp']
            if item['main']['temp'] < low_temp:
                low_temp = item['main']['temp']

        weather_info += f"High: {high_temp}°C / {(high_temp * 9/5) + 32}°F\n"
        weather_info += f"Low: {low_temp}°C / {(low_temp * 9/5) + 32}°F\n"
        
        sunrise = datetime.datetime.fromtimestamp(data['city']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.datetime.fromtimestamp(data['city']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
        weather_info += f"Sunrise: {sunrise}\n"
        weather_info += f"Sunset: {sunset}\n"
        
        weather_info += f"UV Index: {uv_index_data['value']}\n"
        weather_info += f"Air Quality Index: {air_quality_data['list'][0]['main']['aqi']}\n"
        
        weather_label.config(text=weather_info)
        
        # Display weather icon
        icon_code = data['list'][0]['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, stream=True)
        icon_image = Image.open(icon_response.raw)
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
  

    else:
        weather_label.config(text="Failed to retrieve weather data.")

def search_weather():
    city_name = city_entry.get()
    if city_name:
        city_id = get_city_id(api_key, city_name)
        if city_id:
            weather_data = get_weather_data(api_key, city_id)
            if weather_data:
                lat = weather_data['city']['coord']['lat']
                lon = weather_data['city']['coord']['lon']
                air_quality_data = get_air_quality_data(api_key, lat, lon)
                uv_index_data = get_uv_index_data(api_key, lat, lon)
                display_weather_data(weather_data, air_quality_data, uv_index_data)

# API Key for OpenWeatherMap
api_key = "Your_api_key"  #Replace with your api_key

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Load background image
bg_image = Image.open("Background_image.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to place the background image
canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create and place the city entry widget in the middle
city_entry = tk.Entry(root, width=50, font=("Helvetica", 14))
city_entry.insert(0, "Enter city name: {Rajkot, Gondal, etc..}")
city_entry.config(fg="gray")



def clear_placeholder(event):
    if city_entry.cget("fg") == "gray":
        city_entry.delete(0, "end")
        city_entry.config(fg="black")

city_entry.bind("<FocusIn>", clear_placeholder)

canvas.create_window(bg_image.width // 2, bg_image.height // 8, window=city_entry)

# Create and place the search button below the city entry
search_button = tk.Button(root, text="Search", command=search_weather, font=("Helvetica", 14))
canvas.create_window(bg_image.width // 2, bg_image.height // 8 + 50, window=search_button)

# Create and place the weather information label in the middle
weather_label = tk.Label(root, text="", justify="left", anchor="w", bg="white", font=("Helvetica", 12))
canvas.create_window(bg_image.width // 2, bg_image.height // 4 + 135, window=weather_label)

# Create and place the weather icon label below the weather information
icon_label = tk.Label(root, bg="white")
canvas.create_window(bg_image.width // 2, bg_image.height // 2 +185 , window=icon_label)

# Run the main loop
root.mainloop()





