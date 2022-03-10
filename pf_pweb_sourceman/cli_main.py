import click
from pf_pweb_sourceman.common.console import console


@click.group()
def bsw():
    console.blue("-------------------", bold=True)
    console.green("PWeb Source Manager", bold=True)
    console.blue("-------------------", bold=True)


@click.command()
@click.option("--repo", "-r", help="Give Project Git Repository", required=True)
@click.option("--mode", "-m", help="Enter Project Mode", default="dev", show_default=True, type=click.Choice(['dev', 'prod'], case_sensitive=False))
def setup(repo, mode=None):
    console.log(repo)
    console.log(mode)


bsw.add_command(setup)
