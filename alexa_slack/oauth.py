from collections import OrderedDict
from urllib import urlencode

from flask import redirect, request
import requests

from alexa_slack import app
from alexa_slack.constants import AWS_VENDOR_ID, SLACK_CLIENT_ID, SLACK_CLIENT_SECRET


@app.route('/oauth/entry')
def oauth_entry_point():
    client_id = request.args.get('client_id')
    scope = request.args.get('scope')
    state = request.args.get('state')
    url = 'https://slack.com/oauth/authorize'
    query_string = urlencode(OrderedDict(
        scope=scope,
        state=state,
        client_id=client_id
    ))
    redirect_url = '{}?{}'.format(url, query_string)
    return redirect(redirect_url)


@app.route('/oauth/redirect')
def oauth_redirect():
    state = request.args.get('state')
    code = request.args.get('code')

    response = requests.get(
        'https://slack.com/api/oauth.access?{}'.format(urlencode({ 'code': code })),
        auth=(SLACK_CLIENT_ID, SLACK_CLIENT_SECRET)
    )
    response_json = response.json()
    access_token = response_json.get('access_token')

    redirect_url = 'https://pitangui.amazon.com/spa/skill/account-linking-status.html?vendorId={}'.format(AWS_VENDOR_ID)
    redirect_url += '#{}'.format(urlencode({'access_token': access_token, 'state': state, 'token_type': 'Bearer'}))
    return redirect(redirect_url)
