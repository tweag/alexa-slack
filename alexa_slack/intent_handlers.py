import requests

from pylexa.app import handle_launch_request
from pylexa.intent import handle_intent
from pylexa.response import LinkAccountCard, PlainTextSpeech, Response


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
        return Response(
            speech=PlainTextSpeech('What would you like to post? Say "my message is" followed by the message you would like me to post.'),
            reprompt=PlainTextSpeech('Say "my message is" followed by the message you would like me to post'),
            session={'channel': request.session.get('channel')},
            should_end_session=False,
        )
    elif request.session.get('confirming_message'):
        return post_to_slack(request)
    else:
        return PlainTextSpeech('Ooops')


@handle_intent('AMAZON.NoIntent')
def handle_no(request):
    if request.session.get('confirming_channel'):
        return Response(
            speech=PlainTextSpeech("Ok, let's try that again. What channel would you like to post your message to?"),
            reprompt=PlainTextSpeech('Say the name of the channel you would like to post to.'),
            should_end_session=False
        )
    elif request.session.get('confirming_message'):
        return Response(
            speech=PlainTextSpeech("Ok, let's try that again. What would you like to post? Say 'my message is' followed by the message you would like to post"),
            reprompt=PlainTextSpeech('Say "my message is" followed by the message you would like me to post'),
            session=request.session,
            should_end_session=False
        )
    else:
        return PlainTextSpeech('Goodbye')



def post_to_slack(request):
    channel = request.session.get('channel')
    text = request.session.get('message')
    token = request.access_token
    url = 'https://slack.com/api/chat.postMessage'
    res = requests.post(url, {
        'token': token,
        'channel': channel,
        'text': text,
        'as_user': True,
    })
    if res.json()['ok']:
        return PlainTextSpeech("Okay. Your message has been posted.")
    else:
        return PlainTextSpeech('Oops, something went wrong.')


@handle_intent('StartMessage')
@handle_launch_request
def handle_start_message(request):
    if not request.access_token:
        return Response(
            speech=PlainTextSpeech('You must sign in first'),
            card=LinkAccountCard(),
        )
    speech = PlainTextSpeech('What channel would you like to post your message to?')
    reprompt = PlainTextSpeech('Say the name of the channel you would like to post to')
    return Response(speech=speech, reprompt=reprompt, should_end_session=False)


@handle_intent('unrecognized_intent')
def handle_unrecognized_intent(request):
    return PlainTextSpeech("I'm sorry, I didn't understand that")

