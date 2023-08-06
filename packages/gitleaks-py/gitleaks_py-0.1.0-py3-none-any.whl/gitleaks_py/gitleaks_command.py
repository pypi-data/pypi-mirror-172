from dataclasses import dataclass, field
import subprocess
import tempfile
import os.path as os_path
import json

def _read_report(report_file):
    with open(report_file) as f:
        _dict = json.load(f)
        report = GitleaksReport()
        for violation in _dict:
            report.violations.append(GitleaksViolation.from_json_dict(violation))
        return report
    
def detect(gl_config_file, scan_directory):
    with tempfile.TemporaryDirectory() as tmpdir:
        report_file = os_path.join(tmpdir, 'report.json')
        args = ['gitleaks', 'detect', '--no-git', '-c', gl_config_file, '-s', scan_directory, '-r', report_file]
        result = subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return _read_report(report_file)
        
@dataclass
class GitleaksViolation():
    def from_json_dict(__dict):
        return GitleaksViolation(
            __dict.get('Description'),
            __dict.get('StartLine'),
            __dict.get('EndLine'),
            __dict.get('StartColumn'),
            __dict.get('EndColumn'),
            __dict.get('Match'),
            __dict.get('Secret'),
            __dict.get('File'),
            __dict.get('Commit'),
            __dict.get('Entropy'),
            __dict.get('Author'),
            __dict.get('Email'),
            __dict.get('Date'),
            __dict.get('Message'),
            __dict.get('Tags'),
            __dict.get('RuleID'),
            __dict.get('Fingerprint')
        )
        
    description: str=None
    start_line: int=None
    end_line: int=None
    start_column: int=None
    end_column: int=None
    match: str=None
    secret: str=None
    file: str=None
    commit: str=None
    entropy: float=None
    author: str=None
    email: str=None
    date: str=None
    message: str=None
    tags: list[str]=field(default_factory=list)
    rule_id: str=None
    fingerprint: str=None

@dataclass
class GitleaksReport():
    violations: list[GitleaksViolation]=field(default_factory=list)
    def violations_for_rule_id(self, rule_id):
        return [violation for violation in self.violations if violation.rule_id == rule_id]
    