#!/usr/bin/env python

import ConfigParser
from flask import Flask, request, json
import requests

config = ConfigParser.ConfigParser()
config.readfp(open('/etc/stickynotes2modernpaste/config.ini'))

MODERNPASTE = config.get('stickynotes2modernpaste', 'modernpaste')

app = Flask(__name__)
app.debug = True

def r(d):
    '''wrap dict in "result" dict'''
    return {'result': d}

@app.route('/', methods=['POST'])
def main():
    language = request.form.get('paste_lang')
    text = request.form.get('paste_data')
    private = request.form.get('paste_private')
    expire = request.form.get('paste_expire')
    password = request.form.get('paste_password')
    author = request.form.get('paste_user')

    payload = {
        'contents': text,
        'language': language,
        #'expiry_time': expire # Disabled because we force this to 1wk for now.
        'title': "Anonymous user's paste"
    }

    if author != '':
        payload['title'] = author + "'s paste"

    if password != '':
        payload['password'] = password

    resp = requests.post(
        MODERNPASTE + '/api/paste/submit',
        json=payload
    )

    if resp.status_code != 200:
        return json.dumps(
            r({'error': 'Received non-200 status code from Modern Paste'}))

    return json.dumps(
        r({'id': resp.json()['paste_id_repr'],
           'hash': resp.json()['paste_id_repr']
        }))

@app.route('/<path:path>', methods=['POST'])
def shorten(path):
    p = path.replace('/', '')
    resp = requests.get(
        'https://da.gd/s',
        params={'url': MODERNPASTE + '/paste/' + p, 'strip': True})
    if resp.status_code != 200:
        return json.dumps(
            r({'error': 'Could not shorten URL'}))

    # The fpaste client is bad here:
    # This comment is found in its source code:
    # "# We know that short_url is always the third last line in the json output"
    # So this means we have to ensure that there are two lines after the short
    # url in our output.
    return '"short_url": "' + resp.text + '"\n\n\n'

if __name__ == "__main__":
    app.run()
