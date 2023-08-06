import click
from .gitleaks_sort import sort_command
from .gitleaks_diff import diff_command
from .gitleaks_verify import verify_command
from .gitleaks_merge import merge_command
import logging

@click.group
@click.option('-x', '--debug', 'log_level', default='WARN', help='debug logging level')
def cli(log_level):
    logging.basicConfig(level=logging._nameToLevel.get(log_level))

cli.add_command(sort_command)
cli.add_command(diff_command)
cli.add_command(verify_command)
cli.add_command(merge_command)

if __name__ == "__main__":
    cli()