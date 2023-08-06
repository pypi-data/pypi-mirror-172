import glob
import tomli
import requests
from requests.structures import CaseInsensitiveDict
from . import gitleaks_model as model

GITLEAKS_DEFAULT_CONFIG_FILE = "https://raw.githubusercontent.com/zricethezav/gitleaks/master/config/gitleaks.toml"

def loadt(__t: dict):
    
    def __rules(__rules):
        if __rules:
            rules = []
            for __r in __rules:
                __cid = CaseInsensitiveDict(__r)
                rules.append(model.Rule(id=__cid.get('id'),
                            description=__cid.get('description'),
                            secretGroup=__cid.get('secretgroup'),
                            regex=__cid.get('regex'),
                            entropy=__cid.get('entropy'),
                            keywords=__cid.get('keywords'),
                            allowlist=__allowlist(__cid.get('allowlist'))))
            return rules
        
    def __allowlist(__al):
        __cid = CaseInsensitiveDict(__al)
        return model.AllowList(description=__cid.get('description'),
                         paths=__cid.get('paths'),
                         stopwords=__cid.get('stopwords')) if __al else None
        
    toml = CaseInsensitiveDict(__t)
    if toml:
        return model.GitleaksConfig(title = toml.get('title'),
                            allowlist=__allowlist(toml.get('allowlist')),
                            rules=__rules(toml.get('rules')))

def loads(__s: str):
    return loadt(tomli.loads(__s))
    
def load(__fp: str):
    return loadt(_load_toml(__fp))
    
def load_all(config_files: tuple):
    for config_file in config_files:
        for file in glob.glob(config_file):
            yield file, load(file)

def _load_toml(__fp):
    if (__fp.startswith('http')):
        with requests.get(__fp) as response:
            body = response.text
            return tomli.loads(body)
    else:
        with open(__fp, mode="rb") as fp:
            return tomli.load(fp)
