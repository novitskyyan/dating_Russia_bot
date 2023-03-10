from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import Database


TOKEN = "5841939580:AAH2nh8VePTxpvnuseUhOlrmRVWW5PyZeHk"
FILENAME = "database"
FILENAME_LIKES = "liked"
CITIES = ["Москва", "Новгород", "Самара", "Сызрань", "Саратов", "Санкт-Петербург", ]


# FUNCTION
def correct_name(name):
    if len(name) <= 10 and name[0].isupper():
        return True
    return False



# BUTTONS
FORM_BTN = KeyboardButton("Заполнить анкету")
EDIT_FORM_BTN = KeyboardButton("Редактировать анкету")
SWIPE_FORM_BTN = KeyboardButton("Смотреть анкеты")
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
MENU_KB.add(EDIT_FORM_BTN, SWIPE_FORM_BTN, LIKES_BTN, STOP_BTN)
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
    users = Database.get_dict(FILENAME)
    user_id = str(message.from_user.id)
    username = message.from_user.username
    users[user_id] = {"state": "start", "active": "False",
                      "username": username, "name": "no", "city": "no", "age": "no", "likes": []}
    Database.write(users, FILENAME)
    await message.reply(f"Приветствуем, {message.from_user.username}!\nВ данном боте вы "
                        f"можете познакомиться", reply_markup=FORM_KB)

@dp.message_handler(commands=['menu'])
async def menu_(message: types.Message):
    users = Database.get_dict(FILENAME)
    user_id = str(message.from_user.id)
    users[user_id]["state"] = "wait"
    Database.write(users, FILENAME)
    await message.reply(f"Вернулись в главное меню", reply_markup=MENU_KB)


