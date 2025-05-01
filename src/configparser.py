import os

import yaml

CONFIG_PATH = os.environ.get("OCTOCAT_CONFIG_PATH", "config.yaml")


def init_config():
    with open(CONFIG_PATH) as f:
        return yaml.load(f, Loader=yaml.FullLoader)
