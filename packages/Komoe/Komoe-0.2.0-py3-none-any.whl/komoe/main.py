import click

from pathlib import Path


@click.group()
def main():
    pass


@main.command()
@click.argument(
    "path",
    default=".",
    type=click.Path(file_okay=False, path_type=Path),
)
@click.option("--project-name", "-N", prompt=True, required=True)
def new(path, name):
    "Creates a new project"

    if path.exists():
        entries = [entry for entry in path.iterdir() if not entry.name.startswith(".")]
        if len(entries) != 0:
            path_repr = str(path)
            if path_repr == ".":
                path_repr = "the current directory"
            raise click.ClickException(f"{path_repr} isn't empty")

    print(f"{path=}")
    print(f"{name=}")
