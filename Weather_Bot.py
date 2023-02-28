from aiogram import Bot, Dispatcher, executor, types
from user_handlers import register_user_handlers
from config import Config, load_config

config: Config = load_config()

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher(bot)


async def set_main_menu(dp: Dispatcher):
    # Создаем список с командами для кнопки menu
    main_menu_commands = [
        types.BotCommand(command='/start', description='Запустить бота'),
        types.BotCommand(command='/help', description='Справка по работе бота')
    ]
    await dp.bot.set_my_commands(main_menu_commands)



register_user_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_main_menu)