from flask import Flask,render_template,url_for, jsonify
import pandas
import plotly
import plotly.graph_objects as go
import AWS_connector
import weather
from requests import get
app = Flask(__name__)

# ---------------------- Primary User Interface --------------------------
@app.route('/')
def index():    
    linegraph = AWS_connector.grab_graph()
    result_of_values = AWS_connector.values()
    recent_temperature = result_of_values[0]
    #recent_humidity = result_of_values[1]    
    x = weather.getWeatherData(weather.response)
    value_of_temperature = int(x[0])
    value_of_humidity = int(x[1])  
    value_of_pressure = int(x[2])
    description_of_weather = x[3]
    current_town = x[4]
    current_country = x[5]
    current_weather_icon = x[6]
    if recent_temperature > 95:
        return render_template("html/index.html",plot = linegraph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon, countt = 1 , recent_temp_value = recent_temperature)
    else:
        return render_template("html/index.html",plot = linegraph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon)


@app.route('/table-view', methods=("POST", "GET")) # Pandas Table view of the cleaned data.
def html_table():
    df = AWS_connector.get_table_view()
    result_of_values = AWS_connector.values()
    recent_temperature = result_of_values[0]
    #recent_humidity = result_of_values[1]    
    x = weather.getWeatherData(weather.response)
    value_of_temperature = int(x[0])
    value_of_humidity = int(x[1])  
    value_of_pressure = int(x[2])
    description_of_weather = x[3]
    current_town = x[4]
    current_country = x[5]
    current_weather_icon = x[6]
    if recent_temperature > 95:
        return render_template('html/table_view.html',  tables=[df.to_html(classes='data')], titles=df.columns.values, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon, countt = 1 , recent_temp_value = recent_temperature)
    else:
        return render_template('html/table_view.html',  tables=[df.to_html(classes='data')], titles=df.columns.values, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon)


@app.route('/humidity', methods=("POST","GET"))
def h_graph():
    graph = AWS_connector.grab_graph('humidity') #temp is default
    result_of_values = AWS_connector.values()
    recent_temperature = result_of_values[0]
    #recent_humidity = result_of_values[1]    
    x = weather.getWeatherData(weather.response)
    value_of_temperature = int(x[0])
    value_of_humidity = int(x[1])  
    value_of_pressure = int(x[2])
    description_of_weather = x[3]
    current_town = x[4]
    current_country = x[5]
    current_weather_icon = x[6]
    if recent_temperature > 95:
        return render_template("html/humidity_graph.html",plot = graph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon, countt = 1 , recent_temp_value = recent_temperature)
    else:
        return render_template("html/humidity_graph.html",plot = graph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon)


@app.route('/pressure', methods=("POST","GET"))
def press_graph():
    graph = AWS_connector.grab_graph('pressure') #temp is default
    result_of_values = AWS_connector.values()
    recent_temperature = result_of_values[0]
    #recent_humidity = result_of_values[1]    
    x = weather.getWeatherData(weather.response)
    value_of_temperature = int(x[0])
    value_of_humidity = int(x[1])  
    value_of_pressure = int(x[2])
    description_of_weather = x[3]
    current_town = x[4]
    current_country = x[5]
    current_weather_icon = x[6]
    if recent_temperature > 95:
        return render_template("html/pressure_graph.html",plot = graph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon, countt = 1 , recent_temp_value = recent_temperature)
    else:
        return render_template("html/pressure_graph.html",plot = graph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon)


@app.route('/particulate', methods=("POST","GET"))
def part_graph():
    graph = AWS_connector.grab_graph('particulate') #temp is default
    result_of_values = AWS_connector.values()
    recent_temperature = result_of_values[0]
    #recent_humidity = result_of_values[1]    
    x = weather.getWeatherData(weather.response)
    value_of_temperature = int(x[0])
    value_of_humidity = int(x[1])  
    value_of_pressure = int(x[2])
    description_of_weather = x[3]
    current_town = x[4]
    current_country = x[5]
    current_weather_icon = x[6]
    if recent_temperature > 95:
        return render_template("html/particulate_graph.html",plot = graph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon, countt = 1 , recent_temp_value = recent_temperature)
    else:
        return render_template("html/particulate_graph.html",plot = graph, temp_value = value_of_temperature, humidity_value = value_of_humidity, pressure_value = value_of_pressure, weather_description = description_of_weather, town_value = current_town, country_value = current_country,icon_value = current_weather_icon)


# ----------------------- Main ----------------------
if __name__ == "__main__":
    app.run(debug=True)
    