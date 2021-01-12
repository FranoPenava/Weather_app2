import requests
from flask import Flask, render_template, request, redirect, url_for
from configparser import ConfigParser

# Application works for all the correct typed cities!

app = Flask(__name__)

# Returns home html where city_name should be provided for completing the action!
@app.route("/")
def home():
    return render_template("home.html")


# Main function returns values for the city name you provided! 
@app.route("/city", methods = ["POST"])
def city():
    # Getting the city name you provided!
    city_name = request.form.get("city_name")
    # Accessing my api!
    api_key = get_api()
    # Geting the data with function I created later!
    data = get_data(city_name, api_key)
    
    # Accessing specific data from json!
    weather = data["weather"][0]["main"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]

    # Adding data to index.html so that you can see it!
    return render_template("index.html", weather = weather, temp = temp, feels_like = feels_like, city = city_name)



@app.route("/return_back", methods = ["GET"])
def return_back():
    return redirect(url_for("home"))


# Function that returns my api
def get_api():
    config = ConfigParser()
    config.read("config.ini")
    return config['openweathermap']['api']

# Function that is used for getting all the data for the city you provided!
def get_data(city_name, api_key):
    link = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
    
    content = requests.get(link).json()
    
    return content


if __name__ == "__main__":
    app.run(debug=True)