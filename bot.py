from cities import Cities

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import Database

TOKEN = "5841939580:AAH2nh8VePTxpvnuseUhOlrmRVWW5PyZeHk"
cities_obj = Cities("other/russia.json")
CITIES = cities_obj.get_cities()

db = Database("user.db")


# FUNCTION
def correct_name(name):
    if len(name) <= 10 and name[0].isupper():
        return True
    return False


# BUTTONS
FORM_BTN = KeyboardButton("Заполнить анкету")
EDIT_FORM_BTN = KeyboardButton("Редактировать анкету")
SWIPE_FORM_BTN = KeyboardButton("Познакомиться")
MBTI_BTN = KeyboardButton("Узнать MBTI")
TAGS_BTN = KeyboardButton("Указать теги")
LIKES_BTN = KeyboardButton("Лайки")
STOP_BTN = KeyboardButton("Скрыть анкету")
LIKE_BTN = KeyboardButton("😍")
SKIP_BTN = KeyboardButton("➡")
BACK_BTN = KeyboardButton("🔙")
EDIT_NAME = KeyboardButton("Имя")
EDIT_CITY = KeyboardButton("Город")
EDIT_AGE = KeyboardButton("Возраст")
EDIT_DESC = KeyboardButton("Описание")
ACTIVE_PROFILE_BTN = KeyboardButton("Активировать")

# KEYBOARDS
FORM_KB = ReplyKeyboardMarkup(resize_keyboard=True)
FORM_KB.add(FORM_BTN)
MENU_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MENU_KB.add(EDIT_FORM_BTN, SWIPE_FORM_BTN, MBTI_BTN, TAGS_BTN, STOP_BTN)
CHECK_USERS = ReplyKeyboardMarkup(resize_keyboard=True)
CHECK_USERS.add(LIKE_BTN, SKIP_BTN)
EDIT_PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_PROFILE_KB.add(EDIT_NAME, EDIT_CITY, EDIT_AGE, EDIT_DESC)
ACTIVE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
ACTIVE_KB.add(ACTIVE_PROFILE_BTN)

users = {}
last_user_id = 0

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    db.add_user_state(user_id, "start", "False")
    db.add_user(user_id, username)
    await message.reply(f"Приветствуем, {message.from_user.username}!\nВ данном боте вы "
                        f"можете познакомиться", reply_markup=FORM_KB)


@dp.message_handler(commands=['menu'])
async def menu_(message: types.Message):
    user_id = message.from_user.id
    db.replace_state(user_id, "wait")
    await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)


@dp.message_handler()
async def info(message: types.Message):
    user_id = message.from_user.id
    global last_user_id

    # Input file
    if message.text == "Заполнить анкету" and db.get_state(user_id) == "start":
        db.replace_state(user_id, "name")
        await message.reply("Введите имя: ")
    elif db.get_state(user_id) == "name":
        if correct_name(message.text):
            db.replace_state(user_id, "city")
            db.replace_name(user_id, message.text)
            await message.reply("Ваше имя принято!\nВведите теперь название города")
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif db.get_state(user_id) == "city":
        if message.text in CITIES:
            db.replace_state(user_id, "age")
            db.replace_city(user_id, message.text);
            await message.reply("Ваш город принят!\nВведите теперь свой возраст")
        else:
            await message.reply(f"Город не обнаружен.\nДоступные города:\n{', '.join(CITIES)}")
    elif db.get_state(user_id) == "age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            db.replace_state(user_id, "description")
            db.replace_age(user_id, message.text);
            await message.reply("Введите пару слов о себе")
    elif db.get_state(user_id) == "description":
        db.replace_state(user_id, "wait")
        db.replace_active(user_id, "True")
        db.replace_description(user_id, message.text)
        profile_list = db.get_my_profile(user_id)
        await message.reply(
            f"\nВаша анкета:\n{profile_list[2]}\n{profile_list[3]}\n{profile_list[4]}\n{profile_list[5]}\n{profile_list[6]}\n",
            reply_markup=MENU_KB)

    # Edit profile
    elif message.text == "Редактировать анкету" and db.get_state(user_id) == "wait":
        db.replace_state(user_id, "edit")
        await message.reply(f"Выберите, что хотите изменить:  ", reply_markup=EDIT_PROFILE_KB)
    elif message.text == "Имя" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_name")
        await message.reply("Введите новое имя: ")
    elif db.get_state(user_id) == "edit_name":
        if correct_name(message.text):
            db.replace_state(user_id, "wait")
            db.replace_name(user_id, message.text)
            profile_list = db.get_my_profile(user_id)
            await message.reply("Ваше имя изменено!\nНовая анкета")
            await message.reply(
                f"\n{profile_list[2]}\n{profile_list[3]}\n{profile_list[4]}\n{profile_list[5]}\n{profile_list[6]}\n",
                reply_markup=MENU_KB)
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif message.text == "Город" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_city")
        await message.reply("Введите новый город: ")
    elif db.get_state(user_id) == "edit_city" and message.text in CITIES:
        db.replace_state(user_id, "wait")
        db.replace_city(user_id, message.text)
        profile_list = db.get_my_profile(user_id)
        await message.reply("Ваш город изменен!")
        await message.reply(
            f"\n{profile_list[2]}\n{profile_list[3]}\n{profile_list[4]}\n{profile_list[5]}\n{profile_list[6]}\n",
            reply_markup=MENU_KB)
    elif message.text == "Возраст" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_age")
        await message.reply("Введите новый возраст: ")
    elif db.get_state(user_id) == "edit_age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            db.replace_state(user_id, "wait")
            db.replace_age(user_id, message.text)
            profile_list = db.get_my_profile(user_id)
            await message.reply("Ваш возраст изменен!")
            await message.reply(
                f"\n{profile_list[2]}\n{profile_list[3]}\n{profile_list[4]}\n{profile_list[5]}\n{profile_list[6]}\n",
                reply_markup=MENU_KB)
    elif message.text == "Описание" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_desc")
        profile_list = db.get_my_profile(user_id)
        await message.reply(f"Прошлое описание: {profile_list[5]}\nВведите новое описание:")
    elif db.get_state(user_id) == "edit_desc":
        db.replace_state(user_id, "wait")
        db.replace_description(user_id, message.text)
        profile_list = db.get_my_profile(user_id)
        await message.reply(
            f"\n{profile_list[2]}\n{profile_list[3]}\n{profile_list[4]}\n{profile_list[5]}\n{profile_list[6]}\n",
            reply_markup=MENU_KB)

    # freeze and active profile
    elif db.get_state(user_id) == "wait" and message.text == "Скрыть анкету":
        db.replace_active(user_id, "False")
        await message.reply(f"Ваша анкета скрыта. Вы не можете смотреть других участников и поставленные лайки.\n"
                            f"Другие пользователи Вас не видят.\n"
                            f"Ваши данные сохранены, Вы всегда можете к нам вернуться.",
                            reply_markup=ACTIVE_KB)
    elif db.get_state(user_id) == "wait" and message.text == "Активировать":
        db.replace_active(user_id, "True")
        await message.reply(f"Ваша анкета снова видна в поиске!", reply_markup=MENU_KB)


if __name__ == '__main__':
    executor.start_polling(dp)
