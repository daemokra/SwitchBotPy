import requests as r
import json
import time
import hashlib
import hmac
import base64

class RequestsUtil:
    def __init__(self, token, secret, host, version, nonce=''):
        """
        version : 'v1.1'とか指定
        """
        self._token = token
        self._secret = bytes(secret, 'utf-8')
        self._host = host
        self._v = version
        self._nonce = nonce
        self.set_header()

    def get_sign(self, t):
        string_to_sign = bytes('{}{}{}'.format(self._token, t, self._nonce), 'utf-8')
        return base64.b64encode(hmac.new(self._secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    def set_header(self):
        t = int(time.time() * 1000)
        self._header ={
                'Authorization': self._token,
                'Content-Type': 'application/json; charset=utf8',
                'sign': self.get_sign(t),
                'nonce': self._nonce,
                't': str(t)
            }

    def get_header(self):
        return self._header

    def get_request(self, url):
        self.get_header()
        res = r.get('/'.join([self._host,self._v,url]), headers = self.get_header())
        data = res.json()
        if data['message'] == 'success':
            return res.json()
        return {}

    def post_request(self, url, params):
        res = r.post('/'.join([self._host,self._v,url]), data = json.dumps(params), headers = self.get_header())
        data = res.json()
        if data['message'] == 'success':
            return res.json()
        return {}

    def get_status(self, id):
        return self.get_request('/'.join(['devices',id,'status']))

    def post_commands(self, id, params):
        return self.post_request('/'.join(['devices',id,'commands']), params)
