import requests
import config

API_V2_PREFIX = 'https://developer.toutiao.com/api/apps/v2'


class OpenAPI:
    def __init__(self, app_id, app_secret, default_timeout=5):
        self.app_id = app_id
        self.app_secret = app_secret
        self.default_timeout = default_timeout

    @classmethod
    def from_env(cls):
        conf = config.config_from_env('trade')
        if not conf:
            raise Exception(
                "couldn't find app_id & app_secret from env or .token.toml")

        return cls(conf.app_id, conf.app_secret)

    def get_access_token(self):
        endpoint = API_V2_PREFIX + '/token/'
        params = {
            'appid': self.app_id,
            'secret': self.app_secret,
            'grant_type': 'client_credential'
        }
        return self.request('post', endpoint, json=params, timeout=self.default_timeout)

    def get_client_access_token(self):
        endpoint = 'https://open.douyin.com/oauth/client_token/'
        params = {
            'client_key': self.app_id,
            'client_secret': self.app_secret,
            'grant_type': 'client_credential'
        }

    def request(self, method, url, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.default_timeout

        resp = requests.request(method, url, *args, **kwargs)
        return self.parse_response(resp)

    def parse_response(self, resp):
        if resp.status_code != 200 or resp.json()['err_no'] != 0:
            raise Exception(resp.json())
        return resp.json()['data']


if __name__ == '__main__':
    api = OpenAPI.from_env()
    print(api.get_access_token())
