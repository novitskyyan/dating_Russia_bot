from cities import Cities
from database import Database
from read_tags import Read_tags

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import os


TOKEN = "5841939580:AAH2nh8VePTxpvnuseUhOlrmRVWW5PyZeHk"
cities_obj = Cities("other/russia.json")
CITIES = cities_obj.get_cities()

db = Database("user.db")


# FUNCTION
def correct_name(name):
    if len(name) <= 10 and name[0].isupper():
        return True
    return False


def get_profile(user_id):
    profile = db.get_my_profile(user_id)
    return f"Ваша анкета\n" \
           f"---------\n" \
           f"{profile[2]}\n{profile[3]}\n{profile[4]}\n{profile[5]}\n{profile[6]}"


def from_str_to_list(s):
    return s.split(", ")


def from_list_to_str(l):
    return ", ".join(l)


def convert_to_binary_data(filename):
    with open(f'img/{filename}', 'rb') as file:
        blob_data = file.read()
    return blob_data


def write_to_file(data, filename):
    with open(f'img/{filename}', 'wb') as file:
        file.write(data)


# BUTTONS
FORM_BTN = KeyboardButton("Заполнить анкету")
EDIT_FORM_BTN = KeyboardButton("Редактировать анкету")
SWIPE_FORM_BTN = KeyboardButton("Познакомиться")
#MBTI_BTN = KeyboardButton("Узнать MBTI")
TAGS_BTN = KeyboardButton("Указать теги")
LIKES_BTN = KeyboardButton("Лайки")
STOP_BTN = KeyboardButton("Скрыть анкету")
LIKE_BTN = KeyboardButton("😍")
SKIP_BTN = KeyboardButton("➡")
BACK_BTN = KeyboardButton("🔙")
EDIT_NAME = KeyboardButton("Имя")
MALE_BTN = KeyboardButton("Мужской")
FEMALE_BTN = KeyboardButton("Женский")
EDIT_CITY = KeyboardButton("Город")
EDIT_AGE = KeyboardButton("Возраст")
EDIT_DESC = KeyboardButton("Описание")
ACTIVE_PROFILE_BTN = KeyboardButton("Активировать")
YES_BTN = KeyboardButton("ДА")
NO_BTN = KeyboardButton("НЕТ")
LIFE_TAGS = KeyboardButton("Жизнь")
MUSIC_TAGS = KeyboardButton("Жанры музыки")
FILTER_BTN = KeyboardButton("Фильтр")
FILTER_AGE = KeyboardButton("По возрасту")
FILTER_GENDER = KeyboardButton("По полу")
FILTER_CITY = KeyboardButton("По городу")

