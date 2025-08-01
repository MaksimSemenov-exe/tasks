import re

def extract_fio(text):

  patterns = [
      r"([а-яё-]+)\s+([а-яё-]+)\s*([а-яё-]+)?",  # Строчные
      r"([А-ЯЁ-]+)\s+([А-ЯЁ-]+)\s*([А-ЯЁ-]+)?",  # Заглавные
      r"([А-ЯЁ][а-яё-]+)\s+([А-ЯЁ][а-яё-]+)\s*([А-ЯЁ][а-яё-]+)?"  # С заглавной
  ]

  fio_list = []
  for pattern in patterns:
    matches = re.findall(pattern, text)
    for match in matches:
      if len(match) >= 2:  
        surname, name, patronymic = match[0], match[1], match[2] if len(match) > 2 else None

        if patronymic and is_patronymic(patronymic):
          fio = tuple(word.title() for word in [surname, name, patronymic])
          if fio not in fio_list:
            fio_list.append(fio)
        elif not patronymic:
          fio = tuple(word.title() for word in [surname, name])
          if fio not in fio_list:
            fio_list.append(fio)

  return fio_list

def is_patronymic(word):
    word = word.lower()
    patronymic_endings = [
        # Мужские
        "ович", "евич", "ич", "овыч",
        "овича", "евича", "ича", "овыча",
        "овичем", "евичем", "ичем", "овычем",
        "овичу", "евичу", "ичу",
        "овиче", "евиче", "иче", "овыче",

        # Женские
        "овна", "евна", "ична", "инична",
        "овны", "евны", "ичны", "иничны",
        "овне", "евне", "ичне", "иничне",
        "овну", "евну", "ичну", "иничну",
        "овной", "евной", "ичной", "иничной",
    ]

    for ending in patronymic_endings:
        if word.endswith(ending) and len(word) > len(ending) + 1:
            return True
    return False



text = """
Встреча с Ивановым Иваном Ивановичем прошла успешно.
Сегодня встретил Петрову Марию Сергеевну.
Обсуждали начальника УМВД РФ  Сидорова Алексея Михайловича.
Позже говорили о смирнове сергее зелимхановиче.
"""
fio_list = extract_fio(text)

for fio in fio_list:
  print(" ".join(fio))
