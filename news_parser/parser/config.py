import yaml

from pathlib import Path


_base_dir = Path(__file__).parent.parent.parent

with open(_base_dir / 'config.yaml') as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

print(config)