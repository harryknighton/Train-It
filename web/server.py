from flask import Flask, render_template, request
from math import ceil, floor
from datetime import datetime

import predictions
import sys

app = Flask(__name__,
            template_folder="templates")

@app.route('/')
def home():
    return render_template('home.html', delayColour="white")


@app.route('/handle_form', methods=['GET'])
def handle_form():
    # for key, value in request.args.items():
    #     print(key+' '+value, file=sys.stderr)
    listDate = [int(request.args['day']), int(request.args['month']), int(request.args['year'])]
    successFlag, res = predictions.process_request(request.args['source'],
                                                   request.args['destination'],
                                                   listDate,
                                                   request.args['time'])
    app.logger.info(res)
    if successFlag:
        message, colour = get_delay_str(res[0])
        return render_template('home.html',
                               prediction=message,
                               delayColour=colour,
                               weather=res[1],
                               source=request.args['source'],
                               destination=request.args['destination'],
                               date=get_date_string(listDate),
                               time=request.args['time'])
    else:
        return render_template('home.html', errorMessage=res, delayColour="white")


def get_delay_str(delay):
    seconds = int((abs(delay) % 1) * 60)
    if delay < 0:
        return "{}m {}s early".format(ceil(delay), seconds), '#7CFC00'
    elif delay == 0:
        return "No delay", '#7CFC00'
    elif delay <= 1:
        return "{}s late".format(seconds), 'orange'
    elif delay <= 5:
        return "{}m {}s late".format(floor(delay), seconds), 'orange'
    else:
        return "{}m {}s late".format(floor(delay), seconds), 'red'


def get_date_string(date):
    return "{}/{}/{}".format(date[0], date[1], date[2])


if __name__ == '__main__':
    predictions.load_network()
    app.run(debug=True)
