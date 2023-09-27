import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from user_handlers import register_user_handlers
from config import Config, load_config

config: Config = load_config()
storage = MemoryStorage()
# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher(bot, storage=storage)


async def main():
    # Создаем список с командами для кнопки menu
    main_menu_commands = [
        types.BotCommand(command='/start', description='Запустить бота'),
        types.BotCommand(command='/help', description='Справка по работе бота')
    ]
    await dp.bot.set_my_commands(main_menu_commands)

    register_user_handlers(dp)
    await dp.start_polling()
    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
