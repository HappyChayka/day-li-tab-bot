# https://t.me/c/1185804748/13430
# Топик в ли_спейс

# https://t.me/c/1610094748/2
# Топик в моём чате

import nest_asyncio

from datetime import date
from time import sleep
import asyncio
import logging
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types, Router
from aiogram.methods import GetUpdates
from aiogram.filters.command import Command, CommandObject
from aiogram.exceptions import TelegramNetworkError
from sqlite3 import Error
from apscheduler.triggers.cron import CronTrigger
from func_proj_lib import find_by_date, find_by_name, find_in_menu
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker


nest_asyncio.apply()
maker = PetrovichDeclinationMaker()
logging.basicConfig(level=logging.INFO)
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()
router = Router()

today_for_search = str(date.today().strftime("%d.%m"))

"""        
class ChatAdmins:
    def __init__(self):
"""


async def name_cases_to_genitive(l_name, f_name):
    f_name = maker.make(NamePart.FIRSTNAME, Gender.MALE, Case.GENITIVE, f_name)
    l_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.GENITIVE, l_name)
    return l_name, f_name


async def menu_sched():
    await rec()
    sleep(0.1)
    # chat_id, message_thread_id
    chat_id = -1001185804748
    message_thread_id = 13430
    # chat_id = -1001610094748
    # message_thread_id = 2
    menu_list = find_in_menu()
    if menu_list is None:
        menu_list = "Сегодня столовая закрыта."
    await bot.send_message(chat_id=chat_id,
                           text=f"{menu_list}",
                           message_thread_id=message_thread_id)


async def bday_sched():
    # chat_id, message_thread_id
    chat_id = -1001185804748
    message_thread_id = 13225
    # chat_id = -1001610094748
    # message_thread_id = 2
    bday_list = find_by_date(today_for_search)
    send_list = []
    try:
        if len(bday_list) == 0:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Сегодня ни у кого нет дня рождения.",
                                   message_thread_id=message_thread_id)
        else:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Сегодня день рождения у",
                                   message_thread_id=message_thread_id)
            for i in bday_list:
                name = " ".join(await name_cases_to_genitive(i[0].split()[0], i[0].split()[1]))
                school_class = i[1]
                send_list.append(f"*{name} из {school_class} класса")
            send_list = "\n".join(send_list)
            await bot.send_message(chat_id=chat_id,
                                   text=send_list,
                                   message_thread_id=message_thread_id)
            sleep(0.001)
            await bot.send_message(chat_id=chat_id,
                                   text=f"Не забудьте поздравить!",
                                   message_thread_id=message_thread_id)
    except Error:
        pass


async def send_celebs(message, bday_list, date="Сегодня", date_known=True):
    try:
        if len(bday_list) > 0:
            if date_known:
                await message.answer(f"{date} день рождения у")
            sleep(0.001)
            list_of_answers = list()
            for i in bday_list:
                bday = i[-1]
                name = i[0].split()
                name = " ".join(await name_cases_to_genitive(name[0], name[1]))
                school_class = i[1]
                answ = f"\n*{name} из {school_class} класса"
                if not date_known:
                    answ = f"\nДень рождения {answ} будет {bday}"
                list_of_answers.append(answ)
            await message.answer("\n".join(list_of_answers))
            sleep(0.001)
            if date_known:
                await message.answer("Поздравляем!")
        else:
            await message.answer(f"{date} ни у кого нет дня рождения.")
    except Error:
        await message.answer("Произошла ошибка SQL, доложите @HappyChayka.")


"""@dp.message(Command("testic"))
async def test_testic(message: types.Message):
    await bday_sched(-1001610094748, 233)
dp.message.register(test_testic, Command("testic"))"""


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.chat.type == "private":
        await message.answer('''Привет!
    Я — первый бот Ли24!
    Пока что я могу только поздравить с днём рождения и отправить тебе актуальное меню столовой.
    Но дальше будет только больше!
    
    Мои команды:
    /start — Информация о боте
    /menu — Актуальное меню в Лицее
    /bday — Дни Рождения
    
    Напиши /help для дополнительной информации!
    
    (я не понимаю речь, извини)''')


