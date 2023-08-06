import smartdict
import yaml
import json

from oba import Obj

from refconfig import config_type
from refconfig.config_type import CType


class AtomConfig:
    def __init__(self, config, key=None, t=CType.SMART):
        self.config = config
        self.key = key
        self.t = self.parse_type(t)

        self.error = ValueError('Can not identify ConfigType')
        self.value = self.parse_config()

    def parse_type(self, t):
        t = config_type.parse_type(t)

        if t is not CType.SMART:
            return t

        if isinstance(self.config, dict):
            return CType.DICT
        assert isinstance(self.config, str), self.error
        if self.config.endswith('.yaml'):
            return CType.YAML
        if self.config.endswith('.json'):
            return CType.JSON
        raise self.error

    def parse_config(self):
        if self.t is CType.DICT:
            return self.config
        if self.t is CType.JSON:
            return json.load(open(self.config, 'rb+'))
        if self.t is CType.YAML:
            return yaml.safe_load(open(self.config, 'rb+'))
        raise self.error

    def __str__(self):
        return f'Config({self.key}-{self.t})'


def parse(__obj: bool = False, *configs: AtomConfig):
    kv = dict()

    for config in configs:
        if config.key is None:
            assert len(configs) == 1, ValueError('Too much configs with key = None')
            return smartdict.parse(config.value)
        kv[config.key] = config.value

    return smartdict.parse(kv)


def parse_by_tuple(*configs: tuple):
    return parse(*[AtomConfig(config=config[0], key=config[1], t=config[2]) for config in configs])


def parse_with_single_type(t, __config=None, **configs):
    if __config:
        return parse_by_tuple((__config, None, t))
    return parse_by_tuple(*[(v, k, t) for k, v in configs.items()])


def parse_yaml(__config: str = None, **configs):
    return parse_with_single_type(CType.YAML, __config, **configs)


def parse_json(__config: str = None, **configs):
    return parse_with_single_type(CType.JSON, __config, **configs)


def parse_dict(__config: dict = None, **configs):
    return parse_with_single_type(CType.DICT, __config, **configs)