@dp.message_handler()
async def info(message: types.Message):
    user_id = str(message.from_user.id)
    global last_user_id
    users = Database.get_dict(FILENAME)
    if message.text == "Заполнить анкету" and users[user_id]["state"] == "start":
        users[user_id]["state"] = "name"
        Database.write(users, FILENAME)
        await message.reply("Введите имя: ")
    elif users[user_id]["state"] == "name":
        if correct_name(message.text):
            users[user_id]["state"] = "city"
            users[user_id]["name"] = message.text
            Database.write(users, FILENAME)
            await message.reply("Ваше имя принято!\nВведите теперь название города")
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif users[user_id]["state"] == "city":
        if message.text in CITIES:
            users[user_id]["state"] = "age"
            users[user_id]["city"] = message.text
            Database.write(users, FILENAME)
            await message.reply("Ваш город принят!\nВведите теперь свой возраст")
        else:
            await message.reply(f"Город не обнаружен.\nДоступные города:\n{', '.join(CITIES)}")
    elif users[user_id]["state"] == "age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            users[user_id]["state"] = "description"
            users[user_id]["age"] = message.text
            users[user_id]["active"] = "True"
            Database.write(users, FILENAME)
            await message.reply("Введите пару слов о себе")
    elif users[user_id]["state"] == "description":
        users[user_id]["state"] = "wait"
        Database.save_desc_to_file(user_id, message.text)
        Database.write(users, FILENAME)
        await message.reply("Анкета заполнена!", reply_markup=MENU_KB)
    elif users[user_id]["state"] == "wait" and message.text == "Смотреть анкеты":
        users[user_id]["state"] = "check_profiles"
        Database.write(users, FILENAME)
        user_info = Database.random_profile_list(FILENAME, user_id)
        last_user_id = user_info[0]
        await message.reply(f"{user_info[1]}\n{user_info[2]}\n{user_info[3]}\n{user_info[4]}", reply_markup=CHECK_USERS)
    elif users[user_id]["state"] == "check_profiles" and message.text == "➡":
        Database.write(users, FILENAME)
        user_info = Database.random_profile_list(FILENAME, user_id)
        last_user_id = user_info[0]
        await message.reply(f"{user_info[1]}\n{user_info[2]}\n{user_info[3]}", reply_markup=CHECK_USERS)
    # Edit Profile
    elif message.text == "Редактировать анкету" and users[user_id]["state"] == "wait":
        users[user_id]["state"] = "edit"
        Database.write(users, FILENAME)
        await message.reply(f"Выберите, что хотите изменить:  ", reply_markup=EDIT_PROFILE_KB)
    elif message.text == "Имя" and users[user_id]["state"] == "edit":
        users[user_id]["state"] = "edit_name"
        Database.write(users, FILENAME)
        await message.reply("Введите новое имя: ")
    elif users[user_id]["state"] == "edit_name":
        if correct_name(message.text):
            users[user_id]["state"] = "wait"
            users[user_id]["name"] = message.text
            Database.write(users, FILENAME)
            profile_list = Database.get_my_profile(FILENAME, user_id)
            await message.reply("Ваше имя изменено!\nНовая анкета")
            await message.reply(
                f"\n{profile_list[0]}\n{profile_list[1]}\n{profile_list[2]}\n{Database.get_desc_user(user_id)}",
                reply_markup=MENU_KB)
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif message.text == "Город" and users[user_id]["state"] == "edit":
        users[user_id]["state"] = "edit_city"
        Database.write(users, FILENAME)
        await message.reply("Введите новый город: ")
    elif users[user_id]["state"] == "edit_city":
        users[user_id]["state"] = "wait"
        users[user_id]["city"] = message.text
        Database.write(users, FILENAME)
        profile_list = Database.get_my_profile(FILENAME, user_id)
        await message.reply("Ваш город изменен!")
        await message.reply(f"\n{profile_list[0]}\n{profile_list[1]}\n{profile_list[2]}\n{Database.get_desc_user(user_id)}", reply_markup=MENU_KB)
    elif message.text == "Возраст" and users[user_id]["state"] == "edit":
        users[user_id]["state"] = "edit_age"
        Database.write(users, FILENAME)
        await message.reply("Введите новый возраст: ")
    elif users[user_id]["state"] == "edit_age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            users[user_id]["state"] = "wait"
            users[user_id]["age"] = message.text
            Database.write(users, FILENAME)
            profile_list = Database.get_my_profile(FILENAME, user_id)
            await message.reply("Ваш возраст изменен!")
            await message.reply(
                f"\n{profile_list[0]}\n{profile_list[1]}\n{profile_list[2]}\n{Database.get_desc_user(user_id)}",
                reply_markup=MENU_KB)
    elif message.text == "Описание" and users[user_id]["state"] == "edit":
        users[user_id]["state"] = "edit_desc"
        Database.write(users, FILENAME)
        await message.reply(f"Прошлое описание: {Database.get_desc_user(user_id)}\nВведите новое описание:")
    elif users[user_id]["state"] == "edit_desc":
        users[user_id]["state"] = "wait"
        Database.save_desc_to_file(user_id, message.text)
        Database.write(users, FILENAME)
        profile_list = Database.get_my_profile(FILENAME, user_id)
        await message.reply(f"\n{profile_list[0]}\n{profile_list[1]}\n{profile_list[2]}\n{Database.get_desc_user(user_id)}", reply_markup=MENU_KB)

    # Check Profiles
    elif users[user_id]["state"] == "check_profiles" and message.text == "😍":
        if last_user_id not in users[user_id]["likes"]:
            users[user_id]["likes"].append(last_user_id)
        Database.write(users, FILENAME)
        user_info = Database.random_profile_list(FILENAME, user_id)
        last_user_id = user_info[0]
        await message.reply(f"{user_info[1]}\n{user_info[2]}\n{user_info[3]}", reply_markup=CHECK_USERS)
    elif users[user_id]["state"] == "wait" and message.text == "Лайки":
        users = Database.get_dict(FILENAME)
        for liked_id in users[user_id]["likes"]:
            for id in users.keys():
                if liked_id == id:
                    if user_id in users[id]["likes"] and users[id]["active"] == "True":
                        user_info = Database.get_profile_by_id(users, id)
                        await message.reply(f"@{user_info[0]}\n{user_info[1]}\n{user_info[2]}\n"
                                            f"{user_info[3]}")
    # freeze and active profile
    elif users[user_id]["state"] == "wait" and message.text == "Скрыть анкету":
        users[user_id]["active"] = "False"
        Database.write(users, FILENAME)
        await message.reply(f"Ваша анкета скрыта. Вы не можете смотреть других участников и поставленные лайки.\n"
                            f"Другие пользователи Вас не видят.\n"
                            f"Ваши данные сохранены, Вы всегда можете к нам вернуться.",
                            reply_markup=ACTIVE_KB)
    elif users[user_id]["state"] == "wait" and message.text == "Активировать":
        users[user_id]["active"] = "True"
        Database.write(users, FILENAME)
        await message.reply(f"Ваша анкета снова видна в поиске!", reply_markup=MENU_KB)







if __name__ == '__main__':
    executor.start_polling(dp)