import requests
from bs4 import BeautifulSoup


def get_prognoz(city: str, current_date):
    weather = dict()

    s = requests.get(f'https://sinoptik.ua/погода-{city}/{current_date}')

    if s.status_code == 200:
        b = BeautifulSoup(s.text, 'html.parser')

        weather['weather_night_1'] = b.select('.temperature .p1')[0].getText()
        weather['weather_night_2'] = b.select('.temperature .p2')[0].getText()
        weather['weather_day_1'] = b.select('.temperature .p5')[0].getText()
        weather['weather_day_2'] = b.select('.temperature .p6')[0].getText()

        weather['text_prognoz'] = b.select('.description')[0].getText().strip()
        narodny_prognoz = b.select('.description')[1].getText()
        ind = narodny_prognoz.index(':')
        weather['narodny_prognoz'] = narodny_prognoz[ind + 2:]

        return weather
    else:
        return False
