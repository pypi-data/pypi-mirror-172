import sys
import click
import os
import tempfile
import shutil
import json
from dataclasses import dataclass, field
from . import gitleaks_r as gl_r
from . import gitleaks_command as gl
import logging

logger = logging.getLogger()

def verify_config(config_files: tuple, secrets_folder='secrets', dst=None):
    
    def _secret_files(id):
        for file in os.listdir(secrets_folder):
            if file.startswith(f'{id}.'):
                yield os.path.join(secrets_folder, file)
    
    def _verify(status, rule_id, secret_file, config_file):
        with CopyTempFile(secret_file, tmpdir) as dst:
            report = gl.detect(config_file, tmpdir)
            rule_violations = report.violations_for_rule_id(rule_id)
            # violations are good as we've detected a secret for the rule
            if not rule_violations:
                status.fail(secret_file)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        failures = []
        for config_file, gl_config in gl_r.load_all(config_files):
            if gl_config.rules:
                for rule in gl_config.rules:
                    status = VerificationStatus(config_file=config_file, rule_id=rule.id)
                    for secret_file in _secret_files(rule.id):
                        status.tested = True
                        _verify(status, rule.id, secret_file, config_file)
                    if not status.valid():
                        failures.append(status)
                
    report = [f.__dict__ for f in failures]
    _json = json.dumps(report, indent=2)
    if dst:
        with open(dst) as fp:
            fp.write(_json)
    else:
        click.echo(_json)
    return report

class CopyTempFile():
    def __init__(self, src: str, tmp: str) -> None:
        self.src = src
        self.tmp = tmp
        self.dst = None
    
    def __enter__(self):
        dst = str(os.path.join(self.tmp, str(os.path.basename(self.src))))
        # only delete file if we put it there
        if (not os.path.exists(dst)):
            self.dst = dst
            shutil.copyfile(self.src, self.dst)
            logger.info(f"Copied '{self.src}' to '{self.dst}'")
        return dst
  
    def __exit__(self, *args):
        if (self.dst):
            os.remove(self.dst)
            logger.info(f"Removed '{self.dst}'")

@dataclass
class VerificationStatus:
    config_file: str
    rule_id: str
    tested: bool = False
    failures: list[str] = field(default_factory=list)
    def fail(self, secret_file):
        self.failures.append(secret_file)
    def valid(self):
        return self.tested and not self.failures

@click.command('verify')
@click.option('-d', '--dst', help='Destination file to output to')
@click.option('-s', '--secrets', default='secrets', help='Folder with secrets to test rules')
@click.argument('config_files', nargs=-1)
def verify_command(config_files: str, secrets: str, dst: str=None):
    report = verify_config(config_files, secrets, dst)
    if report:
        sys.exit(1)
    
if __name__ == "__main__":
    verify_command()
