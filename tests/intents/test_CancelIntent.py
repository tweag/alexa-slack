from tests.utils import _AlexaTestCase


class TestCancelIntent(_AlexaTestCase):

    def input(self):
        return self.make_intent_request('AMAZON.CancelIntent')

    def should_end_session(self):
        self.assertTrue(self.output.response.shouldEndSession)

    def should_say_goodbye(self):
        self.assertEqual(self.output.response.outputSpeech.text, 'Goodbye')
