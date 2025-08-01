import re
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()

text = """
Встреча с Ивановым Иваном Ивановичем прошла успешно.
Сегодня встретил Петрову Марию Сергеевну.
Обсуждали начальника УМВД РФ  Сидорова Алексея Михайловича.
Позже говорили о Смирнове Сергее Зелимхановиче.
"""

pattern = r'([А-ЯЁ][а-яё]+)\s([А-ЯЁ][а-яё]+)\s([А-ЯЁ][а-яё]+)'
matches = re.findall(pattern, text)

def is_patronymic(word):
    patronymic_endings = [
        # Мужские
        "ович", "евич", "ич",  # Именительный мужской
        "овича", "евича", "ича",  # Родительный мужской
        "овича", "евича", "ича",  # Винительный мужской

        # Женские
        "овна", "евна", "ична", "инична",  # Именительный женский
        "овны", "евны", "ичны", "иничны",  # Родительный женский
        "овну", "евну", "ичну", "иничну",  # Винительный женский
    ]
    parse = morph.parse(word)[0]
    if 'Patr' in parse.tag:
        return True
    for ending in patronymic_endings:
        if word.endswith(ending) and len(word) > len(ending) + 1:
            return True
    return False

for surname, name, patronymic in matches:
    parsed_surname = morph.parse(surname)[0]
    parsed_name = morph.parse(name)[0]
    parsed_patronymic = morph.parse(patronymic)[0]
    if is_patronymic(patronymic):
        print(f"Фамилия: {parsed_surname.inflect({'nomn'}).word.title()}, Имя: {parsed_name.inflect({'nomn'}).word.title()}, Отчество: {parsed_patronymic.inflect({'nomn'}).word.title()}")
