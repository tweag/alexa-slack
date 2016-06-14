from flask import Flask, render_template, request

from pylexa.app import alexa_blueprint
from pylexa.response import AlexaResponseWrapper

from alexa_slack.constants import ALEXA_APP_ID


app = Flask(__name__)
alexa_blueprint.app_id = ALEXA_APP_ID
app.register_blueprint(alexa_blueprint)
app.response_class = AlexaResponseWrapper


@app.before_request
def log_request_json():
    print request.headers
    print request.get_data()


@app.route('/privacy')
def show_privacy_policy():
    return render_template('privacy_policy.html')


import alexa_slack.intent_handlers
import alexa_slack.oauth


if __name__ == '__main__':
    app.run(debug=True, port=8444)
