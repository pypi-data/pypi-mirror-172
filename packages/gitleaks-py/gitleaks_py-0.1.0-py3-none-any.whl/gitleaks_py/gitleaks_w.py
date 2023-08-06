import tomli_w
from . import gitleaks_model as model
from typing import BinaryIO
from dataclasses import asdict

def dumpt(__glc: model.GitleaksConfig):
    
    def __dict_factory(__d):
        return {k: v for (k, v) in __d if v is not None}
        
    def __rules(__rules, toml):
        rules = []
        for __r in __rules or []:
            rules.append(asdict(__r, dict_factory=__dict_factory))
        toml['rules'] = rules
        
    def __allowlist(__al, toml):
        if __al:
            toml['allowlist'] = asdict(__al, dict_factory=__dict_factory)

    toml = {}
    toml['title'] = __glc.title
    __allowlist(__glc.allowlist, toml)
    __rules(__glc.rules, toml)
    return toml

def dumps(__glc: model.GitleaksConfig):
    toml = dumpt(__glc)
    return tomli_w.dumps(toml)

def dump(__glc: model.GitleaksConfig, __fp: BinaryIO):
    toml = dumpt(__glc, )
    tomli_w.dump(toml, __fp)
