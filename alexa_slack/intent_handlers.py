from pylexa.app import handle_launch_request
from pylexa.intent import handle_intent
from pylexa.response import LinkAccountCard, PlainTextSpeech, Response

from alexa_slack.slack import post_to_slack


def make_set_channel_response(message=None, retry=False):
    text = 'What channel would you like to post your message to?'
    if retry:
        text = "Ok, let's try that again. {}".format(text)
    speech = PlainTextSpeech(text)
    reprompt = PlainTextSpeech('Say the name of the channel you would like to post to')
    session = {
        'message': message,
    }
    return Response(speech=speech, reprompt=reprompt, should_end_session=False, session=session)


def make_set_message_response(channel, retry=False):
    text = 'What would you like to post?'
    if retry:
        text = "Ok, let's try that again. {}".format(text)
    return Response(
        speech=PlainTextSpeech(text),
        reprompt=PlainTextSpeech('Say the message you would like me to post'),
        session={'channel': channel},
        should_end_session=False,
    )


def make_confirm_message_response(message, channel):
    return Response(
        speech=PlainTextSpeech('Great. Would you like me to post {} to {}?'.format(message, channel)),
        session={'channel': channel, 'message': message, 'confirming_message': True},
        should_end_session=False,
    )


@handle_intent('SetChannel')
def handle_set_channel_intent(request):
    message = request.session.get('message')
    channel = request.slots.get('channel')
    if message and channel:
        return make_confirm_message_response(message, channel)
    else:
        return Response(
            speech=PlainTextSpeech('Did you say {}?'.format(channel)),
            should_end_session=False,
            session={'confirming_channel': True, 'channel': channel}
        )


@handle_intent('SetMessage')
def handle_set_message_intent(request):
    message = request.slots.get('message')
    channel = request.session.get('channel')
    if message and channel:
        return make_confirm_message_response(message, channel)
    else:
        return make_set_channel_response(message)


@handle_intent('AMAZON.YesIntent')
def handle_confirmation(request):
    if request.session.get('confirming_channel'):
        return make_set_message_response(request.session.get('channel'))
    elif request.session.get('confirming_message'):
        channel = request.session.get('channel')
        message = request.session.get('message')
        token = request.access_token
        return post_to_slack(channel, message, token)
    else:
        return Response(
            speech=PlainTextSpeech("I'm sorry, I didn't understand your request"),
            session=request.session,
            should_end_session=False,
        )


@handle_intent('AMAZON.NoIntent')
def handle_no(request):
    if request.session.get('confirming_channel'):
        return make_set_channel_response(message=request.session.get('message'), retry=True)
    elif request.session.get('confirming_message'):
        return make_set_message_response(request.session.get('channel'), retry=True)
    else:
        return PlainTextSpeech('Goodbye')


@handle_intent('StartMessage')
@handle_launch_request
def handle_start_message(request):
    if not request.access_token:
        return Response(
            speech=PlainTextSpeech('You must sign in first'),
            card=LinkAccountCard(),
        )
    return make_set_channel_response()


@handle_intent('unrecognized_intent')
def handle_unrecognized_intent(request):
    return PlainTextSpeech("I'm sorry, I didn't understand that")


@handle_intent('AMAZON.StopIntent')
@handle_intent('AMAZON.CancelIntent')
def handle_cancel_intent(request):
    return PlainTextSpeech('Goodbye')


@handle_intent('AMAZON.StartOverIntent')
def handle_start_over_intent(request):
    return make_set_channel_response()
