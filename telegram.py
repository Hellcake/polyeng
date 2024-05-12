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
themes = ['All', 'Advert', 'Business', 'Design', 'Education', 'Personality', 'Language',
          'Travel', 'Work', 'Crime', 'Arts and media', 'Trends', 'Engineering']


def handle_command(message):
    cursor.execute("SELECT * FROM Users WHERE user_id=?", (message.from_user.id,))
    result = cursor.fetchone()
    return result


@bot.message_handler(func=lambda message: message.text in ["Вернуться в меню"])
def back(message):
    if message.text == "Вернуться в меню":
        start(message)


def text_to_speech(text, language='en'):
    tts = gtts.gTTS(text, lang=language)
    filename = "output.mp3"  # You can change the filename
    tts.save(filename)
    return filename


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but = []
    for i in themes:
        but.append(types.KeyboardButton(i))
    markup.add(but[1], but[2], but[3])
    markup.add(but[4], but[5], but[6])
    markup.add(but[7], but[8], but[9])
    markup.add(but[10], but[11], but[12])
    markup.add(but[0])

    bot.send_message(message.chat.id, "Выбери юнит", reply_markup=markup, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message):
        bot.send_message(message.chat.id, "Привет! На данный момент доступно два режима: Квиз и Знаю / не знаю. Знаю / не знаю - режим заучивания, бот присылает слова по заданному юниту в выбранном режиме: на русском или английском. Квиз - режим проверки своих знаний в режиме викторины, также доступен на русском и английском.",  parse_mode='html')

def process_text_to_speech(message, text):
    audio_filename = text_to_speech(text)
    audio = open(audio_filename, 'rb')
    bot.send_voice(message.chat.id, audio)
    audio.close()
    os.remove(audio_filename)  # Remove temporary audio file


def switch_case(argument):
    switch_dict = {
        'All': 0,
        'Advert': 1,
        'Business': 2,
        'Design': 3,
        'Education': 4,
        'Personality': 5,
        'Language': 6,
        'Travel': 7,
        'Work': 8,
        'Crime': 9,
        'Arts and media': 10,
        'Trends': 11,
        'Engineering': 12
    }

    return switch_dict.get(argument, "Invalid case")


@bot.message_handler(
    func=lambda message: message.text in themes)
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
    but1 = types.KeyboardButton('Квиз')
    but2 = types.KeyboardButton('Знаю / не знаю')
    but3 = types.KeyboardButton("Вернуться в меню")
    markup.add(but1, but2)
    markup.add(but3)
    bot.send_message(message.chat.id, 'Выбери режим', reply_markup=markup, parse_mode='html')


@bot.message_handler(func=lambda message: message.text in ['Квиз', 'Знаю / не знаю', 'Добавим позже'])
def choose_mode(message):
    if not handle_command(message):
        start(message)
        return
    mode = {'Квиз': 'quiz', 'Знаю / не знаю': 'knowable', 'Добавим позже': 'any'}.get(message.text)

    cursor.execute("UPDATE Users SET mode = ? WHERE user_id = ?", (mode, message.from_user.id))
    conn.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('C английского на русский')
    but2 = types.KeyboardButton('С русского на английский')
    markup.add(but1, but2)
    bot.send_message(message.chat.id, "Выбери язык",
                     reply_markup=markup, parse_mode='html')


@bot.message_handler(func=lambda message: message.text in ['C английского на русский', 'С русского на английский'])
def choose_language(message):
    if not handle_command(message):
        start(message)
        return
    lang = {'C английского на русский': 'eng', 'С русского на английский': 'ru'}.get(message.text)

    cursor.execute("UPDATE Users SET lang = ? WHERE user_id = ?", (lang, message.from_user.id))
    conn.commit()

    cursor.execute("""
                    SELECT mode, last_topic
                    FROM Users
                    WHERE user_id = ?;
                """, (message.from_user.id,))
    current_mode = cursor.fetchone()

    start_game(message, current_mode[0], lang, current_mode[1])


def start_game(message, mode, lang, topic):
    if mode == 'quiz':
        quiz(message, topic, lang)
    elif mode == 'knowable':
        get_random_word(message.from_user.id, topic, message)
    elif mode == 'any':
        bot.send_message(message.from_user.id, 'Ожидайте обновлений ;)')


def get_phrase(message, topic_id, lang):
    if topic_id == '0':
        cursor.execute("""
                SELECT Words.word,Words.translation, UserWords.usage_weight
                FROM Words
                JOIN UserWords ON Words.word_id = UserWords.word_id
                WHERE UserWords.user_id = ?;
            """, (message.from_user.id,))
    else:
        cursor.execute("""
            SELECT Words.word,Words.translation, UserWords.usage_weight
            FROM Words
            JOIN UserWords ON Words.word_id = UserWords.word_id
            WHERE Words.topic_id = ? AND UserWords.user_id = ?;
        """, (topic_id, message.from_user.id,))
    words_with_weights = cursor.fetchall()

    if words_with_weights:
        _, _, usage_weights = zip(*words_with_weights)
        if lang == "eng":
            select = random.choices(words_with_weights, usage_weights)
        else:
            select = random.choices(words_with_weights, usage_weights)
    return select[0]


