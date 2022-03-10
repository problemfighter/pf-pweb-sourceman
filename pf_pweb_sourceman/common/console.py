import click


class Console:

    def log(self, text):
        print(text)

    def green(self, text, bold=False):
        click.echo(click.style(text, fg='green', bold=bold))

    def blue(self, text, bold=False):
        click.echo(click.style(text, fg='blue', bold=bold))

    def red(self, text, bold=False):
        click.echo(click.style(text, fg='red', bold=bold))


console = Console()