# KEYBOARDS
FORM_KB = ReplyKeyboardMarkup(resize_keyboard=True)
FORM_KB.add(FORM_BTN)
MENU_KB = ReplyKeyboardMarkup(resize_keyboard=True)
MENU_KB.add(EDIT_FORM_BTN, SWIPE_FORM_BTN, TAGS_BTN, FILTER_BTN, STOP_BTN)
CHECK_USERS = ReplyKeyboardMarkup(resize_keyboard=True)
CHECK_USERS.add(LIKE_BTN, SKIP_BTN)
EDIT_PROFILE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
EDIT_PROFILE_KB.add(EDIT_NAME, EDIT_CITY, EDIT_AGE, EDIT_DESC)
ACTIVE_KB = ReplyKeyboardMarkup(resize_keyboard=True)
ACTIVE_KB.add(ACTIVE_PROFILE_BTN)
ANS_KB = ReplyKeyboardMarkup(resize_keyboard=True)
ANS_KB.add(YES_BTN, NO_BTN)
TAGS_KB = ReplyKeyboardMarkup(resize_keyboard=True)
TAGS_KB.add(LIFE_TAGS, MUSIC_TAGS)
GENDER_KB = ReplyKeyboardMarkup(resize_keyboard=True)
GENDER_KB.add(MALE_BTN, FEMALE_BTN)
FILTER_KB = ReplyKeyboardMarkup(resize_keyboard=True)
FILTER_KB.add(FILTER_AGE, FILTER_GENDER, FILTER_CITY)

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
            db.replace_state(user_id, "gender")
            db.replace_name(user_id, message.text)
            await message.reply("Ваше имя принято!\nВыберите свой пол:", reply_markup=GENDER_KB)
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif db.get_state(user_id) == "gender" and message.text == "Мужской" or message.text == "Женский":
        db.replace_state(user_id, "city")
        db.replace_gender(user_id, message.text[0])
        await message.reply("Ваше пол принят!\nВведите теперь название города", reply_markup=ReplyKeyboardRemove())
    elif db.get_state(user_id) == "city":
        if message.text in CITIES:
            db.replace_state(user_id, "age")
            db.replace_city(user_id, message.text)
            await message.reply("Ваш город принят!\nВведите теперь свой возраст")
        else:
            await message.reply(f"Город не обнаружен.\nДоступные города:\n{', '.join(CITIES)}")
    elif db.get_state(user_id) == "age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            db.replace_state(user_id, "description")
            db.replace_age(user_id, message.text);
            await message.reply("Введите пару слов о себе")
    elif db.get_state(user_id) == "description":
        db.replace_state(user_id, "ans1")
        db.replace_description(user_id, message.text)
        await message.reply(
            f"Ответьте на вопросы, чтобы определить свой тип личности.\n\n"
            f"В компаниях вы любите быть в центре внимания (ДА / НЕТ)", reply_markup=ANS_KB)
    elif db.get_state(user_id) == "ans1" and message.text in ["ДА", "НЕТ"]:
        ans = message.text
        if ans == "ДА":
            db.replace_mbti(user_id, "E")
        else:
            db.replace_mbti(user_id, "I")
        db.replace_state(user_id, "ans2")
        await message.reply("Ваши мысли, как правило, сосредоточены на событиях реального мира,"
                            "а не на гипотетических возможностях", reply_markup=ANS_KB)
    elif db.get_state(user_id) == "ans2" and message.text in ["ДА", "НЕТ"]:
        ans = message.text
        if ans == "ДА":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "N")
        else:
            db.replace_mbti(user_id, db.get_mbti(user_id) + "S")
        db.replace_state(user_id, "ans3")
        await message.reply("Во время спора чувства других людей должны быть важнее правды",
                            reply_markup=ANS_KB)
    elif db.get_state(user_id) == "ans3" and message.text in ["ДА", "НЕТ"]:
        ans = message.text
        if ans == "ДА":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "F")
        else:
            db.replace_mbti(user_id, db.get_mbti(user_id) + "T")
        db.replace_state(user_id, "ans4")
        await message.reply("Вы продумываете свои планы проведения досуга до мелочей",
                            reply_markup=ANS_KB)
    elif db.get_state(user_id) == "ans4" and message.text in ["ДА", "НЕТ"]:
        ans = message.text
        if ans == "ДА":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "P")
        else:
            db.replace_mbti(user_id, db.get_mbti(user_id) + "J")
        db.replace_state(user_id, "ans5")
        await message.reply("Если кто-то сразу не ответил на ваше сообщение, "
                            "вы начинаете волноваться, что написали что-то не то",
                            reply_markup=ANS_KB)
    elif db.get_state(user_id) == "ans5" and message.text in ["ДА", "НЕТ"]:
        ans = message.text
        if ans == "ДА":
            db.replace_mbti(user_id, db.get_mbti(user_id) + "T")
        else:
            db.replace_mbti(user_id, db.get_mbti(user_id) + "A")
        db.replace_state(user_id, "photo")
        await message.reply(f"Отправьте свое фото", reply_markup=ReplyKeyboardRemove())



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
            photo_blob = db.get_photo(user_id)
            write_to_file(photo_blob, f'photo{user_id}.jpeg')
            await message.reply(f"Ваше имя изменено!\n{get_profile(user_id)}", reply_markup=MENU_KB)
            await bot.send_photo(user_id, types.InputFile(f'img/photo{user_id}.jpeg'))
            os.remove(f"img/photo{user_id}.jpeg")
        else:
            await message.reply("Имя должно быть меньше 10 символов и начинаться с заглавной буквы")
    elif message.text == "Город" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_city")
        await message.reply("Введите новый город: ")
    elif db.get_state(user_id) == "edit_city" and message.text in CITIES:
        db.replace_state(user_id, "wait")
        db.replace_city(user_id, message.text)
        photo_blob = db.get_photo(user_id)
        write_to_file(photo_blob, f'photo{user_id}.jpeg')
        await message.reply(f"Ваш город изменен!\n{get_profile(user_id)}", reply_markup=MENU_KB)
        await bot.send_photo(user_id, types.InputFile(f'img/photo{user_id}.jpeg'))
        os.remove(f"img/photo{user_id}.jpeg")
    elif message.text == "Возраст" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_age")
        await message.reply("Введите новый возраст: ")
    elif db.get_state(user_id) == "edit_age":
        if message.text.isdigit() and 18 <= int(message.text) <= 80:
            db.replace_state(user_id, "wait")
            db.replace_age(user_id, message.text)
            photo_blob = db.get_photo(user_id)
            write_to_file(photo_blob, f'photo{user_id}.jpeg')
            await message.reply(f"Ваш возраст изменен!\n{get_profile(user_id)}", reply_markup=MENU_KB)
            await bot.send_photo(user_id, types.InputFile(f'img/photo{user_id}.jpeg'))
            os.remove(f"img/photo{user_id}.jpeg")
    elif message.text == "Описание" and db.get_state(user_id) == "edit":
        db.replace_state(user_id, "edit_desc")
        profile_list = db.get_my_profile(user_id)
        await message.reply(f"Прошлое описание: {profile_list[5]}\nВведите новое описание:")
    elif db.get_state(user_id) == "edit_desc":
        db.replace_state(user_id, "wait")
        db.replace_description(user_id, message.text)
        photo_blob = db.get_photo(user_id)
        write_to_file(photo_blob, f'photo{user_id}.jpeg')
        await message.reply(f"Ваше описание о себе изменено!\n{get_profile(user_id)}", reply_markup=MENU_KB)
        await bot.send_photo(user_id, types.InputFile(f'img/photo{user_id}.jpeg'))
        os.remove(f"img/photo{user_id}.jpeg")
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

    # Tags
    elif db.get_state(user_id) == "wait" and message.text == "Указать теги":
        db.replace_state(user_id, "tags")
        await message.reply("Выберите раздел: ", reply_markup=TAGS_KB)
    elif db.get_state(user_id) == "life_tags":
        answ = message.text
        l = from_str_to_list(answ)
        tags_obj = Read_tags(filename="other/life_tags.txt")
        tags_list = tags_obj.get_tags_list()
        my_tags = set(from_str_to_list(db.get_tags(user_id)))
        for tag in l:
            if tag in tags_list:
                my_tags.add(tag)
                await message.reply(f"{tag} добавлен!")
            else:
                await message.reply(f"{tag} не обнаружен")
        db.replace_tags(user_id, from_list_to_str(my_tags))
    elif db.get_state(user_id) == "music_tags":
        answ = message.text
        l = from_str_to_list(answ)
        tags_obj = Read_tags(filename="other/music_tags.txt")
        tags_list = tags_obj.get_tags_list()
        my_tags = set(from_str_to_list(db.get_tags(user_id)))
        for tag in l:
            if tag in tags_list:
                my_tags.add(tag)
                await message.reply(f"{tag} добавлен!")
            else:
                await message.reply(f"{tag} не обнаружен")
        db.replace_tags(user_id, from_list_to_str(my_tags))
    elif db.get_state(user_id) == "tags" and message.text == "Жизнь":
        db.replace_state(user_id, "life_tags")
        tags_obj = Read_tags(filename="other/life_tags.txt")
        tags_list = tags_obj.get_tags_list()
        await message.reply(f"Выберите теги из возможных:\n-----------\n"
                            f"{', '.join(tags_list)}", reply_markup=ReplyKeyboardRemove())
    elif db.get_state(user_id) == "tags" and message.text == "Жанры музыки":
        db.replace_state(user_id, "music_tags")
        tags_obj = Read_tags(filename="other/music_tags.txt")
        tags_list = tags_obj.get_tags_list()
        await message.reply(f"Выберите теги из возможных:\n-----------\n"
                            f"{', '.join(tags_list)}", reply_markup=ReplyKeyboardRemove())

    # GET TO KNOW
    elif db.get_state(user_id) == "wait" and message.text == "Познакомиться":
        info = db.get_random_profile(user_id)
        photo_blob = db.get_photo(info[0])
        write_to_file(photo_blob, f'photo{info[0]}.jpeg')
        await message.reply(f"{info[2]}\n{info[4]}\n{info[5]}\n{info[6]}\n{info[7]}")
        await bot.send_photo(user_id, types.InputFile(f'img/photo{info[0]}.jpeg'))
        os.remove(f"img/photo{info[0]}.jpeg")

    # FILTER PROFILES
    elif db.get_state(user_id) == "wait" and message.text == "Фильтр":
        db.replace_state(user_id, "filter")
        await message.reply("Выберите параметры для фильтрации анкет", reply_markup=FILTER_KB)

# PHOTO
@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    user_id = message.from_user.id
    if db.get_state(user_id) == "photo":
        await message.photo[-1].download(destination_file=f"img/photo{user_id}.jpeg")
        db.replace_state(user_id, "wait")
        db.replace_active(user_id, "true")
        db.replace_photo(user_id, convert_to_binary_data(f"photo{user_id}.jpeg"))
        photo_blob = db.get_photo(user_id)
        write_to_file(photo_blob, f'photo{user_id}.jpeg')
        await message.reply(get_profile(user_id), reply_markup=MENU_KB)
        await bot.send_photo(user_id, types.InputFile(f'img/photo{user_id}.jpeg'))
        os.remove(f"img/photo{user_id}.jpeg")





if __name__ == '__main__':
    executor.start_polling(dp)
