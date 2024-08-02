import json
import time
import nest_asyncio
import sys
import os
from datetime import date
from time import sleep
import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command, CommandObject
from students.func_proj_lib import find_by_date, find_by_name, find_in_menu
from library.lib_app_back import search_data_rec
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker

# from middlewares import ThrottlingMiddleware

nest_asyncio.apply()
maker = PetrovichDeclinationMaker()
logger = logging.getLogger(__name__)
webhook = os.getenv("BASE_WEBHOOK_URL") + os.getenv("WEBHOOK_PATH")
session = AiohttpSession()
bot_settings = {"session": session, "parse_mode": ParseMode.HTML}
bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

today_for_search = str(date.today().strftime("%d.%m"))


async def get_chat_admins(message: types.Message):
    return {admin for admin in await bot.get_chat_administrators(message.chat.id)}


async def name_cases_to_genitive(l_name, f_name):
    f_name = maker.make(NamePart.FIRSTNAME, Gender.MALE, Case.GENITIVE, f_name)
    l_name = maker.make(NamePart.LASTNAME, Gender.MALE, Case.GENITIVE, l_name)
    return l_name, f_name


async def send_celebs(message, bday_list, var_date="Сегодня", date_known=True):
    if len(bday_list) < 0:
        await message.answer(f"Ни у кого нет дня рождения.")
        return

    if date_known:
        await message.answer(f"{var_date} день рождения у")

    sleep(0.001)
    list_of_answers = list()
    for i in bday_list:
        name = i[0].split()
        name = " ".join(await name_cases_to_genitive(name[0], name[1]))
        school_class, bday = i[1], i[-1]

        answ = f"\n*{name} из {school_class} класса"
        if not date_known:
            answ = f"\nДень рождения {answ} будет {bday}"
        list_of_answers.append(answ)
    await message.answer("\n".join(list_of_answers))
    sleep(0.001)
    if date_known:
        await message.answer("Поздравляем!")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.chat.type == "private":
        await message.answer('''
Привет!
Я — первый бот Ли24!
Пока что я могу только поздравить с днём рождения, отправить тебе актуальное меню столовой
и сказать, какие книги есть в нашей библиотеке.
Но дальше будет только больше!

Мои команды:
/start — Информация о боте
/menu — Актуальное меню в Лицее
/bday — Дни Рождения

Напиши /help для дополнительной информации!
''')


@dp.message(Command("help"))
async def help_event(message: types.Message):
    if message.chat.type == "private":
        await message.answer('''
/start — Информация о боте
/menu {Дата в формате ДД.ММ} — меню на заданный день
/help — Список команд бота
/searchbook - {И.О.Фамилия автора} , {Название}
/bday {Дата в формате ДД.ММ} / {Ф/И/О} , {КлассБуква}

    { } / { } = Взаимозаменяемые дополнительные фильтры''')


dp.message.register(help_event, Command("help"))


@dp.message(Command("menu"))
async def menu_event(message: types.Message, command: CommandObject):
    if command.args:
        comm_args = str(command.args).split(".")
        date_in_args = date(day=int(comm_args[0]), month=int(comm_args[1]), year=date.today().year)
        menu_list = find_in_menu(date_in_args)
    else:
        menu_list = find_in_menu()
    if message.chat.type == "private" or message.from_user.id in get_chat_admins(message):
        if menu_list is None:
            menu_list = "В этот день столовая закрыта."
        await message.answer(f"{menu_list}")


dp.message.register(menu_event, Command("menu"))


@dp.message(Command("bday"))
async def bday_event(message: types.Message, command: CommandObject):
    if message.chat.type == "private" or message.from_user.id in get_chat_admins(message):
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


dp.message.register(bday_event, Command("bday"))


@dp.message(Command("searchbook"))
async def library_search_event(message: types.Message, command: CommandObject):
    if message.chat.type == "private" or message.from_user.id in get_chat_admins(message):
        try:
            arguments = command.args.split(",")
            if 1 <= len(arguments) <= 2:
                name = arguments[0].lower()
                title = ""
                if len(arguments) == 2:
                    title = arguments[1].lower()
            else:
                raise TypeError
        except TypeError:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Некорректный запрос.")
            return
        op = list()
        for i in search_data_rec(Atr=name.strip(), Bkt=title.strip()):
            op.append("* " + " — ".join([j.title() for j in i if isinstance(j, str)]).strip())
        for i in search_data_rec(Bkt=name.strip(), Atr=title.strip()):
            op.append("* " + " — ".join([j.title() for j in i if isinstance(j, str)]).strip())
        if len(op) == 0:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Такой книги, к сожалению, не нашлось.")
            return
        op = "\n".join(sorted(list((set(op)))))
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Вот, что нашлось: \n{op}")


dp.message.register(bday_event, Command("searchbook"))


async def on_startup():
    await bot.set_webhook(url=webhook)


async def on_shutdown():
    await bot.delete_webhook()


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    await on_startup()

    dp.include_router(router)
    # dp.message.middleware.register(ThrottlingMiddleware())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)


async def yc_handler(event: dict[str], context=None):
    body = json.loads(event["body"])

    if "message" in body.keys():
        mess = body["message"]
    elif "edited_message" in body.keys():
        mess = body["edited_message"]
    else:
        print(body.keys())
        raise KeyError

    result = await dp.feed_raw_update(bot, body)
    log_message = f"Processed event at {time.strftime('%X')}. User ID [{mess['from']['id']}]. Result: <{result}>"
    logger.info(log_message)
    return {"statusCode": 200, "body": log_message}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
