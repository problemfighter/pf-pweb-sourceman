import click
from pf_pweb_sourceman.common.console import console
from pf_pweb_sourceman.pwebsm.descriptor_const import UIType, AppMode
from pf_pweb_sourceman.task.project_init import pi
from pf_pweb_sourceman.task.project_manager import pm


@click.group()
def bsw():
    console.blue("-------------------", bold=True)
    console.green("PWeb Source Manager", bold=True)
    console.blue("-------------------", bold=True)


@click.command()
@click.option("--repo", "-r", help="Give Project Git Repository", required=True)
@click.option("--directory", "-d", help="Project directory name", default=None, show_default=True)
@click.option("--branch", "-b", help="Enter project branch", default="dev", show_default=True)
@click.option("--environment", "-e", help="Enter project environment name", default=None, show_default=True)
@click.option("--mode", "-m", help="Enter Project Mode", default=AppMode.dev, show_default=True, type=click.Choice([AppMode.dev, AppMode.prod], case_sensitive=False))
def setup(repo, directory, branch, environment, mode):
    try:
        pm.setup(repo, directory, branch, mode, environment)
    except Exception as e:
        console.error(str(e))


@click.command()
@click.option("--mode", "-m", help="Enter Project Mode", default=AppMode.dev, show_default=True, type=click.Choice([AppMode.dev, AppMode.prod], case_sensitive=False))
@click.option("--environment", "-e", help="Enter project environment name", default=None, show_default=True)
def update(mode, environment):
    try:
        pm.update(mode, environment)
    except Exception as e:
        console.error(str(e))


@click.command()
@click.option("--name", "-n", help="Project name", default=None, show_default=True, required=True)
@click.option("--port", "-p", help="Project run on the port", default=1212, show_default=True, type=int)
@click.option("--directory", "-d", help="Project directory name", default=None, show_default=True)
@click.option("--mode", "-m", help="Enter Project Mode", default=AppMode.binary, show_default=True, type=click.Choice([AppMode.dev, AppMode.binary], case_sensitive=False))
@click.option("--ui-type", "-ui", help="Enter Project UI Type", default=UIType.ssr, show_default=True, type=click.Choice([UIType.react, UIType.ssr, UIType.api], case_sensitive=False))
def init(name, port, directory, mode, ui_type):
    try:
        pi.init(name, port, directory, mode, ui_type)
    except Exception as e:
        console.error(str(e))


bsw.add_command(setup)
bsw.add_command(update)
bsw.add_command(init)
