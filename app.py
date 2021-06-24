from flask import Flask, render_template, request
import sys
import requests

app = Flask(__name__)


def get_api_key():
    return "e28dface6dd078088c6bd152eb747d19"


def get_weather_result(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    r = requests.post(url)
    return r.json()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_city():
    city_name = request.form["city"]
    api_key = get_api_key()
    data = get_weather_result(city_name, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    location = data["name"]
    sky = data["weather"][0]["main"]
    return render_template("add.html", temp=temp, location=location, sky=sky)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
