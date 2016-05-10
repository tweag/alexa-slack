from tests.utils import _AlexaTestCase


class TestUnrecognizedIntent(_AlexaTestCase):

    def input(self):
        return {
            "session": {
                "sessionId": "SessionId.some_session_id",
                    "application": {
                    "applicationId": "amzn1.echo-sdk-ams.app.some_app_id"
                },
                "user": {
                    "userId": "amzn1.ask.account.some_account_id",
                    "accessToken": "some_access_token"
                },
                "new": True
            },
            "request": {
                "type": "IntentRequest",
                "requestId": "EdwRequestId.351d1af4-0cdb-4294-b082-6707c9510fea",
                "timestamp": "2016-05-09T18:43:53Z",
                "intent": {
                "name": "AMAZON.SomeOtherIntent",
                "slots": {}
                },
                "locale": "en-US"
            },
            "version": "1.0"
        }

    def expectedOutput(self):
        return {
            "version": "1.0",
            "sessionAttributes": None,
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "I'm sorry, I didn't understand that"
                },
                "shouldEndSession": True
            }
        }
