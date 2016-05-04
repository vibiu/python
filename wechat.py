# /usr/bin/env python
# coding: utf-8

from flask import Flask, request, make_response, jsonify
import hashlib
from lead import xmlRequest


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'vibiu_hard_token'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
        return jsonify({'error': 'token invalid'})
    if request.method == 'POST':
        xml_request = xmlRequest(request)
        reply = xml_request.robort_reply()
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response


if __name__ == '__main__':
    app.run(debug=True)
