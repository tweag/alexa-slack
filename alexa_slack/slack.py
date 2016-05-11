import requests

from pylexa.response import PlainTextSpeech


def post_to_slack(channel, text, token):
    url = 'https://slack.com/api/chat.postMessage'
    res = requests.post(url, {
        'token': token,
        'channel': channel,
        'text': text,
        'as_user': False,
    })
    if res.json()['ok']:
        return PlainTextSpeech("Okay. Your message has been posted.")
    else:
        error = res.json().get('error')
        if error == 'channel_not_found':
            return PlainTextSpeech('Sorry, I could not find the {} channel'.format(channel))
        return PlainTextSpeech('Oh no, something went wrong.')

