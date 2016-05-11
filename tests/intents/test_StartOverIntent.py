from tests.utils import _AlexaTestCase


class TestStartOverIntent(_AlexaTestCase):

    def input(self):
        return self.make_intent_request(
            'AMAZON.StartOverIntent', session={'channel': 'channel', 'message': 'message'})

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_reset_session(self):
        self.assertEqual(self.output.sessionAttributes, {
            'message': None
        })

    def should_ask_for_channel(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'What channel would you like to post your message to?'
        )

    def should_include_reprompt(self):
        self.assertEqual(
            self.output.response.reprompt.outputSpeech.text,
            'Say the name of the channel you would like to post to'
        )
