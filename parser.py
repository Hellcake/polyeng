import re
#
# dict = {"a subject / discipline / course": "предмет / дисциплина / курс",
#         "a university campus / degree / professor / lecturer": "университетский городок / ученая степень / профессор / преподаватель",
#         "academic achievement": "академическая успеваемость", "bullying": "травля, запугивание",
#         "compulsory education": "обязательное образование",
#         "continuous assessment": "система непрерывного оценивания (когда академическая успеваемость и работа оцениваются на протяжении всего курса, а не только в конце)",
#         "a curriculum (plural curricula)": "учебный план",
#         "formal / informal learning": "формальное / неформальное обучение", "higher education": "высшее образование",
#         "a mixed school": "школа совместного обучения", "a primary / elementary school": "начальная школа",
#         "private education": "частное образование", "a secondary school": "средняя школа",
#         "a single-sex school": "школа раздельного обучения", "state / public education": "государственное образование",
#         "truancy": "прогул", "tuition fees": "плата за обучение",
#         "Peter the Great St. Petersburg Polytechnic University": "Санкт-Петербургский политехнический университет Петра Великого",
#         "to charge tuition fees / to charge no tuition fees": "взимать плату за обучение / не взимать плату за обучение",
#         "to do an exam": "сдавать экзамен", "to do coursework": "выполнять курсовую работу",
#         "to do homework": "делать домашнюю работу", "to do one’s best": "стараться изо всех сил",
#         "to drop out of school / a course": "бросить школу / курс обучения",
#         "to enroll in higher education": "поступить в высшее учебное заведение",
#         "to fail an exam / a course": "провалить экзамен / курс",
#         "to get / have a degree": "получить / иметь ученую степень",
#         "to get a good grade /result": "получить хорошую оценку / результат",
#         "to get a place at university": "получить место в университете",
#         "to get better exam results": "получить лучшие результаты экзамена", "to get on with people": "ладить с людьми",
#         "to get social experience": "получить социальный опыт",
#         "to go to / attend a seminar": "пойти на / посетить семинар",
#         "to go to school / college": "учиться в школе / колледже",
#         "to graduate from university": "закончить университет",
#         "to hand in an essay / an assignment": "сдать эссе / задание",
#         "to leave primary / secondary  school": "закончить начальную / среднюю школу",
#         "to make a mistake": "совершить ошибку", "to make progress": "делать успехи",
#         "to pass an exam / a course": "сдать экзамен / курс",
#         "to revise a subject": "повторять пройденный материал по предмету",
#         "to revise for an exam / a test": "подготовиться к экзамену / тесту", "to sit an exam": "сдавать экзамен",
#         "to speak in seminars": "выступать на семинарах",
#         "to start / begin primary / secondary  school": "начать обучение в начальной / средней школе",
#         "to study a subject / a language": "изучать предмет / язык", "to study at university": "учиться в университете",
#         "to take / retake an exam / a course": "сдать / пересдать экзамен / курс",
#         "to teach skills people need for the job": "обучать навыкам, необходимым людям для работы",
#         "an approach": "подход, метод", "to criticise": "критиковать",
#         "an educationalist": "педагог, деятель в области образования",
#         "environment": "окружающая среда, окружающая обстановка", "a method": "метод", "pace": "темп",
#         "punctual": "пунктуальный", "strict": "строгий", "unique": "уникальный",
#         "well-prepared": "хорошо подготовленный",
#         "to be based on cooperation rather than competition": "основываться на сотрудничестве, а не на конкуренции",
#         "to be good at answering questions": "хорошо отвечать на вопросы",
#         "to be well-prepared": "быть хорошо подготовленным", "to change the pace of the lesson": "изменять темп урока",
#         "to deal with truancy": "разобраться с прогулами",
#         "to develop social / observation skills": "развивать социальные навыки / навыки наблюдения",
#         "to explain things clearly": "объяснять ясно",
#         "to focus on students’ needs": "сосредоточиться на потребностях студентов",
#         "to give a lot of tests / homework": "давать много тестов / домашних заданий",
#         "to introduce videos, presentations and other documents": "представлять видеоролики, презентации и другие документы",
#         "to keep students interested": "поддерживать интерес студентов",
#         "to learn without being criticised or restricted": "учиться, не подвергаясь критике или ограничениям",
#         "to miss lessons": "пропускать уроки", "to offer a range of activities": "предлагать широкий спектр заданий",
#         "to provide students with individual learning programmes": "предоставлять студентам индивидуальные программы обучения",
#         "to study at your own pace": "учиться в своем собственном темпе",
#         "to treat all students equally": "относиться ко всем студентам одинаково",
#         "to treat students like unique individuals": "относиться к студентам как к уникальным личностям",
#         "to use different / traditional / innovative / interactive methods to teach students": "используйте различные / традиционные / инновационные / интерактивные методы обучения",
#         "to use lectures from free internet resources to support the curriculum": "использовать лекции из бесплатных интернет-ресурсов для поддержки учебной программы",
#         "a formal / informal approach to teaching": "формальный/неформальный подход к преподаванию",
#         "insufficient teacher training": "недостаточная подготовка учителей",
#         "lack of face-to-face contact": "отсутствие личного контакта", "a hall of residence": "студенческое общежитие",
#         "a loan": "кредит", "a privilege": "привилегия", "a right": "право",
#         "an undergraduate programme / degree / student": "программа бакалавриата / степень бакалавра / студент бакалавриата",
#         "a graduate programme / degree / student": "программа магистратуры / степень магистра / студент магистратуры",
#         "a spacious campus": "просторный университетский городок (кампус)",
#         "a peaceful atmosphere for studying": "спокойная атмосфера для учебы",
#         "a well-equipped lecture room": "хорошо оборудованная лекционная аудитория",
#         "a well-stocked library": "хорошо укомплектованная библиотека",
#         "a state-of the-art computer / physics / chemistry laboratory": "современная компьютерная / физическая / химическая лаборатория",
#         "excellent sports facilities": "отличные спортивные сооружения",
#         "to absorb the knowledge teachers give": "впитывать знания, которые дают учителя",
#         "to be interested in the subject you choose": "быть заинтересованым в выбранном вами",
#         "to bring enormous benefits to society": "приносить огромную пользу обществу",
#         "to create a new business": "создать новый бизнес",
#         "to do academic research": "проводить академические исследования",
#         "to expect a high / low / average starting salary": "ожидать высокую / низкую / среднюю стартовую зарплату",
#         "to get fringe benefits": "получать дополнительные льготы", "to get into debt": "залезть в долги",
#         "to have higher level of innovation and growth": "иметь более высокий уровень инноваций и роста",
#         "to have the same / different level of intelligence": "иметь одинаковый / разный уровень интеллекта",
#         "to need highly qualified people": "нуждаться в высококвалифицированных людях",
#         "to pay more tax": "платить больше налогов", "to pay off a university loan": "погасить университетский кредит",
#         "to produce educated and qualified workforce": "производить образованную и квалифицированную рабочую силу",
#         "to promote greater equality": "содействовать большему равенству",
#         "to study for a degree (in engineering, science, etc.)": "учиться на ученую степень (в области инженерного дела, естественных наук и т. д.)",
#         "to support a further increase in university fees": "поддержать дальнейшее увеличение платы за обучение в университете",
#         "to take out a loan to finance their studies": "взять кредит для финансирования своей учебы",
#         "a dog eat dog situation": "a situation in which people will do anything to be successful, even if what they do harms other people - ситуация, где каждый сам за себя",
#         "to burn the midnight oil": "to work late into the night -    усердно работать, засиживаясь допоздна",
#         "to give an edge over non-graduates": "дать преимущество над теми, кто не являются выпускниками университета",
#         "to hit the books": "to begin to study in a serious and determined way -   взятьcя зa книги, зa учёбу",
#         "to pass an exam with flying colours": "to pass an exam very successfully -  блестяще выдержать экзамен"}
# word = []
# translation = []
# items = dict.items()
# for item in items:
#     word.append(item[0]), translation.append(item[1])
#
#
# print(word)
# print(translation)

