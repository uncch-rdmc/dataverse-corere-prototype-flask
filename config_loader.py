import yaml

global config
config = {}

for key, value in yaml.load(open('config.yaml'), Loader=yaml.BaseLoader)['config'].items():
    config[key] = value

