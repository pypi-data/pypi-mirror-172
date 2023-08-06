from email.policy import default
import click
from gitleaks_py.gitleaks_model import GitleaksConfig, AllowList
from . import gitleaks_r as gl_r, gitleaks_w as gl_w, gitleaks_model as model
import logging

logger = logging.getLogger()

def merge(config_files: tuple, title: str=None, dst=None):
    
    allowlist_paths = set()
    allowlist_stopwords = set() 
    rules = []
    duplicate_rules = []
    titles = []

    def _merge_rules(src):
        dst_rule_ids = set([rule.id for rule in rules])
        for rule in src.rules:
            if rule.id in dst_rule_ids:
                duplicate_rules.append(rule.id)
            else:
                rules.append(rule)
                
    def _merge_allowlist(src):
        allowlist = src.allowlist
        if allowlist:
            if allowlist.paths: allowlist_paths.update(allowlist.paths)
            if allowlist.stopwords: allowlist_stopwords.update(allowlist.stopwords)
    
    def merged_title():
        return title if title else ', '.join(titles)
        
    def allowlist():
        paths=list(allowlist_paths) if allowlist_paths else None
        stopwords=list(allowlist_stopwords) if allowlist_stopwords else None
        return AllowList(description="global allowlist", paths=paths, stopwords=stopwords) if allowlist_paths or allowlist_stopwords else None

    # extract
    for file, gl_config in gl_r.load_all(config_files):
        _merge_allowlist(gl_config)
        _merge_rules(gl_config)
        titles.append(gl_config.title)
        
    # transform
    merged_gl_config = GitleaksConfig(merged_title(), allowlist=allowlist(), rules=rules)
            
    # load
    if dst:
        with open(dst, 'wb') as f:
            gl_w.dump(merged_gl_config, f)
    else:
        click.echo(gl_w.dumps(merged_gl_config))

    # warn for dupes
    if duplicate_rules:
        logger.warn(f"Discarded duplicate rules '{duplicate_rules}'")
            
    return merged_gl_config


@click.command('merge')
@click.option('-t', '--title', 'title', help='Title')
@click.option('-d', '--dst', help='Destination file to output to')
@click.argument('config_files', nargs=-1)
def merge_command(config_files: str, title: str=None, dst: str=None):
    merge(config_files, title, dst)

if __name__ == "__main__":
    merge_command()