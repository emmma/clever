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
    return server.incoming(request)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/error')
def error():
    return render_template('error.html')

if __name__=='__main__':
    app.debug = True
    app.run()