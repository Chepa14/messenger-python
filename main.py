import random
import datetime
from flask import Flask, request, abort
import time

app = Flask(__name__)

db = []


@app.route('/')
def hello():
    return 'Hello'


def check_data(data):
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)
    name, text = data['name'], data['text']
    if not isinstance(data['name'], str) or \
            not isinstance(data['text'], str) or \
            name == '' or text == '':
        return abort(400)
    return data


def activate_bot(message):
    sender = message['name']
    text = message['text']
    if '/help' in text:
        db.append({
            'name': '[Bot Walle]',
            'text': 'Тебя приветствует бот, который даст Вам ответ на вопросы! \n'
                    'Список доступных команд: \n'
                    '- /help (Информация о боте и его возможностях)\n'
                    '- /comp *Имя* (Определяет Вашу совместимость с выбранным именем)\n'
                    '- /8_ball *Вопрос* (Магический шар ответит на Ваш вопрос)\n'
                    '- /when *Вопрос* (Подскажет когда произойдет событие, о котором спрашиваете)\n'
                    '- /mark *Предмет* (Подскажет какую оценку по данному предмету Вы получите)\n'
                    '- /animal (Даст ответ на вопрос "Кто Вы из животных?)" \n'
                    'Пример запроса: /comp Мария,\t/when "Когда я женюсь?"\n',
            'time': time.time()
        })
        return
    if '/comp' in text:
        parsed = text.split(sep=' ')
        parsed = parsed[parsed.index('/comp'):]
        try:
            name = parsed[1]
        except:
            db.append({
                'name': '[Bot Walle]',
                'text': 'Вы ввели некорректный запрос! Попробуйте ещё раз',
                'time': time.time()
            })
            return
        n = random.randint(0, 100)
        if n < 30:
            output = '{0}, Ваша совместимость с {1}, к сожалению, равна {2}%.'.format(sender, name, n)
        elif n > 70:
            output = '{0}, у Вас прекрасная совместимость с {1}, равная {2}%!!!'.format(sender, name, n)
        else:
            output = '{0}, Ваша совместимость с {1} ни много ни мало - {2}%!'.format(sender, name, n)
        db.append({
            'name': '[Bot Walle]',
            'text': output,
            'time': time.time()
        })
        return
    if '/8_ball' in text:
        answers = ['Бесспорно', 'Предрешено', 'Никаких сомнений',
                   'Определённо да', 'Можешь быть уверен в этом',
                   'Мне кажется — «да»', 'Вероятнее всего', 'Хорошие перспективы',
                   '(Знаки говорят — «да»', 'Да', 'Лучше не рассказывать',
                   'Сейчас нельзя предсказать', 'Даже не думай', 'Мой ответ — «нет»',
                   'По моим данным — «нет»', '(Перспективы не очень хорошие',
                   'Весьма сомнительно']
        parsed = text.split(sep=' ', maxsplit=1)
        parsed = parsed[parsed.index('/8_ball'):]
        try:
            question = parsed[1]
        except:
            db.append({
                'name': '[Bot Walle]',
                'text': 'Вы ввели некорректный запрос! Попробуйте ещё раз',
                'time': time.time()
            })
            return
        db.append({
            'name': '[Bot Walle]',
            'text': 'Магический шар думает...',
            'time': time.time()
        })
        time.sleep(2.5)
        db.append({
            'name': '[Bot Walle]',
            'text': '"{0}" \n{1}!'.format(
                question, random.choice(answers)),
            'time': time.time()
        })
        return
    if '/when' in text:
        parsed = text.split(sep=' ', maxsplit=1)
        parsed = parsed[parsed.index('/when'):]
        try:
            question = parsed[1]
        except:
            db.append({
                'name': '[Bot Walle]',
                'text': 'Вы ввели некорректный запрос! Попробуйте ещё раз',
                'time': time.time()
            })
            return
        day = random.randint(1, 29)
        month = random.randint(1, 12)
        year = random.randint(2021, 2030)
        date = datetime.date(year, month, day)
        db.append({
            'name': '[Bot Walle]',
            'text': '"{0}" \nЖди {1}!'.format(
                question, date),
            'time': time.time()
        })
        return
    if '/mark' in text:
        parsed = text.split(sep=' ', maxsplit=1)
        parsed = parsed[parsed.index('/mark'):]
        try:
            subject = parsed[1]
        except:
            db.append({
                'name': '[Bot Walle]',
                'text': 'Вы ввели некорректный запрос! Попробуйте ещё раз',
                'time': time.time()
            })
            return
        n = random.randint(1, 5)
        db.append({
            'name': '[Bot Walle]',
            'text': 'Будь уверен, что по предмету "{0}" ты получишь {1} балл(-а/-ов)!'.format(
                subject, n),
            'time': time.time()
        })
        return
    if '/animal' in text:
        animals = ['Бизон', 'Дельфин', 'Орёл', 'Омар', 'Собака',
                   'Корова', 'Олень', 'Утка', 'Кролик',
                   'Волк', 'Лев', 'Свинья', 'Змея', 'Акула',
                   'Медведь', 'Курица', 'Лошадь', 'Кошка']
        db.append({
            'name': '[Bot Walle]',
            'text': f'Без сомнений Вы - {random.choice(animals)}!',
            'time': time.time()
        })
        return


@app.route('/send', methods=['POST'])
def send_message():
    data = check_data(request.json)
    name = data['name']
    text = data['text']
    message = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    db.append(message)
    activate_bot(message)
    return {'ok': True}


@app.route('/messages')
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)
    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(db) >= 100:
                break
    return {'messages': result}


@app.route('/status')
def status():
    return {
        'status': True,
        'name': 'Messenger',
        'time': time.time(),
        'count_of_messages': len(db),
        'users': len(set(msg['name'] for msg in db))
    }


app.run()
