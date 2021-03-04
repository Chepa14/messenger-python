from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, World!"


@app.route('/page2')
def page2():
    return "Hello, Second World!"


app.run()