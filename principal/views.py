from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.core.cache import cache

from principal.models import TemperatureActuelle, TemperatureLac

import matplotlib as pl
pl.use('Agg')
import matplotlib.pyplot as plt

from matplotlib import pylab
from pylab import *

from datetime import datetime
import sched, time
import random
import json
import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import os, os.path

number_of_photo = len([name for name in os.listdir('./static/wallpaper')])
timeout_grand_lac=55

s = sched.scheduler(time.time, time.sleep)
bourget_weather_json_url = "http://api.wunderground.com/api/0c8d8fcc4a61d260/conditions/q/FR/Le_Bourget_Du_Lac.json"

# Create your views here.

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
    """)


def date_actuelle(request):
    # return render(request, 'principal/date.html', {'date': datetime.now()})
    nb_rand = random.randrange(1, number_of_photo)
    image_name = 'wallpaper/' + str(nb_rand) + '.jpg'
    date_derniere_temperature = TemperatureActuelle.objects.last().date_ajout
    print(f'now : {datetime.now()}')
    print(f'photo : {nb_rand}.jpg')
    print(f'django : {date_derniere_temperature.replace(tzinfo=None)}')
    duree = datetime.now() - date_derniere_temperature.replace(tzinfo=None)
    print(f'duree : {duree.seconds}')
    actual_weather = weather()
    weather_condition = actual_weather.get('condition')
    weather_temperature = actual_weather.get('temperature')
    if  duree.seconds > 10800:
        try:
            temperature_lac = temperature_lac_bourget()
            temperature_lac_enregistre = TemperatureLac(degres=temperature_lac)
            temperature_lac_enregistre.save()
            temperature_enregistre = TemperatureActuelle(degres=weather_temperature)
            temperature_enregistre.save()
        except:
            temperature_lac = "Grand Lac KO"
        return render(request, 'principal/date.html', {
            'nb_rand': nb_rand,
            'image_name': image_name,
            'weather_condition': weather_condition,
            'weather_temperature': weather_temperature,
            'temperature_lac': temperature_lac,
        })
    else:
        return render(request, 'principal/date.html', {
            'nb_rand': nb_rand,
            'image_name': image_name,
            'weather_condition': weather_condition,
            'weather_temperature': weather_temperature,
            'temperature_lac': TemperatureLac.objects.last().degres,
        })


def weather():
    # global weather_cache
    # if weather_cache is None or time.time() > weather_cache[1]:
    try:
        with urllib.request.urlopen(bourget_weather_json_url, timeout=60) as stream:
            jsonstr = stream.read()

            # Parse data and build result
            root = json.loads(jsonstr.decode('utf-8'))
            result = {
            "location" : root["current_observation"]["display_location"]["city"],
            "condition" : root["current_observation"]["icon"],
            "temperature" : root["current_observation"]["temp_c"],
            }
            # if 18 < datetime.now().hour:
            # 	result[name] = s

            # Expiration and caching
            now = time.time()
            expire = ((now - 3*60) // 3600 + 1) * 3600 + 3*60  # 3 minutes past the next hour
            expire = min(now + 20 * 60, expire)  # Or 20 minutes, whichever is earlier
            weather_cache = (result, expire)
            return result
    except:
        return -1



def temperature_lac_bourget():
    page_link ='http://www.grand-lac.fr/meteo/'
    # fetch the content from url
    page_response = requests.get(page_link, timeout=timeout_grand_lac)
    # parse html
    page_content = BeautifulSoup(page_response.content, "html.parser")

    # extract all html elements where price is stored
    liste_page = page_content.find(class_="table")

    # liste_page_2 = str(liste_page).split('<td>', )
    liste_page_2 = re.split("<td>|</td>", str(liste_page))

    prochain = 0
    for item in liste_page_2:
        if prochain == 2:
            temperature_lac = float(item[:-3])
            print(temperature_lac)
            return temperature_lac
            break
        if prochain == 1:
            prochain = 2
        if item == "Température de l'eau":
            print(item)
            prochain = 1


def graph_lac(request):
    # return render(request, 'principal/date.html', {'date': datetime.now()})
    nb_rand = random.randrange(1, number_of_photo)
    image_name = 'wallpaper/' + str(nb_rand) + '.jpg'
    actual_weather = weather()
    # temperature_lac = temperature_lac_bourget()
    weather_condition = actual_weather.get('condition')
    weather_temperature = actual_weather.get('temperature')
    getimage(TemperatureLac.objects.all())
    return render(request, 'principal/graph.html', {
        'nb_rand': nb_rand,
        'image_name': image_name,
        'weather_condition': weather_condition,
        'weather_temperature': weather_temperature,
        # 'imgsrc': imgsrc,
        'date': datetime.now(),
        'Titre': 'Lac',
    })

def graph_air(request):
    # return render(request, 'principal/date.html', {'date': datetime.now()})
    nb_rand = random.randrange(1, number_of_photo)
    image_name = 'wallpaper/' + str(nb_rand) + '.jpg'
    actual_weather = weather()
    # temperature_lac = temperature_lac_bourget()
    weather_condition = actual_weather.get('condition')
    weather_temperature = actual_weather.get('temperature')
    getimage(TemperatureActuelle.objects.all())
    return render(request, 'principal/graph.html', {
        'nb_rand': nb_rand,
        'image_name': image_name,
        'weather_condition': weather_condition,
        'weather_temperature': weather_temperature,
        # 'imgsrc': imgsrc,
        'date': datetime.now(),
        'Titre': "Air",
    })

def getimage(data):
    cache.clear()
    x1 = array([0,1])
    s1 = array([0,1])
    x1 = array([e.date_ajout for e in data ])
    s1 = array([e.degres for e in data ])
    fig = plt.figure()
    ax = fig.add_subplot(111, facecolor=(0.1, 0.3, 0.2, 0.1))
    ax.plot(x1, s1)

    ax.set_ylabel('°c')
    plt.grid(True)
    fig.autofmt_xdate()

    plt.savefig("static/img/temperature.png", dpi=None, transparent=True)
