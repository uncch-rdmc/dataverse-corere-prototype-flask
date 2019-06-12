import yaml

global config
config = {}

for key, value in yaml.load(open('config.yaml'))['config'].items():
    config[key] = value

