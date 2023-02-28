from aiogram.types import ReplyKeyboardMarkup


Keyboard_prognoz = ReplyKeyboardMarkup(resize_keyboard=True)
Keyboard_prognoz.add('Прогноз на сегодня', 'Прогноз на завтра').add('🌞Народный прогноз🌞')


Keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
Keyboard.add('Посмотреть другой прогноз ♻').add('Выбрать другой город 🏙').add('Выход ❌')