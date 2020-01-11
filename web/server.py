from flask import Flask, render_template, request

import predictions
import sys

app = Flask(__name__,
            template_folder="templates")

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/handle_form', methods=['GET'])
def handle_form():
    # for key, value in request.args.items():
    #     print(key+' '+value, file=sys.stderr)
    listDate = [int(request.args['day']), int(request.args['month']), int(request.args['year'])]
    successFlag, res = predictions.process_request(request.args['source'],
                                                   request.args['destination'],
                                                   listDate,
                                                   request.args['time'])
    if successFlag:
        app.logger.info(res)
        message = get_delay_str(res)
        return render_template('home.html', prediction=message)
    else:
        app.logger.info(res)
        return render_template('home.html', errorMessage=res)


def get_delay_str(delay):
    if delay < 0:
        return str(abs(delay)) + "m early"
    elif delay == 0:
        return "No delay"
    else:
        return str(delay) + "m late"


if __name__ == '__main__':
    predictions.load_network()
    app.run(debug=True)
