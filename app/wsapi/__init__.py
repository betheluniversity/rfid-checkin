import time
import hmac
import hashlib
import requests
import json
import urllib.parse

from app import app


class WSAPIController:

    def get_hmac_request(self, path):
        path_and_query = path + '?TIMESTAMP=' + str(int(time.time())) + '&ACCOUNT_ID=labs'
        host = 'https://wsapi.bethel.edu'
        sig = hmac.new(bytes(app.config['WSAPI_SECRET'], 'utf-8'), digestmod=hashlib.sha1,
                       msg=bytes(path_and_query, 'utf-8')).hexdigest()
        req = requests.get(host + path_and_query, headers={'X-Auth-Signature': sig})
        req_info = json.loads(req.content)
        return req_info

    def get_names_from_username(self, username):
        path = '/username/{0}/names'.format(username)
        return self.get_hmac_request(path)

    def get_user_from_prox(self, card_id):
        path = '/card_id/{0}'.format(card_id)
        return self.get_hmac_request(path)
