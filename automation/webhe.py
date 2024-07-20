import os
import nest_asyncio
from datetime import date
from time import sleep
import logging
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, Router
from students.func_proj_lib import find_by_date, find_in_menu
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker


nest_asyncio.apply()
maker = PetrovichDeclinationMaker()
logging.basicConfig(level=logging.INFO)
session = AiohttpSession()
bot_settings = {"session": session, "parse_mode": ParseMode.HTML}
bot = Bot(token=os.getenv("BOT_TOKEN"), **bot_settings)
dp = Dispatcher()
router = Router()

today_for_search = str(date.today().strftime("%d.%m"))

chat_id = -1001185804748
message_thread_id = 25150


async def name_cases_to_genitive(l_name, f_name):
    f_name = maker.make(NamePart.FIRSTNAME, Gender.MALE, Case.GENITIVE, f_name)
    l_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.GENITIVE, l_name)
    return l_name, f_name


async def menu_sched():
    res = "OK"
    try:
        menu_list = find_in_menu()
        if menu_list is None:
            menu_list = "Сегодня столовая закрыта."
        await bot.send_message(chat_id=chat_id,
                               text=f"{menu_list}",
                               message_thread_id=message_thread_id)
    except Exception as error:
        res = error
    finally:
        return res


async def bday_sched():
    res = "OK"

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
                send_list.append(f"\n*{name} из {school_class} класса")
            send_list = "\n".join(send_list)
            await bot.send_message(chat_id=chat_id,
                                   text=send_list,
                                   message_thread_id=message_thread_id)
            sleep(0.001)
            await bot.send_message(chat_id=chat_id,
                                   text=f"Не забудьте поздравить!",
                                   message_thread_id=message_thread_id)
    except Exception as error:
        res = error
    finally:
        return res


async def dayli_sht(event, context=None):
    status = 200
    body = "OK"
    res1, res2 = "BAD", "BAD"
    try:
        res1 = await bday_sched()
        #res2 = await menu_sched()
    except Exception as Err:
        status = 500
        body = Err
    finally:
        return {
            "statusCode": status,
            "body": [body, res1, res2]
        }
