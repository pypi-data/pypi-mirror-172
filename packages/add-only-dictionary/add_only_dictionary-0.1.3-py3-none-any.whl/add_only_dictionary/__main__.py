"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Add Only Dictionary."""


if __name__ == "__main__":
    main(prog_name="add-only-dictionary")  # pragma: no cover
