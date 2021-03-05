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
