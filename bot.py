import telebot
from telebot import types
import sqlite3

API_TOKEN = '7478443998:AAFuq6ZE_1yDiUX4YAHgyYa_kVYCcrYed7A'
bot = telebot.TeleBot(API_TOKEN)

user_data = {}

def save_question(user_id, question):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (user_id, question)
        VALUES (?, ?)
    ''', (user_id, question))
    conn.commit()
    conn.close()

def start_survey(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Рэп')
    itembtn2 = types.KeyboardButton('Рок')
    itembtn3 = types.KeyboardButton('Поп')
    itembtn4 = types.KeyboardButton('Классика')
    itembtn5 = types.KeyboardButton('Хип-хоп')
    itembtn6 = types.KeyboardButton('Электроника')
    itembtn7 = types.KeyboardButton('Другой вариант')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
    msg = bot.send_message(message.chat.id, 'Выберите ваш любимый жанр музыки:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_genre)

def process_genre(message):
    user_id = message.from_user.id
    genre = message.text
    user_data[user_id]['genre'] = genre

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Начинающий')
    itembtn2 = types.KeyboardButton('Средний')
    itembtn3 = types.KeyboardButton('Продвинутый')
    markup.add(itembtn1, itembtn2, itembtn3)
    msg = bot.send_message(message.chat.id, 'Выберите ваш уровень навыков:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_level)

def process_level(message):
    user_id = message.from_user.id
    level = message.text
    user_data[user_id]['level'] = level

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    markup.add(itembtn1, itembtn2)
    msg = bot.send_message(message.chat.id, 'Работали ли вы на студии?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_studio)

def process_studio(message):
    user_id = message.from_user.id
    studio = message.text
    user_data[user_id]['studio'] = studio

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    markup.add(itembtn1, itembtn2)
    msg = bot.send_message(message.chat.id, 'Писали ли вы свою музыку?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_written_music)

def process_written_music(message):
    user_id = message.from_user.id
    written_music = message.text
    user_data[user_id]['written_music'] = written_music

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Да')
    itembtn2 = types.KeyboardButton('Нет')
    markup.add(itembtn1, itembtn2)
    msg = bot.send_message(message.chat.id, 'Хотели бы вы написать свой альбом?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_album)

def process_album(message):
    user_id = message.from_user.id
    album = message.text
    user_data[user_id]['album'] = album

    bot.send_message(message.chat.id, 'Ваш профиль успешно создан! 🎉')
    show_main_menu(message)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    user_data[user_id] = {'name': first_name}

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Создать профиль')
    markup.add(itembtn1)

    with open('welcome.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=f"Добро пожаловать, {first_name}! 🎶 Ваш персональный помощник в создании музыки. Пожалуйста, создайте свой профиль.", reply_markup=markup)
    
    bot.send_message(message.chat.id, "Искусственный интеллект будет использовать ваши ответы для формирования персонализированного подбора видеоматериалов на основе нашей базы данных.")

@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.text == 'Создать профиль':
        create_profile(message)
    elif message.text == '🎵 Просмотреть материалы':
        show_materials_menu(message)
    elif message.text == '❓ Задать вопрос':
        ask_question(message)
    elif message.text == '👤 Мой профиль':
        view_profile(message)
    elif message.text == '⚙️ Настройки':
        settings(message)
    else:
        bot.reply_to(message, 'Извините, я вас не понял.')

def create_profile(message):
    start_survey(message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('🎵 Просмотреть материалы')
    itembtn2 = types.KeyboardButton('❓ Задать вопрос')
    itembtn3 = types.KeyboardButton('👤 Мой профиль')
    itembtn4 = types.KeyboardButton('⚙️ Настройки')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)

def show_materials_menu(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('📚 Аудио материалы', callback_data='audio_materials')
    itembtn2 = types.InlineKeyboardButton('📹 Видео материалы', callback_data='video_materials')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, 'Выберите тип материалов:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['audio_materials', 'video_materials'])
def show_materials(call):
    if call.data == 'audio_materials':
        bot.send_message(call.message.chat.id, 'Вот ваши аудио материалы:')
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('Эксперт 1 - Создание музыки с нуля', callback_data='audio_expert_1')
        itembtn2 = types.InlineKeyboardButton('Эксперт 2 - Запись на студии новичка', callback_data='audio_expert_2')
        markup.add(itembtn1, itembtn2)
        bot.send_message(call.message.chat.id, 'Выберите материал:', reply_markup=markup)
    elif call.data == 'video_materials':
        bot.send_message(call.message.chat.id, 'Вот ваши видео материалы:')
        markup = types.InlineKeyboardMarkup()
        itembtn1 = types.InlineKeyboardButton('Эксперт 1 - Создание музыки с нуля', callback_data='video_expert_1')
        itembtn2 = types.InlineKeyboardButton('Эксперт 2 - Запись на студии новичка', callback_data='video_expert_2')
        markup.add(itembtn1, itembtn2)
        bot.send_message(call.message.chat.id, 'Выберите материал:', reply_markup=markup)

def ask_question(message):
    msg = bot.send_message(message.chat.id, 'Введите ваш вопрос:')
    bot.register_next_step_handler(msg, process_question)

def process_question(message):
    user_id = message.from_user.id
    question = message.text
    save_question(user_id, question)
    bot.send_message(message.chat.id, 'Ваш вопрос отправлен экспертам. Спасибо!')

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn = types.KeyboardButton('⬅️ Главное меню')
    markup.add(itembtn)
    bot.send_message(message.chat.id, 'Нажмите кнопку ниже, чтобы вернуться в главное меню.', reply_markup=markup)

def view_profile(message):
    user_id = message.from_user.id
    profile_info = f"Имя: {user_data[user_id]['name']}\nПредпочтения: {user_data[user_id].get('preferences', 'Не указано')}\nУровень навыков: {user_data[user_id].get('skill_level', 'Не указано')}"
    bot.send_message(message.chat.id, profile_info)

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn = types.KeyboardButton('⬅️ Главное меню')
    markup.add(itembtn)
    bot.send_message(message.chat.id, 'Нажмите кнопку ниже, чтобы вернуться в главное меню.', reply_markup=markup)

def settings(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('🔔 Уведомления')
    itembtn2 = types.KeyboardButton('🌐 Язык интерфейса')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, 'Настройки:', reply_markup=markup)

    markup_back = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn = types.KeyboardButton('⬅️ Главное меню')
    markup_back.add(itembtn)
    bot.send_message(message.chat.id, 'Нажмите кнопку ниже, чтобы вернуться в главное меню.', reply_markup=markup_back)

@bot.callback_query_handler(func=lambda call: call.data.startswith('audio_expert') or call.data.startswith('video_expert'))
def handle_expert_selection(call):
    if call.data.startswith('audio_expert'):
        expert_number = call.data.split('_')[-1]
        bot.send_message(call.message.chat.id, f'Вы выбрали аудио материал: Эксперт {expert_number}')
    elif call.data.startswith('video_expert'):
        expert_number = call.data.split('_')[-1]
        bot.send_message(call.message.chat.id, f'Вы выбрали видео материал: Эксперт {expert_number}')

bot.polling()