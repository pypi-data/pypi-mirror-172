""" Sensospot Data Parser

Parsing the numerical output from Sensovations Sensospot image analysis.
"""

__version__ = "1.0.1"


import pathlib

import click
import pandas

from . import columns  # noqa: F401
from .parser import parse_file, parse_folder  # noqa: F401

DEFAULT_OUTPUT_FILENAME = "collected_data.csv"


@click.command()
@click.argument(
    "sources",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    required=True,
    nargs=-1,
)
@click.option(
    "-o",
    "--output",
    is_flag=False,
    flag_value=DEFAULT_OUTPUT_FILENAME,
    type=click.Path(exists=False, dir_okay=False),
    help=f"Output file path, defaults to '{DEFAULT_OUTPUT_FILENAME}'",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Ignore Sanity Check",
)
def main(sources, output, quiet=False):
    """Parses the measurement results of the Sensospot reader

    The resulting output is either echoed to stdout or saved to a file.

    """
    paths = (pathlib.Path(source) for source in sources)
    collection = (parse_folder(source, quiet) for source in paths)
    result = pandas.concat(collection, ignore_index=True).to_csv(
        output, sep="\t", index=False
    )
    # if 'output' is None, the call to 'to_csv()' returns the csv as text
    # if 'output' is not None, 'to_csv()' writes to the file and returns None
    if result:
        click.echo(result)
