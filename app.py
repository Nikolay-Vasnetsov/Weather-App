from flask import Flask, render_template, request, url_for, redirect
import sys
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class city(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    weather = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return {"name": self.name, "temp": self.temp, "weather": self.weather}
db.create_all()


def get_api_key():
    return "e28dface6dd078088c6bd152eb747d19"


def get_weather_result(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    r = requests.post(url)
    return r.json()


@app.route('/')
def index():
    list_of_cities = city.query.all()
    return render_template("index.html", list_of_cities=list_of_cities)


@app.route('/add', methods=['POST'])
def add_city():
    api_key = get_api_key()
    city_name = request.form["city"]
    data = get_weather_result(city_name, api_key)
    temp = round(data["main"]["temp"])
    sky = data["weather"][0]["main"]
    info = city(name=city_name, temp=temp, weather=sky)
    db.session.add(info)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
