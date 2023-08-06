# Gitleaks configuration utilities

[Gitleaks](https://github.com/zricethezav/gitleaks)  is a SAST tool for detecting and preventing hardcoded secrets like passwords, api keys, and tokens in git repos.

`gitleaks-py` provides a python library and CLI to manage Gitleaks rule configurations:

* Compare configurations using sort and diff
* Verify rules against fixture files containing secrets
* Merge rules from multiple files into a single file

## Sort

Sort Gitleaks config file by case-insensitive rule ID.

```bash
python -m gitleaks_py.cli sort [OPTIONS] CONFIG_FILE
```

* `CONFIG_FILE`
  File or URL to sort

* `-d`, `--dst`
  Output destination file. Writes to `std-out` if omitted

## Diff

Diff two config files.

```bash
python -m gitleaks_py.cli diff [OPTIONS] CONFIG_FILE [DEFAULT_CONFIG_FILE]
```

* `CONFIG_FILE`
  File or URL to diff

* `DEFAULT_CONFIG_FILE`
  File or URL to diff against.
  Defaults to [gitleaks default config file](https://raw.githubusercontent.com/zricethezav/gitleaks/master/config/gitleaks.toml)

* `-d`, `--dst`
  Output destination file. Writes to `std-out` if omitted

* `-o`, `--omissions`
  Display omissions (rules from default config, not found in config)

* `-a`, `--additions`
  Display additions (rule from config, not found in default config)

## Verify

Verify config file against secrets held in sample files.

```bash
python -m gitleaks_py.cli verify [OPTIONS] CONFIG_FILE
```

* `CONFIG_FILE`
  File or URL to verify

* `-d`, `--dst`
  Output destination file. Writes to `std-out` if omitted

* `-s`, `--secrets`
  Folder with secrets to test rules. Defaults to `./secrets`

  Files should be named with the rule id followed by a _dot_.
  e.g. `uk-gov-notify-api-key.txt`

  Multiple files with secrets can be tested against the same rule by use of an additional suffix.
  e.g. `uk-gov-notify-api-key.1.txt`, `uk-gov-notify-api-key.2.txt`

## Merge

Merge multiple config files into one

```bash
python -m gitleaks_py.cli merge [OPTIONS] [CONFIG_FILES]...
```

* `CONFIG_FILES`
  A space separated list of files to merge. Glob patterns may be used. e.g. `toml/*.toml`

* `-t`, `--title`
  Output config title. Joins titles from files if omitted

* `-d`, `--dst`
  Output destination file. Writes to `std-out` if omitted
