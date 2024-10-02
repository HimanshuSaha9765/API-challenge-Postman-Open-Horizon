import tkinter as tk  # Import the tkinter library for creating GUI applications
from tkinter import messagebox  # Import the messagebox module for displaying message boxes
from PIL import Image, ImageTk  # Import the Image and ImageTk modules from the PIL library for handling images
import requests  # Import the requests library for making HTTP requests
import datetime  # Import the datetime module for handling date and time
import os  # Import the os module for interacting with the operating system
import pytz  # Import the pytz library for handling time zones
from datetime import timezone  # Import the timezone class from the datetime module

def get_city_id(api_key, city_name):
    # Function to get the city ID from the OpenWeatherMap API using the city name
    api_url = "http://api.openweathermap.org/data/2.5/find"  # API endpoint for finding city ID
    params = {
        "q": city_name,  # City name parameter
        "appid": api_key  # API key parameter
    }
    try:
        response = requests.get(api_url, params=params)  # Make a GET request to the API
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()  # Parse the JSON response
        if data['count'] > 0:  # Check if any cities were found
            return data['list'][0]['id']  # Return the ID of the first city in the list
        else:
            messagebox.showerror("Error", "City not found.")  # Show an error message if no cities were found
            return None  # Return None if no cities were found
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")  # Show an error message for HTTP errors
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")  # Show an error message for other exceptions
    return None  # Return None if an exception occurred

def get_weather_data(api_key, city_id):
    # Function to get the weather data from the OpenWeatherMap API using the city ID
    api_url = "http://api.openweathermap.org/data/2.5/forecast"  # API endpoint for weather forecast
    params = {
        "id": city_id,  # City ID parameter
        "appid": api_key,  # API key parameter
        "units": "metric"  # Units parameter (metric)
    }
    try:
        response = requests.get(api_url, params=params)  # Make a GET request to the API
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()  # Parse the JSON response
        return data  # Return the weather data
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")  # Show an error message for HTTP errors
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")  # Show an error message for other exceptions
    return None  # Return None if an exception occurred

def get_air_quality_data(api_key, lat, lon):
    # Function to get the air quality data from the OpenWeatherMap API using latitude and longitude
    api_url = "http://api.openweathermap.org/data/2.5/air_pollution"  # API endpoint for air pollution data
    params = {
        "lat": lat,  # Latitude parameter
        "lon": lon,  # Longitude parameter
        "appid": api_key  # API key parameter
    }
    try:
        response = requests.get(api_url, params=params)  # Make a GET request to the API
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()  # Parse the JSON response
        return data  # Return the air quality data
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")  # Show an error message for HTTP errors
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")  # Show an error message for other exceptions
    return None  # Return None if an exception occurred

def get_uv_index_data(api_key, lat, lon):
    # Function to get the UV index data from the OpenWeatherMap API using latitude and longitude
    api_url = "http://api.openweathermap.org/data/2.5/uvi"  # API endpoint for UV index data
    params = {
        "lat": lat,  # Latitude parameter
        "lon": lon,  # Longitude parameter
        "appid": api_key  # API key parameter
    }
    try:
        response = requests.get(api_url, params=params)  # Make a GET request to the API
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()  # Parse the JSON response
        return data  # Return the UV index data
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")  # Show an error message for HTTP errors
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")  # Show an error message for other exceptions
    return None  # Return None if an exception occurred

