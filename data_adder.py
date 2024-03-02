import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('db/database.db')
cursor = conn.cursor()


# Шаг 3: Добавление слов с учетом topic_id
words = [
    "the advent of personal computers",
    "information media",
    "to be quantitatively encoded as a series of ones and zeroes",
    "to accelerate the transmission and processing of information",
    "interactive consumer exchange for goods and information",
    "near-instant exchange of information",
    "the development of fiber optic cables",
    "digitization of information",
    "to have a profound impact on sth",
    "to be described in digital form",
    "to be embedded in",
    "machine-to-machine (M2M) technologies",
    "cognitive computing technologies/ a cognitive computing system",
    "robotic automation (in manufacturing facilities)",
    "to work through tasks without human intervention",
    "to function without human intervention",
    "to dramatically change the nature of work and other societal norms",
    "to automate some human tasks",
    "to collect and analyze an unprecedented volume of data",
    "to diagnose diseases and recommend the best treatments",
    "to lead to a high rate of unemployment",
    "programmable citywide testbed",
    "smart city infrastructure",
    "cloud infrastructure",
    "Wi-Fi (Wireless Fidelity) deployment",
    "mobile edge computing (MEC)",
    "5G network architecture",
    "small cell deployment",
    "internet connectivity",
    "gizmos and gadgets",
    "to facilitate communication between the user and the system",
    "wired and wireless systems"
]

translate = [
    "появление персональных компьютеров",
    "носители информации",
    "быть количественно закодированным как последовательность единиц и нулей",
    "ускорить передачу и обработку информации",
    "интерактивный потребительский обмен товарами и информацией",
    "практически мгновенный обмен информацией",
    "разработка оптоволоконных кабелей",
    "оцифровка информации",
    "оказывать сильное влияние на что-либо",
    "Описываться в цифровой форме",
    "быть встроенным",
    "межмашинное взаимодействие",
    "технология/система когнитивных вычислений",
    "роботизация (на производственных предприятиях)",
    "выполнять задачи без вмешательства человека",
    "функционировать без вмешательства человека",
    "резко изменить характер работы/труда и другие социальные нормы",
    "автоматизировать некоторые задачи, выполняемые человеком",
    "собирать и анализировать беспрецедентный объем данных",
    "диагностировать заболевания и рекомендовать лучшие методы лечения",
    "привести к высокому уровню безработицы",
    "программируемый общегородской испытательный стенд/модель, город как испытательный полигон",
    "инфраструктура умного/интеллектуального города",
    "облачная инфраструктура",
    "развертывание/размещение беспроводных точек доступа к сети Интернет",
    "технология мобильных граничных вычислений, граничные вычисления с множественным доступом",
    "архитектура мобильной сети 5G (пятого поколения)",
    "развертывание малых сот",
    "подключение к Интернету",
    "приспособления и устройства",
    "обеспечить взаимодействие между пользователем и системой",
    "проводные и беспроводные системы"
]

weight = [1] * len(words)
topic_id = 1
print(len(words))
print(len(translate))
words_data = list(zip(words, translate, weight, [topic_id] * len(words)))

cursor.executemany("INSERT INTO Words (word, translation, weight, topic_id) VALUES (?, ?, ?, ?);", words_data)

# # Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
