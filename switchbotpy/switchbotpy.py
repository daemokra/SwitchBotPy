import json
import time
import hashlib
import hmac
import base64
import requests
from .device import *

class SwitchBotPy:
    HOST = 'https://api.switch-bot.com'
    def __init__(self, token, secret, version='v1.1', nonce='') -> None:
        self._token = token
        self._secret = bytes(secret, 'utf-8')
        self._v = version
        self._nonce = nonce

        self._session = requests.Session()
        self._header = self._gen_header()
        self._session.headers.update(self._header)

    def _gen_sign(self, t):
        string_to_sign = bytes('{}{}{}'.format(self._token, t, self._nonce), 'utf-8')
        return base64.b64encode(hmac.new(self._secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    def _gen_header(self):
        t = int(time.time() * 1000)
        self._header ={
                'Authorization': self._token,
                'Content-Type': 'application/json; charset=utf8',
                'sign': self._gen_sign(t),
                'nonce': self._nonce,
                't': str(t)
            }
        return self._header

    def get_request(self, url):
        res = self._session.get('/'.join([self.HOST,self._v,url]))
        data = res.json()
        if data['message'] == 'success':
            return res.json()
        return {}

    def post_request(self, url, params):
        res = self._session.post('/'.join([self.HOST,self._v,url]), data = json.dumps(params))
        data = res.json()
        if data['message'] == 'success':
            return res.json()
        return {}

    def get_status(self, id):
        return self.get_request('/'.join(['devices',id,'status']))

    def post_commands(self, id, params):
        return self.post_request('/'.join(['devices',id,'commands']), params)

    def get_devices_list(self):
        return self.get_request('devices')['body']

    def get_physical_devices(self):
        return self.get_devices_list()['deviceList']

    def get_virtual_devices(self):
        return self.get_devices_list()['infraredRemoteList']

    def get_airconditioners(self) -> AirConditioner:
        acs = []
        for device in self.get_virtual_devices():
            if  device['remoteType'] == 'Air Conditioner':
                acs.append(AirConditioner(self, device['deviceId'], device['deviceName'], device['remoteType'], device['hubDeviceId']))
        return acs

    def get_hubminis(self) -> HubMini:
        d = []
        for device in self.get_physical_devices():
            if  device['deviceType'] == 'Hub Mini':
                d.append(HubMini(self, device['deviceId'], device['deviceName'], device['deviceType'], device['hubDeviceId']))
        return d

