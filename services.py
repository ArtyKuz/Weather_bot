import aiohttp
from bs4 import BeautifulSoup


async def get_forecast(city: str, current_date) -> dict | bool:
    weather: dict = {}
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'https://sinoptik.ua/погода-{city}/{current_date}')
        if response.status == 200:
            b = BeautifulSoup(await response.text(), 'html.parser')

            weather['night_1'] = b.select('.temperature .p1')[0].getText()
            weather['night_2'] = b.select('.temperature .p2')[0].getText()
            weather['day_1'] = b.select('.temperature .p5')[0].getText()
            weather['day_2'] = b.select('.temperature .p6')[0].getText()

            weather['text_prognoz'] = b.select('.description')[0].getText().strip()
            narodny_prognoz = b.select('.description')[1].getText()
            ind = narodny_prognoz.index(':')
            weather['narodny_prognoz'] = narodny_prognoz[ind + 2:]

            return weather

        return False
