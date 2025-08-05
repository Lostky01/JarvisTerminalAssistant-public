import requests

DEFAULT_CITY = ""  # Your City E.G New York, ETC  

def get_weather(city=DEFAULT_CITY):
    try:
        res = requests.get(
            "http://api.weatherapi.com/v1/current.json",
            params={
                "key": "YOUR_KEY_HERE",
                "q": city,
                "aqi": "no"
            }
        )
        res.raise_for_status()
        data = res.json()
        condition = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
        feels_like = data["current"]["feelslike_c"]
        humidity = data["current"]["humidity"]
        wind = data["current"]["wind_kph"]
        return (
            f"The current weather in {city} is {condition.lower()} with a temperature of {temp}°C, "
            f"feels like {feels_like}°C. Humidity is at {humidity}%, and wind speed is {wind} km/h."
        )
    except Exception as e:
        print("✖️ WeatherAPI error:", e)
        return "I tried fetching the weather, but WeatherAPI just ghosted me. Probably drunk on cloud fumes."
