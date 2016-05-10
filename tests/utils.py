import json
import unittest

from alexa_slack import app

app.debug = True


class _AlexaTestCase(unittest.TestCase):

    def post_to_app(self, body):
        with app.test_client() as client:
            rv = client.post(
                '/',
                data=json.dumps(body),
                headers={'content-type': 'application/json'},
            )
            return json.loads(rv.get_data())

    def should_return_expected_output(self):
        result = self.post_to_app(self.input())
        self.assertEqual(result, self.expectedOutput())
