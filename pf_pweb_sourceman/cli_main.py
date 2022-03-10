import click
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.task.project_manager import pm


@click.group()
def bsw():
    console.blue("-------------------", bold=True)
    console.green("PWeb Source Manager", bold=True)
    console.blue("-------------------", bold=True)


@click.command()
@click.option("--repo", "-r", help="Give Project Git Repository", required=True)
@click.option("--directory", "-d", help="Project directory name", default="pweb", show_default=True)
@click.option("--branch", "-b", help="Enter project branch", default="dev", show_default=True)
@click.option("--mode", "-m", help="Enter Project Mode", default="dev", show_default=True, type=click.Choice(['dev', 'prod'], case_sensitive=False))
def setup(repo, directory, branch, mode):
    pm.setup(repo, directory, branch, mode)
    console.log(repo)
    console.log(directory)
    console.log(branch)
    console.log(mode)


bsw.add_command(setup)
