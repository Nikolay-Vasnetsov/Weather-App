from flask import Flask, render_template, request, redirect, flash
import sys
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '48yrfhefhi3ed33'
db = SQLAlchemy(app)


class city_table(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    weather = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return {"name": self.name, "temp": self.temp, "weather": self.weather, "id": self.id}
        # f"{self.name} {self.temp} {self.weather} {self.id}"
        # {"name": self.name, "temp": self.temp, "weather": self.weather, "id": self.id}


db.create_all()


def get_api_key():
    return "e28dface6dd078088c6bd152eb747d19"


def get_weather_result(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    r = requests.post(url)
    return r.json()


@app.route('/')
def index():
    list_of_cities = city_table.query.all()
    return render_template("index.html", list_of_cities=list_of_cities)


@app.route('/add', methods=['POST'])
def add_city():
    city_name = request.form["city"]
    api_key = get_api_key()
    data = get_weather_result(city_name, api_key)
    if data["cod"] == "400" or data["cod"] == "404":
        flash("The city doesn't exist!")
    else:
        data_from_db = city_table.query.all()
        i = 0
        for _ in data_from_db:
            if city_name == data_from_db[i].name:
                flash("The city has already been added to the list!")
                break
            i += 1
        else:
            temp = round(data["main"]["temp"])
            sky = data["weather"][0]["main"]
            info = city_table(name=city_name, temp=temp, weather=sky)
            db.session.add(info)
            db.session.commit()
    return redirect('/')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    city_id = request.form["id"]
    _city = city_table.query.filter_by(id=city_id).first()
    db.session.delete(_city)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
