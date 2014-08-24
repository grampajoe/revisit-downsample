from flask import Flask


app = Flask('downsample')


@app.route('/')
def index():
    return 'Wow!!!!!'