def display_weather_data(data, air_quality_data, uv_index_data):
    # Function to display the weather data, air quality data, and UV index data in the GUI
    if data:
        city_name = data['city']['name']  # Get the city name from the weather data
        timezone_offset = data['city']['timezone']  # Get the timezone offset in seconds
        
        # Get current UTC time
        utc_now = datetime.datetime.now(datetime.UTC)  # Get the current UTC time
        
        # Calculate local time using the timezone offset
        city_time = utc_now + datetime.timedelta(seconds=timezone_offset)  # Calculate the local time
        local_time_str = city_time.strftime('%Y-%m-%d %H:%M:%S')  # Format the local time as a string

        weather_info = f"City: {city_name}\n"  # Create a string with the city name
        weather_info += f"Current Local Time: {local_time_str}\n"  # Add the local time to the string
        weather_info += f"Temperature (Celsius): {data['list'][0]['main']['temp']}°C\n"  # Add the temperature in Celsius to the string
        weather_info += f"Temperature (Fahrenheit): {(data['list'][0]['main']['temp'] * 9/5) + 32}°F\n"  # Add the temperature in Fahrenheit to the string
        weather_info += f"Humidity: {data['list'][0]['main']['humidity']}%\n"  # Add the humidity to the string
        weather_info += f"Pressure: {data['list'][0]['main']['pressure']} hPa\n"  # Add the pressure to the string
        weather_info += f"Wind Speed: {data['list'][0]['wind']['speed']} m/s\n"  # Add the wind speed to the string
        weather_info += f"Weather: {data['list'][0]['weather'][0]['description'].capitalize()}\n"  # Add the weather description to the string

        high_temp = data['list'][0]['main']['temp']  # Initialize the high temperature
        low_temp = data['list'][0]['main']['temp']  # Initialize the low temperature

        for item in data['list']:  # Iterate through the weather data
            if item['main']['temp'] > high_temp:  # Check if the temperature is higher than the current high temperature
                high_temp = item['main']['temp']  # Update the high temperature
            if item['main']['temp'] < low_temp:  # Check if the temperature is lower than the current low temperature
                low_temp = item['main']['temp']  # Update the low temperature

        weather_info += f"High: {high_temp}°C / {(high_temp * 9/5) + 32}°F\n"  # Add the high temperature to the string
        weather_info += f"Low: {low_temp}°C / {(low_temp * 9/5) + 32}°F\n"  # Add the low temperature to the string
        
        sunrise = datetime.datetime.fromtimestamp(data['city']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')  # Get the sunrise time and format it as a string
        sunset = datetime.datetime.fromtimestamp(data['city']['sunset']).strftime('%Y-%m-%d %H:%M:%S')  # Get the sunset time and format it as a string
        weather_info += f"Sunrise: {sunrise}\n"  # Add the sunrise time to the string
        weather_info += f"Sunset: {sunset}\n"  # Add the sunset time to the string
        
        weather_info += f"UV Index: {uv_index_data['value']}\n"  # Add the UV index to the string
        weather_info += f"Air Quality Index: {air_quality_data['list'][0]['main']['aqi']}\n"  # Add the air quality index to the string
        
        weather_label.config(text=weather_info)  # Update the weather label with the weather information
        
        # Display weather icon
        icon_code = data['list'][0]['weather'][0]['icon']  # Get the weather icon code
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"  # Create the URL for the weather icon
        icon_response = requests.get(icon_url, stream=True)  # Make a GET request to get the weather icon
        icon_image = Image.open(icon_response.raw)  # Open the weather icon image
        icon_photo = ImageTk.PhotoImage(icon_image)  # Convert the image to a PhotoImage
        icon_label.config(image=icon_photo)  # Update the icon label with the weather icon
        icon_label.image = icon_photo  # Keep a reference to the image to prevent garbage collection
    else:
        weather_label.config(text="Failed to retrieve weather data.")  # Update the weather label if data retrieval failed

def search_weather():
    # Function to search for weather data based on the city name entered by the user
    city_name = city_entry.get()  # Get the city name from the entry widget
    if city_name:  # Check if the city name is not empty
        city_id = get_city_id(api_key, city_name)  # Get the city ID using the city name
        if city_id:  # Check if the city ID was found
            weather_data = get_weather_data(api_key, city_id)  # Get the weather data using the city ID
            if weather_data:  # Check if the weather data was retrieved
                lat = weather_data['city']['coord']['lat']  # Get the latitude from the weather data
                lon = weather_data['city']['coord']['lon']  # Get the longitude from the weather data
                air_quality_data = get_air_quality_data(api_key, lat, lon)  # Get the air quality data using the latitude and longitude
                uv_index_data = get_uv_index_data(api_key, lat, lon)  # Get the UV index data using the latitude and longitude
                display_weather_data(weather_data, air_quality_data, uv_index_data)  # Display the weather data, air quality data, and UV index data

# API Key for OpenWeatherMap
api_key = "Your_api_key"  # Your OpenWeatherMap API key

# Create the main window
root = tk.Tk()  # Create the main window
root.title("Weather App")  # Set the title of the main window

# Load background image
bg_image = Image.open("background1.jpg")  # Open the background image
bg_photo = ImageTk.PhotoImage(bg_image)  # Convert the background image to a PhotoImage

# Create a canvas to place the background image
canvas = tk.Canvas(root, width=bg_image.width, height=bg_image.height)  # Create a canvas with the same size as the background image
canvas.pack(fill="both", expand=True)  # Pack the canvas to fill the window and allow it to expand
canvas.create_image(0, 0, image=bg_photo, anchor="nw")  # Place the background image on the canvas

# Create and place the city entry widget in the middle
city_entry = tk.Entry(root, width=50, font=("Helvetica", 14))  # Create an entry widget for the city name
city_entry.insert(0, "Enter city name: {Rajkot, Gondal, etc..}")  # Insert placeholder text into the entry widget
city_entry.config(fg="gray")  # Set the text color to gray

def clear_placeholder(event):
    # Function to clear the placeholder text when the entry widget is focused
    if city_entry.cget("fg") == "gray":  # Check if the text color is gray
        city_entry.delete(0, "end")  # Delete the placeholder text
        city_entry.config(fg="black")  # Set the text color to black

city_entry.bind("<FocusIn>", clear_placeholder)  # Bind the clear_placeholder function to the FocusIn event

canvas.create_window(bg_image.width // 2, bg_image.height // 8, window=city_entry)  # Place the entry widget on the canvas

# Create and place the search button below the city entry
search_button = tk.Button(root, text="Search", command=search_weather, font=("Helvetica", 14))  # Create a search button
canvas.create_window(bg_image.width // 2, bg_image.height // 8 + 50, window=search_button)  # Place the search button on the canvas

# Create and place the weather information label in the middle
weather_label = tk.Label(root, text="", justify="left", anchor="w", bg="white", font=("Helvetica", 12))  # Create a label for the weather information
canvas.create_window(bg_image.width // 2, bg_image.height // 4 + 135, window=weather_label)  # Place the weather information label on the canvas

# Create and place the weather icon label below the weather information
icon_label = tk.Label(root, bg="white")  # Create a label for the weather icon
canvas.create_window(bg_image.width // 2, bg_image.height // 2 + 185, window=icon_label)  # Place the weather icon label on the canvas

# Run the main loop
root.mainloop()  # Start the main loop to run the application
