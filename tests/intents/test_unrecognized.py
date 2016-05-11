from tests.utils import _AlexaTestCase


class TestUnrecognizedIntent(_AlexaTestCase):

    def input(self):
        return self.make_intent_request('AMAZON.SomeOtherIntent')

    def should_say_sorry(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            "I'm sorry, I didn't understand that"
        )

    def should_end_session(self):
        self.assertTrue(self.output.response.shouldEndSession)
