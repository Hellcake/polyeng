import random
import telebot
from telebot import types
import sqlite3
import os
import gtts
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.environ.get("TELEGRAM_BOT_API"))

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()


def handle_command(message):
    cursor.execute("SELECT * FROM Users WHERE user_id=?", (message.from_user.id,))
    result = cursor.fetchone()
    return result


def text_to_speech(text, language='en'):
    tts = gtts.gTTS(text, lang=language)
    filename = "output.mp3"  # You can change the filename
    tts.save(filename)
    return filename


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("a")
    markup.add(but1)

    bot.send_message(message.chat.id, "Выбери юнит:", reply_markup=markup, parse_mode='html')


def process_text_to_speech(message, text):
    audio_filename = text_to_speech(text)
    audio = open(audio_filename, 'rb')
    bot.send_voice(message.chat.id, audio)
    audio.close()
    os.remove(audio_filename)  # Remove temporary audio file


@bot.message_handler(
    func=lambda message: message.text in ['a'])
def choose_topic(message):
    user_id = message.from_user.id
    topic_name = message.text
    topic_id = switch_case(topic_name)

    cursor.execute("""SELECT COUNT(*) FROM UserWords WHERE user_id = ?;""", (user_id,))
    user_topic_exists = cursor.fetchone()[0]

    cursor.execute("""SELECT COUNT(*) FROM Users WHERE user_id = ?;""", (user_id,))
    user_topic_exists1 = cursor.fetchone()[0]

    if not user_topic_exists:
        cursor.execute("""
                INSERT INTO UserWords (user_id, word_id, usage_weight)
                SELECT ?, word_id, weight FROM Words;
            """, (user_id,))
        conn.commit()
    if not user_topic_exists1:
        cursor.execute("INSERT INTO Users (user_id, last_topic) VALUES (?, ?)", (user_id, topic_id,))
        conn.commit()
    cursor.execute("UPDATE Users SET last_topic = ? WHERE user_id = ?",
                   (topic_id, user_id,))
    conn.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("С английского")
    but2 = types.KeyboardButton("С русского")
    markup.add(but1, but2)
    bot.send_message(message.chat.id, "Выбери режим заучивания:", reply_markup=markup, parse_mode='html')


@bot.message_handler(func=lambda message: message.text in ['С английского', 'С русского'])
def choose_mode(message):
    if not handle_command(message):
        start(message)
        return
    mode = {'С английского': 'eng', 'С русского': 'ru'}.get(message.text)

    cursor.execute("""
                    SELECT last_topic
                    FROM Users
                    WHERE user_id = ?;
                """, (message.from_user.id,))
    last_info = cursor.fetchone()
    cursor.execute("UPDATE Users SET mode = ? WHERE user_id = ?", (mode, message.from_user.id))
    conn.commit()
    get_random_word(message.from_user.id, last_info[0], message)


def switch_case(argument):
    switch_dict = {
        'a': 1
    }

    return switch_dict.get(argument, "Invalid case")


def get_random_word(user_id, topic_id, message):
    cursor.execute("""
        SELECT Words.word,Words.translation, UserWords.usage_weight
        FROM Words
        JOIN UserWords ON Words.word_id = UserWords.word_id
        WHERE Words.topic_id = ? AND UserWords.user_id = ?;
    """, (topic_id, user_id,))

    words_with_weights = cursor.fetchall()
    cursor.execute("""
                    SELECT mode
                    FROM Users
                    WHERE user_id = ?;
                """, (message.from_user.id,))
    last_info = cursor.fetchone()[0]
    if words_with_weights:
        words, translation, usage_weights = zip(*words_with_weights)
        if last_info == "eng":
            selected_word = random.choices(words, usage_weights)[0]
        else:
            selected_word = random.choices(translation, usage_weights)[0]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Знаю")
        but2 = types.KeyboardButton("Не знаю")
        markup.add(but1, but2)
        but3 = types.KeyboardButton("Назад")
        markup.add(but3)
        bot.send_message(message.from_user.id, selected_word, reply_markup=markup, parse_mode='html')
        cursor.execute("UPDATE Users SET last_word = ? WHERE user_id = ? AND last_topic = ?",
                       (selected_word, user_id, topic_id))
        conn.commit()
        if last_info == "eng": process_text_to_speech(message, selected_word)
    else:
        return None


@bot.message_handler(func=lambda message: message.text in ['Знаю', 'Не знаю'])
def on_user_response(message):
    if not handle_command(message):
        start(message)
        return
    cursor.execute("""
                SELECT last_word, last_topic, mode
                FROM Users
                WHERE user_id = ?;
            """, (message.from_user.id,))
    last_info = cursor.fetchone()

    user_id = message.from_user.id
    if last_info[2] == "eng":
        cursor.execute("""
                    SELECT word_id, translation, weight
                    FROM Words
                    WHERE word = ?;
                """, (last_info[0],))
        word_info = cursor.fetchone()
    else:
        cursor.execute("""
                    SELECT word_id, word, weight
                    FROM Words
                    WHERE translation = ?;
                """, (last_info[0],))
        word_info = cursor.fetchone()

    if word_info is not None:
        cursor.execute("""
                                SELECT usage_weight
                                FROM UserWords
                                WHERE word_id = ? AND user_id = ?;
                            """, (word_info[0], user_id))
        w = cursor.fetchone()[0]

        if message.text == 'Знаю':
            word, translation, weight = word_info
            bot.send_message(message.from_user.id, f"Напоминаю🤓:\n{translation}", parse_mode='html')

            cursor.execute("UPDATE UserWords SET usage_weight = ? WHERE user_id = ? AND word_id = ?",
                           (w / 1.5, user_id, word_info[0]))
            conn.commit()
            if last_info[2] == "ru": process_text_to_speech(message, translation)

            get_random_word(user_id, last_info[1], message)

        if message.text == 'Не знаю':
            word, translation, weight = word_info
            bot.send_message(message.from_user.id, f"Перевод😉:\n{translation}", parse_mode='html')
            if last_info[2] == "ru": process_text_to_speech(message, translation)
            get_random_word(user_id, last_info[1], message)

    else:
        bot.send_message(message.from_user.id, f"Возникла ошибка\nПропиши /start", parse_mode='html')


@bot.message_handler(content_types=["text"])
def back(message):
    if message.text == 'Назад':
        start(message)


bot.polling(none_stop=True)
