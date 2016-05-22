from tests.utils import _AlexaTestCase


class TestSetMessageIntentWhenChannelSet(_AlexaTestCase):

    channel = 'foo'
    message = 'This is my message'

    def input(self):
        return self.make_intent_request(
            'SetMessage', session={'channel': self.channel}, message=self.message)

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


class TestSetMessageWithoutChannel(_AlexaTestCase):

    message = 'This is my message'

    def input(self):
        return self.make_intent_request('SetMessage', message=self.message)

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_set_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, {
            'message': self.message,
        })

    def should_ask_for_channel(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'What channel would you like to post your message to?'
        )

    def should_include_reprompt_text(self):
        self.assertEqual(
            self.output.response.reprompt.outputSpeech.text,
            'Say the name of the channel you would like to post to'
        )


class TestSetMessageWhenMessageAlreadySet(_AlexaTestCase):

    existing_message = 'foo'
    new_message = 'hello'

    def input(self):
        return self.make_intent_request(
            'SetMessage',
            session={'message': self.existing_message},
            message=self.new_message,
        )

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_set_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, {
            'channel': self.new_message,
            'message': self.existing_message,
            'confirming_message': True
        })

    def should_ask_for_confirmation(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'Great. Would you like me to post {} to {}?'.format(self.existing_message, self.new_message)
        )
