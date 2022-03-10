import click
from pf_pweb_sourceman.common.console import console


@click.group()
def bsw():
    console.blue("-------------------", bold=True)
    console.green("PWeb Source Manager", bold=True)
    console.blue("-------------------", bold=True)


@click.command()
def setup():
    console.red('Setup Project')
    click.echo(click.style('Hello World!', fg='green'))
    click.echo(click.style('Some more text', bg='blue', fg='white'))
    click.echo(click.style('ATTENTION', blink=True, bold=True))


bsw.add_command(setup)
