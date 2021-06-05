import os
import requests
import configparser
from datetime import datetime, time
from flask.globals import request
from flask import Flask, render_template



app = Flask(__name__)

@app.route('/')
def weatherMain():
    userCity = currentLocation()
    lon, lat, cityCode = getCityData(userCity)

    data = getWeatherReport(lat, lon)

    timezone = 7200
    time = int(data['current']['dt']) + timezone
    sunrise = int(data['current']['sunrise']) + timezone
    sunset = int(data['current']['sunset']) + timezone

    hour1 = int(data['hourly'][1]['dt']) + timezone
    hour2 = hour1 + 3600
    hour3 = hour2 + 3600
    hour4 = hour3 + 3600 
    hour5 = hour4 + 3600 
    hour6 = hour5 + 3600 
    day = hour6 + 3600 

    user_weather = {
        'city' : userCity.title(),
        'city_code' : cityCode,
        'current_icon' : data['current']['weather'][0]['icon'],
        'current_description' : data['current']['weather'][0]['description'].capitalize(),
        'current_temp' : round(data['current']['temp']),
        'current_temp_feel' : round(data['current']['feels_like']),
        'current_max_temp' : round(data['daily'][0]['temp']['max']),
        'current_min_temp' : round(data['daily'][0]['temp']['min']),
        'current_humidity' : data['current']['humidity'],
        'current_wind' : data['current']['wind_speed'],
        'current_date' : datetime.utcfromtimestamp(time).strftime('%A %e %B'),
        'current_sunrise' : datetime.utcfromtimestamp(sunrise).strftime('%H:%M'),
        'current_sunset' : datetime.utcfromtimestamp(sunset).strftime('%H:%M'),

        # hourly report
        'next_hours1' : datetime.utcfromtimestamp(hour1).strftime('%H:%M'),
        'next_hours_icon1' : data['hourly'][1]['weather'][0]['icon'],
        'next_hours_temp1' : round(data['hourly'][1]['temp']),

        'next_hours2' : datetime.utcfromtimestamp(hour2).strftime('%H:%M'),
        'next_hours_icon2' : data['hourly'][2]['weather'][0]['icon'],
        'next_hours_temp2' : round(data['hourly'][2]['temp']),

        'next_hours3' : datetime.utcfromtimestamp(hour3).strftime('%H:%M'),
        'next_hours_icon3' : data['hourly'][3]['weather'][0]['icon'],
        'next_hours_temp3' : round(data['hourly'][3]['temp']),

        'next_hours4' : datetime.utcfromtimestamp(hour4).strftime('%H:%M'),
        'next_hours_icon4' : data['hourly'][4]['weather'][0]['icon'],
        'next_hours_temp4' : round(data['hourly'][4]['temp']),

        'next_hours5' : datetime.utcfromtimestamp(hour5).strftime('%H:%M'),
        'next_hours_icon5' : data['hourly'][5]['weather'][0]['icon'],
        'next_hours_temp5' : round(data['hourly'][5]['temp']),

        'next_hours6' : datetime.utcfromtimestamp(hour6).strftime('%H:%M'),
        'next_hours_icon6' : data['hourly'][6]['weather'][0]['icon'],
        'next_hours_temp6' : round(data['hourly'][6]['temp']),

        'next_hours7' : datetime.utcfromtimestamp(day).strftime('%H:%M'),
        'next_hours_icon7' : data['hourly'][7]['weather'][0]['icon'],
        'next_hours_temp7' : round(data['hourly'][7]['temp'])
    }

    return render_template('home.html', user_weather = user_weather)

