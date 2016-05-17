from tests.utils import _AlexaTestCase


class _BaseHelpIntentTestCase(_AlexaTestCase):

    session = {}

    def input(self):
        return self.make_intent_request('AMAZON.HelpIntent', session=self.session)

    def should_not_end_session(self):
        self.assertFalse(self.output.response.shouldEndSession)

    def should_propagate_session_attributes(self):
        self.assertEqual(self.output.sessionAttributes, self.session)

    def should_say_expected_speech(self):
        self.assertEqual(
            self.output.response.outputSpeech.text,
            self.expected_speech
        )


class TestHelpIntentWithNoSession(_BaseHelpIntentTestCase):

    expected_speech = (
        "You can begin by saying the name of the channel you would like to "
        "post to. After that, you'll be prompted for the message to post. "
        "Once you confirm the message and channel, your message will be posted. "
        "What channel would you like to post to?"
    )


class TestHelpIntentWithoutMessage(_BaseHelpIntentTestCase):

    session = { 'channel': 'foo' }
    expected_speech = (
        "You can now say the message you want to post to foo. What message would "
        "you like to post?"
    )


class TestHelpIntentWithoutChannel(_BaseHelpIntentTestCase):

    session = { 'message': 'my message' }
    expected_speech = "What channel would you like to post your message to?"


class TestHelpWhenConfirmingChannel(_BaseHelpIntentTestCase):

    session = { 'channel': 'foo', 'confirming_channel': True }
    expected_speech = (
        "Do you want to post to the foo channel? Say yes if that channel is "
        "correct, or say no if you would like to specify another channel."
    )


class TestHelpWhenConfirmingMessage(_BaseHelpIntentTestCase):

    session = {
        'channel': 'foo',
        'message': 'my message',
        'confirming_message': True
    }
    expected_speech = (
        "Do you want to post my message to foo? Say yes if the channel and message "
        "are correct, or say no if you would like to specify another message."
    )
