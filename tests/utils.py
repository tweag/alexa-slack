import json
import unittest

from alexa_slack import app

app.debug = True


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value


class _AlexaTestCase(unittest.TestCase):

    def _post_to_app(self, body):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(body),
                headers={'content-type': 'application/json'},
            )
            self.status_code = rv.status_code
            return json.loads(rv.get_data())

    def make_intent_request(self, intent_name, session=None, access_token='some_token', **kwargs):
        slots = {
            name: {
                'name': name,
                'value': value,
            } for name, value in kwargs.iteritems()
        }
        return {
            "session": {
                "attributes": session,
                "sessionId": "SessionId.some_session_id",
                    "application": {
                    "applicationId": "amzn1.echo-sdk-ams.app.some_app_id"
                },
                "user": {
                    "userId": "amzn1.ask.account.some_account_id",
                    "accessToken": access_token
                },
                "new": True
            },
            "request": {
                "type": "IntentRequest",
                "requestId": "EdwRequestId.351d1af4-0cdb-4294-b082-6707c9510fea",
                "timestamp": "2016-05-09T18:43:53Z",
                "intent": {
                    "name": intent_name,
                    "slots": slots
                },
                "locale": "en-US"
            },
            "version": "1.0"
        }

    def should_return_200_status_code(self):
        self.assertEqual(self.status_code, 200)

    def setUp(self):
        self.output = DotDict(self._post_to_app(self.input()))
