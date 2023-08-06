"""
This module is part of the 'web-compressor' package,
which is released under GPL-3.0-only license.
"""

from typing import Union

import click

from ..core import WebCompressor
from .config import Config


@click.command()
@click.argument("source", type=click.Path(exists=True))
@click.option("--config-file", type=click.Path(exists=True), help="Path to config file")
@click.option("-t", "--tasks", help="Tasks to be applied, like '-t mfs'")
@click.version_option("0.4.1")
def cli(source: str, config_file: str, tasks: Union[str, None]) -> None:
    """
    Supercharges HTML files & web assets in SOURCE

    Available tasks: (m)inify & (h)ash assets, (o)ptimize images,
    (f)ormat them as WebP/AVIF, implement (s)ubresource integrity attributes &
    insert 'meta' tag enforcing (c)ontent security policy
    """

    # Engage!
    obj = WebCompressor(source)

    # Load configuration
    config = Config(config_file)

    # Minify web assets
    if tasks is None or "m" in tasks:
        click.echo("Minifying assets ..", nl=False)
        obj.minify_assets(**config.get("minify", {}))
        click.echo(" done!")

    # Optimize images
    if tasks is None or "o" in tasks:
        click.echo("Optimizing images ..", nl=False)
        obj.optimize_images(**config.get("images.optimize", {}))
        click.echo(" done!")

    # Gotta hash 'em all
    if tasks is None or "h" in tasks:
        click.echo("Hashing assets ..", nl=False)
        obj.hash_assets(**config.get("hashing", {}))
        click.echo(" done!")

    # Create modern image formats
    if tasks is None or "f" in tasks:
        click.echo("Converting images to AVIF/WebP ..", nl=False)
        obj.convert_images(**config.get("images.convert", {}))
        click.echo(" done!")

    # Minify HTML files
    if tasks is None or "m" in tasks:
        obj.minify_html(**config.get("minify", {}))

    # Add subresource integrity values (SRI)
    if tasks is None or "s" in tasks:
        click.echo("Minifying assets ..", nl=False)
        obj.generate_sri(**config.get("sri", {}))
        click.echo(" done!")

    # Generate content security policy (CSP)
    if tasks is None or "c" in tasks:
        click.echo("Minifying assets ..", nl=False)
        obj.generate_csp(**config.get("csp", {}))
        click.echo(" done!")

    # Minify HTML files .. again (see comment below)
    if tasks is None or "m" in tasks:
        click.echo("Minifying HTML ..", nl=False)
        obj.minify_html(**config.get("minify", {}))
        click.echo(" done!")

    # NOTE:
    # Minifying HTML files also compresses inline styles/scripts,
    # which interferes with generating hashes for them, and since
    # this leads to invalid hashes, we have twice - any solutions
    # or PRs are welcome!
