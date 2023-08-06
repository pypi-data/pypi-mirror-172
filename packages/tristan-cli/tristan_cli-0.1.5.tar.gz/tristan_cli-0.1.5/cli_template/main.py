import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Setup git-leaks automatically
    """


@app.command()
def initialize(name: str):
    """
    Setup Git-Leaks
    :type name: str The user's name
    """
    typer.echo(f"Git-Leaks setup successfully for {name}, we can all go home")

