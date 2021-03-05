import requests

data = {
    'name': 'Ivan',
    'text': 'testing...'
}
name = input('Введите имя: ')
while True:
    text = input('Введите сообщение: ')

    response = requests.post(
        'http://127.0.0.1:5000/send',
        # json=data
        json={
            'name': name,
            'text': text
        }
    )

