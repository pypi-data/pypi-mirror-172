import click
from . import gitleaks_r as gl_r, gitleaks_w as gl_w, gitleaks_model as model

def sort(config, dst=None):
    
    # extract & transform
    gl = gl_r.load(config)
    
    # load
    if dst:
        with open(dst, 'wb') as f:
            gl_w.dump(gl, f)
    else:
        click.echo(gl_w.dumps(gl))
    return gl
    
@click.command('sort')
@click.option('-d', '--dst', help='Destination file to output to')
@click.argument('config_file', default=model.GITLEAKS_DEFAULT_CONFIG_FILE)
def sort_command(config_file, dst=None):
    sort(config_file, dst)

if __name__ == "__main__":
    sort()
