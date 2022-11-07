import time
import requests
import config
from dataclasses import dataclass

GOODLIFE_V1_PREFIX = 'https://open.douyin.com/goodlife/v1/'
GOODLIFE_MA_PREFIX = 'https://open.douyin.com/'


@dataclass
class AccessToken:
    access_token: str
    created_at: int
    expires_in: int

    def valid(self):
        return (self.created_at + self.expires_in) > int(time.time())


class OpenAPIWeb:
    def __init__(self, app_id, app_secret, default_timeout=5):
        self.app_id = app_id
        self.app_secret = app_secret
        self.default_timeout = default_timeout
        self._access_token = None

    @property
    def access_token(self):
        if self._access_token is not None and self._access_token.valid():
            return self._access_token.access_token

        endpoint = 'https://open.douyin.com/oauth/client_token/'
        params = {
            'client_key': self.app_id,
            'client_secret': self.app_secret,
            'grant_type': 'client_credential'
        }

        resp = self.request('post', endpoint, params=params, add_token=False)
        data = self.parse_response(resp)
        self._access_token = AccessToken(
            data['access_token'], int(time.time()), data['expires_in'])
        return self._access_token.access_token

    def list_goods(self, account_id, cursor=None, count=None, status=None):
        endpoint = GOODLIFE_V1_PREFIX + 'goods/product/online/query/'
        params = {
            'account_id': account_id,
            'count': count
        }

        if cursor:
            params['cursor'] = cursor
        if status:
            params['status'] = status

        resp = self.request('get', endpoint, params=params)
        return self.parse_response(resp)

    def request(self, method, url, *args, add_token=True, **kwargs):
        # todo, refresh token logic here
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.default_timeout

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        if add_token:
            kwargs['headers']['access-token'] = self.access_token
        return requests.request(method, url, *args, **kwargs)

    def parse_response(self, response):
        print(response.json())
        if response.status_code != 200 or response.json()['data']['error_code'] != 0:
            raise Exception(response.content.decode('utf8'))

        return response.json()['data']

    def query_poi_match_relations(self, ext_ids):
        endpoint = GOODLIFE_V1_PREFIX + 'poi/match/relation/query/'
        params = {
            "ext_ids": ext_ids
        }

        return self.parse_response(self.request('get', endpoint, params=params))

    def ma_list_goods(self, cursor=None, count=5, status=None):
        endpoint = GOODLIFE_MA_PREFIX + 'life/goods/product/online/list/'
        params = dict(count=count, access_token=self.access_token)
        if cursor:
            params['cursor'] = cursor
        if status is not None:
            params['status'] = status

        return self.parse_response(self.request('get', endpoint, params=params))

if __name__ == '__main__':
    conf = config.config_from_env('goodlife')
    api = OpenAPIWeb(conf.app_id, conf.app_secret)
    # print(api.list_goods(7158417672403699749))
    # print(api.query_poi_match_relations('kaTest1104'))
    print(api.ma_list_goods())
    
