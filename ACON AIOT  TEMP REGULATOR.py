import requests                       #pip install requests

# API key for OpenWeatherMap
API_KEY = "56ac9609d73cd3406b671921ef9521c1"

# The current location's latitude and longitude from the GPS sensor
latitude = 28.4595
longitude = 77.0266

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=minutely&appid={API_KEY}"
api_data = requests.get(url).json()

# The current temperature and humidity from the API response
temp = [int(api_data["current"]["temp"]) - 273.15, int(api_data["hourly"][0]["temp"]) - 273.15]
hum = [int(api_data["current"]["humidity"]), int(api_data["hourly"][0]["humidity"])]

# The current temperature and humidity from the hardware sensors
current_temp_accord = int(input("Temperature(from sensor):")) 
current_hum_accord =  int(input("Humidity(From sensor):")) 

diff = [(temp[0] - current_temp_accord) / 2, (hum[0] - current_hum_accord) / 2]

temp_s = (temp[0] * 0.2 + temp[1] * 0.1 + current_temp_accord * 0.7) 
hum_s = (hum[0] * 0.2 + hum[1] * 0.1 + current_hum_accord * 0.7)

# Weather description from the API response
main_des = api_data["current"]["weather"][0]["main"]

# Set the ideal temperature and humidity based on the weather description
if (main_des == "Thunderstorm" or main_des == "Drizzle" or main_des == "Rain"):
    ideal_t = 24
    ideal_h = 30
elif (main_des == "Snow"):
    ideal_t = 20
    ideal_h = 70
elif (main_des == "Clear" or main_des == "Clouds"):
    ideal_t = 26
    ideal_h = 30
else:
    ideal_t = 24
    ideal_h = 30

# Calculate the required temperature and humidity
req_temp = (ideal_t * 3 + temp_s) /4
req_hum = (ideal_h * 3 + hum_s) / 4

print(f"Set temperature to {round(req_temp+diff[0])}°C")
32
# Determining the AC mode based on the required temperature and humidity
req_hum +=diff[1]
if (req_hum < hum_s):
    if (req_temp > temp_s):
        mode = "dry"
    else:
        mode = "cool"
else:
    if (req_temp > temp_s):
        mode = "fan"
    else:
        mode = "cool"

print(f"Set Mode of AC to {mode}")