from django.shortcuts import render, redirect
import json
import urllib.request
from datetime import datetime
from django.contrib import messages


# Create your views here.

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        city = city.replace(' ', '%20')

        try:
            res = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q="+city+"&APPID=18ebbd6b51735bc746ed959476a398d7").read()
            
            json_data = json.loads(res)

        except urllib.error.HTTPError:
            messages.warning(request, 'Not Found')
            return redirect("/")



        cur_date = getDate()
        data = {
            "country_code" : str(json_data['sys']['country']),
            "coordinate" : str(json_data['coord']['lon']) + ' ' +
            str(json_data['coord']['lat']),
            "temp" : str(round((json_data['main']['temp']) - 273.15)),
            "pressure" : str(json_data['main']['pressure']),
            "humidity" : str(json_data['main']['humidity'],),
            "wind_speed" : str(json_data['wind']['speed']),
            "description" : str(json_data['weather'][0]['description']),
            "weather_icon" : json_data['weather'][0]['icon']
            
        }

        lon = str(json_data['coord']['lon'])
        lat = str(json_data['coord']['lat'])

        daily_forcast = getFiveDayForcast(lon, lat)
        
    else:
        daily_forcast = []
        cur_date = ""
        city = ""
        data = {}

    city = city.replace('%20', ' ')
    city = city.split(',',1)[0]
    return render(request, 'index.html', {'data' : data, 'city' : city, 'cur_date' : cur_date, 'daily_forcast' : daily_forcast})

def getDate():
    dt = datetime.now()

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    cur_month = months[dt.month - 1]
    cur_day = days[dt.isoweekday() - 1]  
    current_time = dt.strftime("%I:%M")
    # print(current_time)

    complete_date = [cur_day+',', cur_month, current_time]
    real_date = ' '.join(complete_date)
    return real_date

def getFiveDayForcast(lon, lat):
    res = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?lat="+lat+"&lon="+lon+"&appid=18ebbd6b51735bc746ed959476a398d7").read() 
    json_data = json.loads(res)
    #print(json_data)

    
    daily_forcast = []
    num = 1
    for data in json_data['list'][::8]:
        daily_forcast.append({
            "dt" : data['dt'],
            "day" : datetime.fromtimestamp(data['dt']).strftime("%A"),
            "weather_icon" : data['weather'][0]['icon'],
            "temp" : str(round((data['main']['temp']) - 273.15)),
            "max_temp" : round(data['main']["temp_max"]) - 273.15
        })

        
    # print(daily_forcast)
    return daily_forcast


    

