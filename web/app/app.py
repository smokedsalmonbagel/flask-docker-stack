from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta,datetime, date
import datetime
import time
import json,os
import pymysql
import prebuilt_loggers



app_log = prebuilt_loggers.filesize_logger('logs/app.log')
#create Flask app instance
app = Flask(__name__,static_url_path='')
application = app

app.secret_key = 'xfdgbsbW$^%W%Hwe57hE56yw56h'
app.config['SESSION_TYPE'] = 'filesystem'

sess = Session()
sess.init_app(app)



@app.route('/')
def index():
    return render_template('index.html')




# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
