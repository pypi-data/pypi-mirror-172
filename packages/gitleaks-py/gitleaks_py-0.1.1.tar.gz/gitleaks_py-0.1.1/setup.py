# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitleaks_py']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'requests>=2.28.1,<3.0.0',
 'tomli-w>=1.0.0,<2.0.0',
 'tomli>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'gitleaks-py',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Gitleaks configuration utilities\n\n[Gitleaks](https://github.com/zricethezav/gitleaks)  is a SAST tool for detecting and preventing hardcoded secrets like passwords, api keys, and tokens in git repos.\n\n`gitleaks-py` provides a python library and CLI to manage Gitleaks rule configurations:\n\n* Compare configurations using sort and diff\n* Verify rules against fixture files containing secrets\n* Merge rules from multiple files into a single file\n\n## Sort\n\nSort Gitleaks config file by case-insensitive rule ID.\n\n```bash\npython -m gitleaks_py.cli sort [OPTIONS] CONFIG_FILE\n```\n\n* `CONFIG_FILE`\n  File or URL to sort\n\n* `-d`, `--dst`\n  Output destination file. Writes to `std-out` if omitted\n\n## Diff\n\nDiff two config files.\n\n```bash\npython -m gitleaks_py.cli diff [OPTIONS] CONFIG_FILE [DEFAULT_CONFIG_FILE]\n```\n\n* `CONFIG_FILE`\n  File or URL to diff\n\n* `DEFAULT_CONFIG_FILE`\n  File or URL to diff against.\n  Defaults to [gitleaks default config file](https://raw.githubusercontent.com/zricethezav/gitleaks/master/config/gitleaks.toml)\n\n* `-d`, `--dst`\n  Output destination file. Writes to `std-out` if omitted\n\n* `-o`, `--omissions`\n  Display omissions (rules from default config, not found in config)\n\n* `-a`, `--additions`\n  Display additions (rule from config, not found in default config)\n\n## Verify\n\nVerify config file against secrets held in sample files.\n\n```bash\npython -m gitleaks_py.cli verify [OPTIONS] CONFIG_FILE\n```\n\n* `CONFIG_FILE`\n  File or URL to verify\n\n* `-d`, `--dst`\n  Output destination file. Writes to `std-out` if omitted\n\n* `-s`, `--secrets`\n  Folder with secrets to test rules. Defaults to `./secrets`\n\n  Files should be named with the rule id followed by a _dot_.\n  e.g. `uk-gov-notify-api-key.txt`\n\n  Multiple files with secrets can be tested against the same rule by use of an additional suffix.\n  e.g. `uk-gov-notify-api-key.1.txt`, `uk-gov-notify-api-key.2.txt`\n\n## Merge\n\nMerge multiple config files into one\n\n```bash\npython -m gitleaks_py.cli merge [OPTIONS] [CONFIG_FILES]...\n```\n\n* `CONFIG_FILES`\n  A space separated list of files to merge. Glob patterns may be used. e.g. `toml/*.toml`\n\n* `-t`, `--title`\n  Output config title. Joins titles from files if omitted\n\n* `-d`, `--dst`\n  Output destination file. Writes to `std-out` if omitted\n',
    'author': 'Pat',
    'author_email': 'patrick.turner@nhs.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
