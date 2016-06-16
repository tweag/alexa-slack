import json

from flask import Flask, render_template, request

from pylexa.app import alexa_blueprint
from pylexa.response import AlexaResponseWrapper

from alexa_slack.constants import ALEXA_APP_ID


app = Flask(__name__)
alexa_blueprint.app_id = ALEXA_APP_ID
app.register_blueprint(alexa_blueprint)
app.response_class = AlexaResponseWrapper


@alexa_blueprint.before_request
def log_request_json():
    try:
        data = json.loads(request.get_data())
        sessionData = data.get('session', {})
        requestData = data.get('request', {})
        log_items = {
            'newSession': sessionData.get('new'),
            'sessionId': sessionData.get('sessionId'),
            'timestamp': requestData.get('timestamp'),
            'requestType': requestData.get('type')
        }
        if 'intent' in requestData:
            log_items['intent'] = requestData.get('intent', {}).get('name')
        print(
            ' '.join([
                '{}={}'.format(key, value)
                for key, value in sorted(log_items.items())
            ])
        )
    except Exception as ex:
        print('failed to log request: {}'.format(ex))


@app.route('/privacy')
def show_privacy_policy():
    return render_template('privacy_policy.html')


import alexa_slack.intent_handlers
import alexa_slack.oauth


if __name__ == '__main__':
    app.run(debug=True, port=8444)
