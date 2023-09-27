import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from Keyboards import Keyboard, Keyboard_prognoz
from services import get_prognoz


async def process_start_command(message: types.Message):
    await message.answer(
        f'Привет {message.from_user.first_name}! Напиши город в котором ты хочешь узнать прогноз погоды.')


async def process_help_command(message: types.Message):
    await message.answer('Бот предоставляет прогноз на сегодня и на завтра\n\n'
                         'Кнопка "Народный прогноз" предоставляет информацию '
                         'о народных приметах связанных с этим днём.')


async def process_get_prognoz(message: types.Message, state: FSMContext):
    city = message.text.lower().strip().replace(' ', '-')
    async with state.proxy() as data:
        data['city'] = city
        current_date = datetime.date.today()
        tomorrow_date = current_date + datetime.timedelta(days=1)

        weather_today = get_prognoz(city, current_date)
        weather_tomorrow = get_prognoz(city, tomorrow_date)
        if not weather_today:
            await message.answer('К сожалению я не владею информацией о погоде в этом городе.')
        else:
            data['today'] = weather_today
            data['tomorrow'] = weather_tomorrow
            await message.answer(
                'Отлично! По этому городу у меня есть прогноз!\n\nКакой прогноз тебя интересует?\nВыбирай ниже ⬇',
                reply_markup=Keyboard_prognoz)


async def process_weather_today(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(text=f'<b>Погода на сегодня:</b>\n'
                                  f'Температура днём: от {data["today"]["day_1"]} до {data["today"]["day_2"]}\n'
                                  f'Температура ночью: от {data["today"]["night_1"]} до {data["today"]["night_2"]}\n\n'
                                  f'{data["today"]["text_prognoz"]}',
                             reply_markup=Keyboard, parse_mode='html')


async def process_weather_tomorrow(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(text=f'<b>Погода на завтра:</b>\n'
                                  f'Температура днём: от {data["tomorrow"]["day_1"]} до {data["tomorrow"]["day_2"]}\n'
                                  f'Температура ночью: от {data["tomorrow"]["night_1"]} до '
                                  f'{data["tomorrow"]["night_2"]}\n\n'
                                  f'{data["tomorrow"]["text_prognoz"]}',
                             reply_markup=Keyboard, parse_mode='html')


async def process_narodny_prognoz(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(f'{data["today"]["narodny_prognoz"]}', reply_markup=Keyboard)


async def process_other_prognoz(message: types.Message):
    await message.answer('Выбирай какой еще прогноз хочешь посмотреть ⬇', reply_markup=Keyboard_prognoz)


async def process_other_city(message: types.Message):
    await message.answer('Напиши город в котором хочешь узнать прогноз')


async def process_exit(message: types.Message):
    await message.answer('Увидимся!\n\nЕсли захочешь узнать прогноз просто напиши мне название города.',
                         reply_markup=ReplyKeyboardRemove())


# Функция для регистрации хэндлеров в диспетчере. Вызывается в исполняемом файле bot.py
def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands='start')
    dp.register_message_handler(process_help_command, commands='help')
    dp.register_message_handler(process_weather_today, text='Прогноз на сегодня')
    dp.register_message_handler(process_weather_tomorrow, text='Прогноз на завтра')
    dp.register_message_handler(process_narodny_prognoz, text='🌞Народный прогноз🌞')
    dp.register_message_handler(process_other_prognoz, text='Посмотреть другой прогноз ♻')
    dp.register_message_handler(process_other_city, text='Выбрать другой город 🏙')
    dp.register_message_handler(process_exit, text='Выход ❌')
    dp.register_message_handler(process_get_prognoz)
