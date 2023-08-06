import click
from gitleaks_py.gitleaks_model import GitleaksConfig
from . import gitleaks_r as gl_r, gitleaks_w as gl_w, gitleaks_model as model

def _diff(lhs, rhs):
    additions = []
    allowlist = None
    for rule in lhs.rules:
        if (not rhs.has_rule(rule)):
            additions.append(rule)
    if lhs.allowlist != rhs.allowlist:
        allowlist = lhs.allowlist
    return GitleaksConfig(title=f"Rules in '{lhs.title}' and not in '{rhs.title}'", allowlist=allowlist, rules=additions)

def diff(config_file: str, default_config_file: str, additions: bool=True, dst=None):
    
    # extract
    gl_config=gl_r.load(config_file)
    gl_config.title = config_file
    default_config = gl_r.load(default_config_file)
    default_config.title = default_config_file
    
    # transform
    lhs, rhs = (gl_config, default_config) if additions else (default_config, gl_config)
    diff_config = _diff(lhs, rhs)
    
    # load
    if dst:
        gl_w.dump(diff_config, dst)
    else:
        click.echo(gl_w.dumps(diff_config))
    return diff_config

@click.command('diff')
@click.option('-d', '--dst', help='Destination file to output to')
@click.option('-o', '--omissions', 'additions', flag_value=False, help='Omissions from default config, not found in config')
@click.option('-a', '--additions', 'additions', flag_value=True, default=True, help='Additions from config, not found in default config')
@click.argument('config_file')
@click.argument('default_config_file', default=model.GITLEAKS_DEFAULT_CONFIG_FILE)
def diff_command(config_file: str, default_config_file: str, additions: bool=True, dst=None):
    diff(config_file, default_config_file, additions, dst)

if __name__ == "__main__":
    diff_command()
