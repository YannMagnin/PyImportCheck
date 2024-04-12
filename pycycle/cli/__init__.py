"""
pycycle.cli   - Crupy CLI entry
"""
__all__ = [
    'pycycle_cli_entry',
]
from typing import NoReturn
from pathlib import Path
import sys

import click

from pycycle.core.scan import pycycle_scan_package
from pycycle.core.detect import pycycle_detect_circular_import

#---
# Public
#---

@click.command('pycycle')
@click.option(
    '-p', '--prefix', 'package_prefix',
    required    = True,
    metavar     = 'PACKAGE_PREFIX',
    help        = 'package prefix to analyse',
    type        = click.Path(
        exists      = True,
        file_okay   = False,
        dir_okay    = True,
        path_type   = Path,
    ),
)
@click.version_option()
def pycycle_cli_entry(package_prefix: Path) -> NoReturn:
    """ Python circular import detector
    """
    info = pycycle_scan_package(package_prefix)
    pycycle_detect_circular_import(info)
    sys.exit(0)
