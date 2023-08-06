from dataclasses import dataclass
from typing import List, Set

GITLEAKS_DEFAULT_CONFIG_FILE = "https://raw.githubusercontent.com/zricethezav/gitleaks/master/config/gitleaks.toml"

@dataclass
class AllowList(object):
    description: str==None
    paths: List==None
    stopwords: List==None
    
@dataclass
class Rule(object):
    id: str=None
    description: str=None
    secretGroup: int=None
    regex: str=None
    entropy: float=None
    keywords: List=None
    allowlist: AllowList=None

@dataclass
class GitleaksConfig(object):
    title: str=None
    allowlist: AllowList=None
    rules: List[Rule]=None
    rule_ids: Set[str]=None
    
    def __post_init__(self):
        if self.rules: 
            self.rules.sort(key=lambda r : r.id.lower() if r.id else r.id)
            self.rule_ids = set([rule.id for rule in self.rules])

    def has_rule(self, rule):
        return self.rule_ids and rule.id in self.rule_ids