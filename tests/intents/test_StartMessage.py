from tests.utils import _AlexaTestCase


class TestStartMessageWhenNoAccessToken(_AlexaTestCase):

    def input(self):
        return self.make_intent_request('StartMessage', access_token=None)

    def should_end_session(self):
        self.assertTrue(self.output.response.shouldEndSession)

    def should_require_sign_in(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            'You must sign in first'
        )

    def should_send_link_account_card(self):
        self.assertEqual(self.output.response.card.type, 'LinkAccount')


class TestStartMessageWithToken(_AlexaTestCase):

    def input(self):
        return self.make_intent_request('StartMessage')

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

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

    def should_set_message_to_None_in_session(self):
        self.assertIsNone(self.output.sessionAttributes.message)
