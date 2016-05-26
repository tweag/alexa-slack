from tests.utils import _AlexaTestCase


class TestSetChannelMessageIntent(_AlexaTestCase):

    channel = 'foo'
    message = 'This is my message'

    def input(self):
        return self.make_intent_request(
            'SetChannelMessage', channel=self.channel, message=self.message)

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


class TestSetChannelMessageIntentWithoutMessage(_AlexaTestCase):

    channel = 'foo'

    def input(self):
        return self.make_intent_request(
            'SetChannelMessage', channel=self.channel, message=None)

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_set_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, {
            'channel': self.channel
        })

    def should_ask_for_confirmation(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'What would you like to post?'
        )


class TestSetChannelMessageIntentWithoutChannel(_AlexaTestCase):

    message = 'This is my message'

    def input(self):
        return self.make_intent_request(
            'SetChannelMessage', channel=None, message=self.message)

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_set_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, {
            'message': self.message
        })

    def should_ask_for_confirmation(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'What channel would you like to post your message to?'
        )