def quiz(message, topic_id, lang):
    flag = 1 if lang == 'eng' else 0
    main_phrase = get_phrase(message, topic_id, lang)  # фраза которую будем переводить
    options = [main_phrase[flag]]  # варианты ответа
    for _ in range(3):
        cur = get_phrase(message, topic_id, lang)[flag]
        while cur in options:
            cur = get_phrase(message, topic_id, lang)[flag]
        options.append(cur)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = []
    for _ in range(4):
        t = random.choice(options)
        button.append(types.KeyboardButton(t))
        options.remove(t)
    markup.add(button[0], button[1])
    markup.add(button[2], button[3])
    markup.add("Вернуться в меню")
    bot.send_message(message.from_user.id, main_phrase[abs(flag - 1)], reply_markup=markup, parse_mode='html')
    cursor.execute("UPDATE Users SET last_word = ? WHERE user_id = ? AND last_topic = ?",
                   (main_phrase[abs(flag - 1)], message.from_user.id, topic_id))
    conn.commit()


def get_random_word(user_id, topic_id, message):
    if topic_id == '0':
        cursor.execute("""
                SELECT Words.word,Words.translation, UserWords.usage_weight
                FROM Words
                JOIN UserWords ON Words.word_id = UserWords.word_id
                WHERE UserWords.user_id = ?;
            """, (user_id,))
    else:
        cursor.execute("""
            SELECT Words.word,Words.translation, UserWords.usage_weight
            FROM Words
            JOIN UserWords ON Words.word_id = UserWords.word_id
            WHERE Words.topic_id = ? AND UserWords.user_id = ?;
        """, (topic_id, user_id,))

    words_with_weights = cursor.fetchall()
    cursor.execute("""
                    SELECT lang
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
        but3 = types.KeyboardButton("Вернуться в меню")
        markup.add(but1, but2)
        markup.add(but3)
        bot.send_message(message.from_user.id, selected_word, reply_markup=markup, parse_mode='html')
        cursor.execute("UPDATE Users SET last_word = ? WHERE user_id = ? AND last_topic = ?",
                       (selected_word, user_id, topic_id))
        conn.commit()
        if last_info == "eng": process_text_to_speech(message, selected_word)
    else:
        return None


@bot.message_handler(content_types=['text'])
def on_user_response(message):
    if not handle_command(message):
        start(message)
        return
    cursor.execute("""
                SELECT last_word, last_topic, lang, mode
                FROM Users
                WHERE user_id = ?;
            """, (message.from_user.id,))
    last_info = cursor.fetchone()
    phrase, cur_topic, cur_lang, cur_mode = last_info
    user_id = message.from_user.id

    if cur_lang == "eng":
        cursor.execute("""
                    SELECT word_id, translation, weight
                    FROM Words
                    WHERE word = ?;
                """, (phrase,))
        word_info = cursor.fetchone()
        translation = word_info[1]
    else:
        cursor.execute("""
                    SELECT word_id, word, weight
                    FROM Words
                    WHERE translation = ?;
                """, (phrase,))
        word_info = cursor.fetchone()
        translation = word_info[1]

    if cur_mode == 'knowable':

        if word_info is not None:
            cursor.execute("""
                                    SELECT usage_weight
                                    FROM UserWords
                                    WHERE word_id = ? AND user_id = ?;
                                """, (word_info[0], user_id))
            w = cursor.fetchone()[0]

            if message.text == 'Знаю':
                bot.send_message(message.from_user.id, f"Напоминаю🤓:\n{translation}", parse_mode='html')

                cursor.execute("UPDATE UserWords SET usage_weight = ? WHERE user_id = ? AND word_id = ?",
                               (w / 1.5, user_id, word_info[0]))
                conn.commit()
                if cur_lang == "ru": process_text_to_speech(message, translation)

                get_random_word(user_id, cur_topic, message)

            if message.text == 'Не знаю':
                bot.send_message(message.from_user.id, f"Перевод😉:\n{translation}", parse_mode='html')
                if cur_lang == "ru": process_text_to_speech(message, translation)
                get_random_word(user_id, cur_topic, message)

        else:
            bot.send_message(message.from_user.id, f"Возникла ошибка\nПропиши /start", parse_mode='html')

    elif cur_mode == 'quiz':
        if message.text == translation or message.text == phrase:
            bot.send_message(message.from_user.id, 'Верно!', parse_mode='html')
        else:
            bot.send_message(message.from_user.id, f'Неверно! Правильный перевод - {translation}', parse_mode='html')
        quiz(message, cur_topic, cur_lang)


bot.infinity_polling()
