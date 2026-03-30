import yaml
import itertools
from copy import deepcopy

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
def set_nested(config, key, value):
    keys = key.split(".")
    d = config
    for k in keys[:-1]:
        d = d[k]
    d[keys[-1]] = value


def generate_configs(base_config, sweep_dict):
    keys = sweep_dict.keys()
    values = sweep_dict.values()

    for combination in itertools.product(*values):
        config = deepcopy(base_config)

        for k, v in zip(keys, combination):
            set_nested(config, k, v)

        yield config