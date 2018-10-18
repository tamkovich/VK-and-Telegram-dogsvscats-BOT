from private.parse_config import parse

config = dict()
config['token'], config['confirmation_token'], config['app'] = parse('private', 'config.yaml')
