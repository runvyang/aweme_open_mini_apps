from dataclasses import dataclass
import os
import toml

LOCAL_TOKEN_FILE = '.token.toml'


@dataclass
class Config:
    app_id: str
    app_secret: str


def config_from_env(app_name='trade') -> Config:
    env_app_id = os.environ.get('APP_ID')
    env_app_secret = os.environ.get('APP_SECRET')
    if env_app_id and env_app_secret:
        return Config(env_app_id, env_app_secret)

    file_dir = os.path.dirname(os.path.realpath(__file__))
    token_file = os.path.join(file_dir, LOCAL_TOKEN_FILE)
    if os.path.exists(token_file):
        config_file = toml.load(token_file)
        if app_name not in config_file:
            raise Exception(f"couldn't find {app_name} in {LOCAL_TOKEN_FILE}")

        config = config_file[app_name]
        return Config(config['app_id'], config['app_secret'])
