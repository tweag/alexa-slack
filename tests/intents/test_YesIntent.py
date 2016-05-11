from mock import patch

from pylexa.response import PlainTextSpeech

from tests.utils import _AlexaTestCase


class TestYesIntentWhenNotConfirmingAnything(_AlexaTestCase):

    session = { 'channel': 'foo' }

    def input(self):
        return self.make_intent_request('AMAZON.YesIntent', session=self.session)

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_propagate_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, self.session)

    def should_say_sorry(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            "I'm sorry, I didn't understand your request"
        )


class TestYesIntentWhenConfirmingChannel(_AlexaTestCase):

    channel = 'foo'

    def input(self):
        return self.make_intent_request('AMAZON.YesIntent', session={
            'confirming_channel': True,
            'channel': self.channel,
        })

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_ask_for_message(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'What would you like to post?'
        )

    def should_set_channel_on_session(self):
        self.assertEqual(self.output.sessionAttributes, {
            'channel': self.channel
        })

    def should_include_reprompt(self):
        self.assertEqual(
            self.output.response.reprompt.outputSpeech.text,
            'Say the message you would like me to post'
        )


class TestYesIntentWhenConfirmingMessage(_AlexaTestCase):

    channel = 'foo'
    message = 'This is my message'

    def setUp(self):
        self.requests_patcher = patch('alexa_slack.slack.requests')
        self.requests = self.requests_patcher.start()
        self.requests.post.return_value.json.return_value = { 'ok': True }
        super(TestYesIntentWhenConfirmingMessage, self).setUp()

    def tearDown(self):
        self.requests_patcher.stop()
        super(TestYesIntentWhenConfirmingMessage, self).tearDown()

    def input(self):
        return self.make_intent_request('AMAZON.YesIntent', session={
            'channel': self.channel,
            'message': self.message,
            'confirming_message': True
        })

    def should_end_session(self):
        self.assertTrue(self.output.response.shouldEndSession)

    def should_say_success(self):
        self.assertEqual(
            self.output.response.outputSpeech.text, 'Okay. Your message has been posted.')