@app.route('/searchresult', methods=['POST'])
def searchResult():
    city = request.form['City']
    lon, lat, cityCode = getCityData(city)

    data = getWeatherReport(lat, lon)

    timezone = data['timezone_offset']
    time = data['current']['dt'] + timezone
    sunrise = data['current']['sunrise'] + timezone
    sunset = data['current']['sunset'] + timezone

    #next 7 hours
    hour1 = data['hourly'][1]['dt'] + timezone
    hour2 = hour1 + 3600    #3600 = 1hour in unix date format
    hour3 = hour2 + 3600
    hour4 = hour3 + 3600 
    hour5 = hour4 + 3600 
    hour6 = hour5 + 3600 
    day = hour6 + 3600 

    #next 5 days
    day1 = data['daily'][1]['dt'] + timezone
    day2 = day1 + 86400    #86400 = 1hour in unix date format
    day3 = day2 + 86400
    day4 = day3 + 86400
    day5 = day4 + 86400

    weather = {
        'city' : city.title(),
        'city_code' : cityCode,
        'current_icon' : data['current']['weather'][0]['icon'],
        'current_description' : data['current']['weather'][0]['description'].capitalize(),
        'current_temp' : round(data['current']['temp']),
        'current_temp_feel' : round(data['current']['feels_like']),
        'current_max_temp' : round(data['daily'][0]['temp']['max']),
        'current_min_temp' : round(data['daily'][0]['temp']['min']),
        'current_humidity' : data['current']['humidity'],
        'current_wind' : data['current']['wind_speed'],
        'current_date' : datetime.utcfromtimestamp(time).strftime('%A %e %B'),
        'current_sunrise' : datetime.utcfromtimestamp(sunrise).strftime('%H:%M'),
        'current_sunset' : datetime.utcfromtimestamp(sunset).strftime('%H:%M'),
        'current_cloudy' : data['current']['clouds'],
        'current_pressure' : data['current']['pressure'],

        # hourly report
        'next_hours1' : datetime.utcfromtimestamp(hour1).strftime('%H:%M'),
        'next_hours_icon1' : data['hourly'][1]['weather'][0]['icon'],
        'next_hours_temp1' : round(data['hourly'][1]['temp']),

        'next_hours2' : datetime.utcfromtimestamp(hour2).strftime('%H:%M'),
        'next_hours_icon2' : data['hourly'][2]['weather'][0]['icon'],
        'next_hours_temp2' : round(data['hourly'][2]['temp']),

        'next_hours3' : datetime.utcfromtimestamp(hour3).strftime('%H:%M'),
        'next_hours_icon3' : data['hourly'][3]['weather'][0]['icon'],
        'next_hours_temp3' : round(data['hourly'][3]['temp']),

        'next_hours4' : datetime.utcfromtimestamp(hour4).strftime('%H:%M'),
        'next_hours_icon4' : data['hourly'][4]['weather'][0]['icon'],
        'next_hours_temp4' : round(data['hourly'][4]['temp']),

        'next_hours5' : datetime.utcfromtimestamp(hour5).strftime('%H:%M'),
        'next_hours_icon5' : data['hourly'][5]['weather'][0]['icon'],
        'next_hours_temp5' : round(data['hourly'][5]['temp']),

        'next_hours6' : datetime.utcfromtimestamp(hour6).strftime('%H:%M'),
        'next_hours_icon6' : data['hourly'][6]['weather'][0]['icon'],
        'next_hours_temp6' : round(data['hourly'][6]['temp']),

        'next_hours7' : datetime.utcfromtimestamp(hour1).strftime('%H:%M'),
        'next_hours_icon7' : data['hourly'][7]['weather'][0]['icon'],
        'next_hours_temp7' : round(data['hourly'][7]['temp']),

        # daily report
        'next_weekday1' : datetime.utcfromtimestamp(day1).strftime('%a'),
        'next_day_month1' : datetime.utcfromtimestamp(day1).strftime('%e/%b'),
        'next_weekday1_icon1' : data['daily'][1]['weather'][0]['icon'],
        'next_weekday_max_temp1' : data['daily'][1]['temp']['max'],
        'next_weekday_min_temp1' : data['daily'][1]['temp']['min'],
        'next_weekday_humidity1' : data['daily'][1]['humidity'],
        'next_weekday_wind1' : data['daily'][1]['wind_speed'],

        'next_weekday2' : datetime.utcfromtimestamp(day2).strftime('%a'),
        'next_day_month2' : datetime.utcfromtimestamp(day2).strftime('%e/%b'),
        'next_weekday1_icon2' : data['daily'][2]['weather'][0]['icon'],
        'next_weekday_max_temp2' : data['daily'][2]['temp']['max'],
        'next_weekday_min_temp2' : data['daily'][2]['temp']['min'],
        'next_weekday_humidity2' : data['daily'][2]['humidity'],
        'next_weekday_wind2' : data['daily'][2]['wind_speed'],

        'next_weekday3' : datetime.utcfromtimestamp(day3).strftime('%a'),
        'next_day_month3' : datetime.utcfromtimestamp(day3).strftime('%e/%b'),
        'next_weekday1_icon3' : data['daily'][3]['weather'][0]['icon'],
        'next_weekday_max_temp3' : data['daily'][3]['temp']['max'],
        'next_weekday_min_temp3' : data['daily'][3]['temp']['min'],
        'next_weekday_humidity3' : data['daily'][3]['humidity'],
        'next_weekday_wind3' : data['daily'][3]['wind_speed'],

        'next_weekday4' : datetime.utcfromtimestamp(day4).strftime('%a'),
        'next_day_month4' : datetime.utcfromtimestamp(day4).strftime('%e/%b'),
        'next_weekday1_icon4' : data['daily'][4]['weather'][0]['icon'],
        'next_weekday_max_temp4' : data['daily'][4]['temp']['max'],
        'next_weekday_min_temp4' : data['daily'][4]['temp']['min'],
        'next_weekday_humidity4' : data['daily'][4]['humidity'],
        'next_weekday_wind4' : data['daily'][4]['wind_speed'],

        'next_weekday5' : datetime.utcfromtimestamp(day5).strftime('%a'),
        'next_day_month5' : datetime.utcfromtimestamp(day5).strftime('%e/%b'),
        'next_weekday1_icon5' : data['daily'][5]['weather'][0]['icon'],
        'next_weekday_max_temp5' : data['daily'][5]['temp']['max'],
        'next_weekday_min_temp5' : data['daily'][5]['temp']['min'],
        'next_weekday_humidity5' : data['daily'][5]['humidity'],
        'next_weekday_wind5' : data['daily'][5]['wind_speed']
    }

    return render_template('searchResult.html', weather=weather)

def getAPI():
    return '65eeeb0d5776ccbf4f9190c89311b810'

def getCityData(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city, getAPI())
    r = requests.get(url).json()
    lon = r['coord']['lon']
    lat = r['coord']['lat']
    cityCode = r['sys']['country']

    return lon, lat, cityCode;

def getWeatherReport(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,alerts&units=metric&appid={}'.format(lat, lon, getAPI())
    r = requests.get(url).json()
    return r

def currentLocation():
    url = 'http://ipinfo.io/json'
    r = requests.get(url).json()
    userCity = r['city']
    return userCity


if __name__ == '__main__':
    app.run()