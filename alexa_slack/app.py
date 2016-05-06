# -*- coding: utf-8 -*-
from collections import OrderedDict
from urllib import urlencode
import os

from flask import Flask, redirect, request
import requests

from pylexa.app import alexa_blueprint, handle_launch_request
from pylexa.intent import handle_intent
from pylexa.response import (
    AlexaResponseWrapper, LinkAccountCard, PlainTextSpeech, Response
)


app = Flask(__name__)
app.register_blueprint(alexa_blueprint)
app.response_class = AlexaResponseWrapper

AWS_VENDOR_ID = os.getenv('AWS_VENDOR_ID')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', 'botstuff')


@app.before_request
def log_request_json():
    print request.headers
    print request.json


@handle_launch_request
def handle_launch(request):
    return PlainTextSpeech('Launching Slack bot')


@handle_intent('SetChannel')
def handle_set_channel_intent(request):
    channel = request.slots.get('channel')
    return Response(
        speech=PlainTextSpeech('Did you say {}?'.format(channel)),
        should_end_session=False,
        session={'confirming_channel': True, 'channel': channel}
    )


@handle_intent('SetMessage')
def handle_set_message_intent(request):
    message = request.slots.get('message')
    channel = request.session.get('channel')
    return Response(
        speech=PlainTextSpeech('Great. Would you like me to post {} to {}'.format(message, channel)),
        session={'channel': channel, 'message': message, 'confirming_message': True},
        should_end_session=False,
    )


@handle_intent('AMAZON.YesIntent')
def handle_confirmation(request):
    if request.session.get('confirming_channel'):
        channel = request.session.get('channel', 'unknown channel')
        return Response(
            speech=PlainTextSpeech('What would you like to post?'),
            reprompt=PlainTextSpeech('Say the message you would like me to post'),
            session=request.session,
            should_end_session=False,
        )
    elif request.session.get('confirming_message'):
        return post_to_slack(request)
    else:
        return PlainTextSpeech('Ooops')


def post_to_slack(request):
    channel = request.session.get('channel')
    text = request.session.get('message')
    token = request.access_token
    url = 'https://slack.com/api/chat.postMessage'
    res = requests.post(url, {
        'token': token,
        'channel': channel,
        'text': text,
        # 'as_user': False,
        # 'username': 'Benevolent Robot Foosball Overlord',
    })
    if res.json()['ok']:
        return PlainTextSpeech("Okay. It's done.")
    else:
        return PlainTextSpeech('Oops, something went wrong.')


@handle_intent('StartMessage')
def handle_start_message(request):
    if not request.access_token:
        return Response(
            speech=PlainTextSpeech('You must sign in first'),
            card=LinkAccountCard(),
        )
    speech = PlainTextSpeech('What channel would you like to post to?')
    reprompt = PlainTextSpeech('Say the name of the channel you would like to post to')
    return Response(speech=speech, reprompt=reprompt, should_end_session=False)


@handle_intent('unrecognized_intent')
def handle_unrecognized_intent(request):
    return PlainTextSpeech("I'm sorry I didn't understand that")


@app.route('/oauth/entry')
def oauth_entry_point():
    client_id = request.args.get('client_id')
    scope = request.args.get('scope')
    state = request.args.get('state')
    url = 'https://slack.com/oauth/authorize'
    query_string = urlencode(OrderedDict(
        scope=scope,
        state=state,
        client_id=client_id
    ))
    redirect_url = '{}?{}'.format(url, query_string)
    return redirect(redirect_url)


@app.route('/oauth/redirect')
def oauth_redirect():
    state = request.args.get('state')
    code = request.args.get('code')

    response = requests.get(
        'https://slack.com/api/oauth.access?{}'.format(urlencode({ 'code': code })),
        auth=(SLACK_CLIENT_ID, SLACK_CLIENT_SECRET)
    )
    response_json = response.json()
    access_token = response_json.get('access_token')

    redirect_url = 'https://pitangui.amazon.com/spa/skill/account-linking-status.html?vendorId={}'.format(AWS_VENDOR_ID)
    redirect_url += '#{}'.format(urlencode({'access_token': access_token, 'state': state, 'token_type': 'Bearer'}))
    return redirect(redirect_url)


if __name__ == '__main__':
    app.run(debug=True, port=8444)
