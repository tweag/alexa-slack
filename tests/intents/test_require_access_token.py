from alexa_slack.intent_handlers import require_access_token

from pylexa.intent import handle_intent
from pylexa.response import PlainTextSpeech, Response

from tests.utils import _AlexaTestCase


@handle_intent('foo')
@require_access_token
def handle_foo(request):
    return Response(speech=PlainTextSpeech('It works'), should_end_session=False)


class TestFooIntentWithoutAccessToken(_AlexaTestCase):

    def input(self):
        return self.make_intent_request('foo', access_token=None)

    def should_end_session(self):
        self.assertTrue(self.output.response.shouldEndSession)

    def should_require_sign_in(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'You must sign in first'
        )

    def should_send_link_account_card(self):
        self.assertEqual(self.output.response.card.type, 'LinkAccount')


class TestFooIntentWithAccessToken(_AlexaTestCase):

    def input(self):
        return self.make_intent_request('foo')

    def should_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_require_sign_in(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'It works'
        )