text = """1) accident – авария, катастрофа, несчастный случай
2) aircraft / spacecraft - воздушное судно / космический корабль
3) aircraft industry - авиационная промышленность
4) car manufacturing company – автомобилестроительная компания
5) commercial / military aircraft - коммерческий / военный самолет
6) to construct – сооружать, строить, возводить
7) engine – двигатель, машина, механизм
8) engineer – инженер, конструктор 
9) engineering – инженерное дело, машиностроение, техника
10) failure – неудача, сбой, отказ
11) head of engineering – руководитель инженерно-технического отдела
12) heart pacemaker - кардиостимулятор
13) household appliances - бытовая техника
14) mechanical engineering department – кафедра машиностроения 
15) microchip - микросхема
16) project management - управление проектами
17) well-paid / respected job - хорошо оплачиваемая / уважаемая работа
18) to be in a high position – занимать высокую должность
19) to control / prevent pollution – контролировать / предотвращать загрязнение
20) to create advanced technologies – создавать передовые технологии
21) to design new products – разрабатывать новые продукты
22) to develop new medicines - разрабатывать новые лекарства
23) to do / carry out research – проводить исследования
24) to explore new worlds – исследовать новые миры
25) to find new uses for old products – найти новое применение старым продуктам
26) to find a solution to a problem / to solve a problem – найти решение проблемы / решить проблему
27) to have practical experience – иметь практический опыт
28) to improve the way the world works – улучшить то, как устроен мир
29) to meet a deadline – уложиться в срок
30) to put smth into practice – применить что-то на практике
31) to study engineering at university - изучать инженерное дело в университете
32) to work in a test / research laboratory (lab) – работать в испытательной / исследовательской лаборатории                                                                                         
33) aeronautical engineering - авиационное машиностроение
34) aerospace engineering – аэрокосмическое машиностроение
34) biomedical engineering - биомедицинская инженерия
35) civil engineering - гражданское строительство
36) computer engineering - вычислительная техника
37) electrical engineering - электротехника
38) genetic engineering - генная инженерия
39) mechanical engineering – машиностроение
40) survival engineering - аварийно-спасательное оборудование и техника
41) alien invasion - инопланетное вторжение
42) asteroid - астероид
43) to collide - сталкиваться
44) collision - столкновение
45) to disintegrate – распадаться, разрушаться
46) to deflect - отклонять
47) deflection - отклонение
48) drought - засуха
49) earthquake - землетрясение
50) extinction – вымирание, исчезновение
51) famine - голод
52) flood - наводнение
53) hazardous - опасный
54) hurricane - ураган
55) meteor - метеор
56) missile – ракета, реактивный снаряд
57) meteorite - метеорит
58) overpopulation - перенаселение
59) probe - зонд
60) superbug - стойкая к лекарствам бактерия, вызывающая опасные заболевания
61) tsunami - цунами
62) volcano - вулкан 
63) to approach the Earth - приближаться к Земле
64) to avoid a collision - избежать столкновения
65) to build a model / prototype – построить модель / прототип
66) to burn up in the atmosphere - сгореть в атмосфере
67) to carry loads – выдерживать нагрузки
68) to cause an earthquake / a tsunami  - вызвать землетрясение / цунами
69) to change direction - изменить направление
70) to collide with the Earth - столкнуться с Землей
71) to do a safety / stress / fatigue test – проводить испытания на безопасность / нагрузочные испытания / усталостные испытания
72) to make a breakthrough – совершить порыв
73) to move through space – передвигаться в космосе
74) to prevent / avoid a collision - предотвратить столкновение / избежать столкновения
75) to test a model / prototype /theory – испытывать модель / прототип / проверить теорию
76) to travel at a speed of - передвигаться со скоростью
77) solar farm - солнечная ферма
78) solar panel - солнечная панель
79) wind farm - ветровая электростанция
80) hydro-electric dam - плотина гидроэлектростанции, гидроэлектростанция 
81) man-made structure - рукотворное сооружение
82) magnetically-raised train - поезд на магнитной подушке
83) to be attached to the anchor - быть прикрепленным к якорю
84) to be … metres high / long / wide / deep – составлять … метров в высоту / длину / ширину / глубину
85) to cover … square kilometres – покрывать … квадратных километров
86) to cut journey time - сократить время в пути
87) to depend on fossil fuels - зависеть от ископаемого топлива
88) to float in the ocean - плавать в океане
89) to generate / produce electricity – производить электричество 
90) to be sunk into the bottom of the sea - быть погруженным на дно моря
91) to solve climate change problems - решать проблемы изменения климата
92) to transport by a special ship – транспортировать на специальном судне
93) to give the country a sense of pride – дать стране чувство гордости
94) to stimulate the country’s economic growth - стимулировать экономический рост страны
95) to provide a wide range of jobs - обеспечить широкий спектр рабочих мест
1) to assess the feasibility of the project* - оценить осуществимость проекта
2) to be at the cutting edge of smth** - быть на переднем крае чего-либо 
3) to be out of order* – быть поврежденным, неисправным 
4) to blind someone with science** - заумно объяснять
5) to deliver electricity to consumers* - доставлять электричество потребителям 
6) to develop a mathematical model* - разработать математическую модель
7) to employ a steam engine to crack a nut** - стрелять из пушки по воробьям 
8) to get /give an electric shock* – получить удар / ударить током
9) to get / have a spare part* – получить / иметь запасную часть
10) to have specialised knowledge* – обладать специальными знаниями
11) to implement an engineering project* – осуществлять инженерно-технический проект
12) to implement state-of-the-art techniques* - внедрять самые современные технологии
13) to keep up to date with modern technologies* - идти в ногу с современными технологиями
14) to make a full size / production version* – изготовить полномасштабную / производственную версию
15) to make predictions about behavior*- делать прогнозы о поведении
16) to operate equipment* – управлять оборудованием
17) to put smth together* - собирать
18) to run on electricity* – работать на электричестве
19) to take smth to pieces* - разобрать что-то на части
20) to use high-powered instruments* - использовать мощные приборы
1) to control / prevent pollution – контролировать / предотвращать загрязнение
2) to create advanced technologies – создавать передовые технологии
3) to design new products – разрабатывать новые продукты
4) to develop new medicines - разрабатывать новые лекарства
5) to do / carry out research – проводить исследования
6) to explore new worlds – исследовать новые миры
7) to find new uses for old products – найти новое применение старым продуктам
8) to find a solution to a problem / to solve a problem – найти решение проблемы / решить проблему
9) to put smth into practice – применить что-то на практике
10) to work in a test / research laboratory (lab) – работать в испытательной / исследовательской лаборатории
1) to assess the feasibility of the project* - оценить осуществимость проекта
2) to blind someone with science** - заумно объяснять 
3) to build a model / prototype – построить модель / прототип
4) to develop a mathematical model* - разработать математическую модель
5) to do a safety / stress / fatigue test – проводить испытания на безопасность / нагрузочные испытания / усталостные испытания
6) to implement an engineering project* – осуществлять инженерно-технический проект
7) to make a full size / production version* – изготовить полномасштабную / производственную версию
8) to make predictions about behavior*- делать прогнозы о поведении
9) to test a model / prototype /theory – испытывать модель / прототип / проверить теорию
10) to use high-powered instruments* - использовать мощные приборы
1) to be at the cutting edge of smth** - быть на переднем крае чего-либо 
2) to be … metres high / long / wide / deep – составлять … метров в высоту / длину / ширину / глубину
3) to cover … square kilometres – покрывать … квадратных километров
4) to employ a steam engine to crack a nut** - стрелять из пушки по воробьям 
5) to implement state-of-the-art techniques* - внедрять самые современные технологии
6) to keep up to date with modern technologies* -  идти в ногу с современными технологиями
7) to solve climate change problems - решать проблемы изменения климата
8) to give the country a sense of pride – дать стране чувство гордости
9) to stimulate the country’s economic growth - стимулировать экономический рост страны
10) to provide a wide range of jobs - обеспечить широкий спектр рабочих мест
"""

text_without_numbers_and_brackets = re.sub(r'[\d()]+', '', text)
pattern = re.compile(r'(.+?) – (.+)')
matches = pattern.findall(text_without_numbers_and_brackets)

english_words = [match[0].strip() for match in matches]
translations = [match[1].strip() for match in matches]

print(english_words)
print(translations)
