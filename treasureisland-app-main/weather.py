from requests import get

#######################################
#get weather data from openweathermap
#######################################

def getWeatherResponse():   
    try:
        ip = '207.180.167.194'

        latlong = get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')

        weather = get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=fb008fbe7e419329e7243ea4a640f4e9'.format(latlong[0], latlong[1])).json()
        return weather

    except Exception as e:
        print("Couldn't get the weather info")

    try:
        ip = '207.180.167.194'

        latlong = get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')

        weather = get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=36d7c29ad0ad8c8876406503ad039630'.format(latlong[0], latlong[1])).json()
        return weather

    except Exception as e:
        print("Couldn't get the weather info")
    
    try:
        ip = '207.180.167.194'

        latlong = get('https://ipapi.co/{}/latlong/'.format(ip)).text.split(',')

        weather = get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=4a0e392106ce16a6fd93a7738c301353'.format(latlong[0], latlong[1])).json()
        return weather

    except Exception as e:
        print("Couldn't get the weather info")

#########################################################
#function to convert from kevin to fahrenheit
#########################################################
def kevinToFahrenheit(kevin):    
    try:
        kevin = float(kevin)
        fahrenheit = 1.8*(kevin - 273.15) + 32
        return round(fahrenheit,1)

    except Exception as e :        
        return "cannot convert to fahrenheit"

response = getWeatherResponse()
# WeatherData_jsonObject = getWeatherResponse()

def getWeatherData(response):
    try:
        temperature = kevinToFahrenheit(response['main']['temp'])
        humidity = response['main']['humidity']
        pressure = response['main']['pressure']
        weather_condition = response['weather'][0]['description']
        name_of_city = response['name']
        name_of_country = response['sys']['country']
        weather_icon = 'https://openweathermap.org/img/w/'+response['weather'][0]['icon']+'.png'
        return [temperature, humidity, pressure,weather_condition, name_of_city, name_of_country,weather_icon]
    except:
        print("cannot process data from json object")

