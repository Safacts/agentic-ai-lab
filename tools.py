import requests
from langchain_core.tools import tool

CITY_COORDS = {
    "hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "delhi": {"lat": 28.6139, "lon": 77.2090},
    "mumbai": {"lat": 19.0760, "lon": 72.8777},
    "bangalore": {"lat": 12.9716, "lon": 77.5946},
    "chennai": {"lat": 13.0827, "lon": 80.2707},
    "new york": {"lat": 40.7128, "lon": -74.0060},
    "london": {"lat": 51.5074, "lon": -0.1278}
}

@tool
def get_weather(city_name: str):
    """
    Get the current weather for a specific city. 
    Input should be the name of the city (e.g., 'Hyderabad', 'Delhi').
    """
    city = city_name.lower().strip()
    if city not in CITY_COORDS:
        return f"Error: I don't know the coordinates for '{city_name}'. Try Hyderabad, Delhi, Mumbai, etc."
    
    coords = CITY_COORDS[city]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,humidity_2m,wind_speed_10m"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        current = data['current']
        return (f"Weather in {city_name.title()}:\n"
                f"- Temperature: {current['temperature_2m']}°C\n"
                f"- Wind Speed: {current['wind_speed_10m']} km/h\n"
                f"- Humidity: {current['humidity_2m']}%")
    except Exception as e:
        return f"API Connection Failed: {e}"

available_tools = [get_weather]