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
        return render_template('home.html', prediction=res)
    else:
        app.logger.info(res)
        return render_template('home.html', errorMessage=res)




if __name__ == '__main__':
    # predictions.load_network()
    app.run(debug=True)
