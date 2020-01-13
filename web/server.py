from flask import Flask, render_template, request
from math import ceil, floor

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
        message, colour = get_delay_str(res)
        return render_template('home.html', prediction=message, delayColour=colour)
    else:
        return render_template('home.html', errorMessage=res, delayColour="white")


def get_delay_str(delay):
    seconds = int((abs(delay) % 1) * 60)
    if delay < 0:
        return "{}m {}s early".format(ceil(delay), seconds), 'green'
    elif delay == 0:
        return "No delay", 'green'
    elif delay <= 0.5:
        return "{}s late".format(seconds), 'green'
    elif delay <= 2:
        return "{}m {}s late".format(floor(delay), seconds), 'orange'
    else:
        return "{}m {}s late".format(floor(delay), seconds), 'red'



if __name__ == '__main__':
    predictions.load_network()
    app.run(debug=True)
