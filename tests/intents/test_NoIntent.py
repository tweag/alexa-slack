from tests.utils import _AlexaTestCase


class TestNoIntent(_AlexaTestCase):

    def input(self):
        return self.make_intent_request('AMAZON.NoIntent')

    def should_end_session(self):
        self.assertTrue(self.output.response.shouldEndSession)

    def should_say_goodbye(self):
        self.assertEqual(self.output.response.outputSpeech.text, 'Goodbye')


class TestNoIntentWhenConfirmingChannel(_AlexaTestCase):

    message = 'This is my message'

    def input(self):
        return self.make_intent_request(
            'AMAZON.NoIntent', session={
                'confirming_channel': True,
                'message': self.message,
                'channel': 'foo'
            })

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_propagate_message_in_session(self):
        self.assertEqual(self.output.sessionAttributes, {
            'message': self.message
        })

    def should_ask_for_channel(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            "Ok, let's try that again. What channel would you like to post your message to?"
        )

    def should_inlcude_reprompt(self):
        self.assertEqual(
            self.output.response.reprompt.outputSpeech.text,
            'Say the name of the channel you would like to post to'
        )


class TestNoIntentWhenConfirmingMessage(_AlexaTestCase):

    message = 'this is my message'
    channel = 'foo'

    def input(self):
        return self.make_intent_request(
            'AMAZON.NoIntent', session={
                'confirming_message': True,
                'message': self.message,
                'channel': self.channel,
        })

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_ask_for_message(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            "Ok, let's try that again. What would you like to post?"
        )

    def should_include_reprompt(self):
        self.assertEqual(
            self.output.response.reprompt.outputSpeech.text,
            'Say the message you would like me to post'
        )
