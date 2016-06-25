import logging
import json
import sys

from flask import Flask, render_template, request

from pylexa.app import alexa_blueprint

from alexa_slack.constants import ALEXA_APP_ID


app = Flask(__name__)
app.config['app_id'] = ALEXA_APP_ID
app.register_blueprint(alexa_blueprint)
logger = app.logger


@app.before_first_request
def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@app.before_request
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
            intent = requestData.get('intent', {})
            log_items['intent'] = intent.get('name')
            log_items['slots'] = json.dumps(intent.get('slots'))
        logger.info('Got request: %s', ' '.join([
            '{}={}'.format(key, value)
            for key, value in sorted(log_items.items())
        ]))
    except Exception as ex:
        logger.info('failed to log request: %s', ex)


@app.route('/privacy')
def show_privacy_policy():
    return render_template('privacy_policy.html')


import alexa_slack.intent_handlers
import alexa_slack.oauth


if __name__ == '__main__':
    app.run(debug=True, port=8444)
