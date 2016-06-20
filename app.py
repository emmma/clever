from flask import Flask
from flask import request
from flask import render_template

import server

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/oauth', methods=['GET'])
def oauth():
    name = server.oauth(request)
    return render_template('results.html', name=name)


@app.route('/results')
def results(name=None):
    return render_template('results.html', name=name)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(debug=True, port=port)
