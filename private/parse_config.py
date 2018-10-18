import yaml
import os

from exception.exception import ConfigDoesNotExist


def parse(dir, name):
    path = os.path.join(dir, name)
    with open(path, 'r') as stream:
        try:
            config = yaml.load(stream)
        except FileNotFoundError:
            raise ConfigDoesNotExist(path)

    return config['token'], config['confirmation_token'], config['app']
