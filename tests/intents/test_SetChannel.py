from tests.utils import _AlexaTestCase


class TestSetChannelIntentWhenNoSession(_AlexaTestCase):

    channel = 'foo'

    def input(self):
        return self.make_intent_request('SetChannel', channel=self.channel)

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_set_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, {
            'channel': self.channel,
            'confirming_channel': True,
        })

    def should_ask_for_confirmation(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'Did you say {}?'.format(self.channel)
        )


class TestSetChannelIntentWhenMessageAlreadySet(_AlexaTestCase):

    message = 'This is my message'
    channel = 'foo'

    def input(self):
        return self.make_intent_request(
            'SetChannel', session={'message': self.message}, channel=self.channel)

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_set_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, {
            'channel': self.channel,
            'message': self.message,
            'confirming_message': True
        })

    def should_ask_for_confirmation(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'Great. Would you like me to post {} to {}?'.format(self.message, self.channel)
        )