@dp.message(Command("help"))
async def help_event(message: types.Message):
    if message.chat.type == "private":
        await message.answer('''
    /start — Информация о боте
    /menu {Дата в формате ДД.ММ}
    /help — Список команд бота
    /bday {Дата в формате ДД.ММ} / {Ф/И/О} , {КлассБуква}
        { } / { } = Взаимозаменяемые дополнительные фильтры
    
        Обязательно соблюдайте последовательность строчных и заглавных букв.''')
dp.message.register(help_event, Command("help"))


@dp.message(Command("menu"))
async def menu_event(message: types.Message, command: CommandObject):
    #await rec()
    #sleep(0.1)
    await bot(GetUpdates())
    if command.args:
        comm_args = str(command.args).split(".")
        date_in_args = date(day=int(comm_args[0]), month=int(comm_args[1]), year=date.today().year)
        menu_list = find_in_menu(date_in_args)
    else:
        menu_list = find_in_menu()
    if message.chat.type == "private":
        if menu_list is None:
            menu_list = "В этот день столовая закрыта."
        await message.answer(f"{menu_list}")

    else:
        chat_admins = set()
        if message.chat.type != "private":
            get_admins = await bot.get_chat_administrators(message.chat.id)
            for admin in get_admins:
                chat_admins.add(admin.user.id)
        if message.from_user.id in chat_admins:
            if menu_list is None:
                menu_list = "Сегодня столовая закрыта."
            await message.answer(f"{menu_list}")
        else:
            try:
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Недостаточно прав для выполнения действия.")
                await message.delete()
            except:
                pass
dp.message.register(menu_event, Command("menu"))


@dp.message(Command("bday"))
async def bday_event(message: types.Message, command: CommandObject):
    #await rec()
    #sleep(0.1)
    await bot(GetUpdates())
    chat_admins = set()
    if message.chat.type != "private":
        get_admins = await bot.get_chat_administrators(message.chat.id)
        for admin in get_admins:
            chat_admins.add(admin.user.id)
    if message.chat.type == "private" or message.from_user.id in chat_admins:
        if command.args:

            comm_args = command.args.split(",")

            if len(comm_args) == 2:
                class_id = comm_args[1].strip()
            elif len(comm_args) > 2:
                await message.answer("Ошибка! Максимально допустимо два аргумента.")
                return
            else:
                class_id = None

            try:
                # Если можно превратить в значение с плавающей точкой, то
                float(comm_args[0])
                date_in_args = str(comm_args[0])
                bday_list = find_by_date(date_in_args, class_id)
                await send_celebs(message, bday_list, date_in_args, True)

            except ValueError:
                name = str(command.args).split()[0]
                bday_list = find_by_name(name, class_id)
                await send_celebs(message, bday_list, "", False)
        else:
            await send_celebs(message, find_by_date(today_for_search))
    else:
        try:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Недостаточно прав для выполнения действия.")
            await message.delete()
        except:
            pass
dp.message.register(bday_event, Command("bday"))


@dp.message(Command("resend_em"))
async def emergency_resend(message: types.Message):
    chat_admins = set()
    if message.chat.type != "private":
        get_admins = await bot.get_chat_administrators(message.chat.id)
        for admin in get_admins:
            chat_admins.add(admin.user.id)
        if message.from_user.id in chat_admins:
            await bday_sched()
            await menu_sched()

        else:
            await message.delete()
dp.message.register(emergency_resend, Command("resend_em"))


async def scheduler():
    f_scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # -1001185804748, 13225     li_space
    # -1001610094748, 2         my_chat
    trigger = CronTrigger(hour=7, minute=15)
    f_scheduler.add_job(bday_sched, trigger)
    f_scheduler.add_job(menu_sched, trigger)
    f_scheduler.add_job(reconnect, "interval", hours=1)
    f_scheduler.start()


async def on_startup():
    await asyncio.create_task(scheduler())
    await dp.start_polling(bot)


async def rec():
    try:
        await bot(GetUpdates())
    except TelegramNetworkError:
        await dp.stop_polling()
        await dp.start_polling(bot)


async def reconnect():
    await rec()


async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())
    loop.close()


if __name__ == "__main__":
    asyncio.run(main())



