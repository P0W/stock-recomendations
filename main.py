## Author : Prashant Srivastava
## Dated: November 29th 2020

import json
from flask import Flask, render_template, request
from _parseTickerTapeRecs import *
import os
import datetime
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def updateDatabases():
    createDataBase('stocksLargeCap', htmlPath)
    createDataBase('stocksMidCap', midCap150htmlPage)


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateDatabases, trigger="cron", hour='13', minute='30')
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%A, %d. %B %Y %I:%M:%S %p")


app = Flask(__name__)


@app.route("/",  methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        lastModifiedTime = modification_date('stocksLargeCap.db')
        data = {'chart_data': getData(
            'stocksLargeCap', 15), 'lastModifiedTime': lastModifiedTime}
        return render_template("index.html", data=data)
    else:
        pass


@app.route('/MoreData/<jsdata>')
def MoreData(jsdata):
    jsdata = json.loads(jsdata)
    db = jsdata['stocksDBVal']
    if db == 'stocksMidCap' or db == 'stocksLargeCap':
        data = {'chart_data': getData(
            jsdata['stocksDBVal'], jsdata['stockCount'])}
        return data
    return []


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8081, debug=True)
