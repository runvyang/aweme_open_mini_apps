LOCAL_TOKEN_FILE = '.token.toml'

class OpenAPI:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret

    @classmethod
    def from_env(cls):
        import toml
        import os

        env_app_id = os.environ.get('APP_ID')
        env_app_secret = os.environ.get('APP_SECRET')
        if env_app_id && env_app_secret:
            return cls(env_app_id, env_app_secret)

        if os.path.exists(LOCAL_TOKEN_FILE):
            config = toml.load(LOCAL_TOKEN_FILE)
            return cls(config['app_id'], config['app_secret'])

        raise Exception("could find app_id & app_secret from env or .token.toml")
