"""
pyimportcheck.cli   - Crupy CLI entry
"""
__all__ = [
    'pyimportcheck_cli_entry',
]
from typing import NoReturn
from pathlib import Path
from importlib.metadata import version
import sys

import click

from pyimportcheck.core.scan import pycycle_scan_package
from pyimportcheck.core.detect import pycycle_detect_circular_import

#---
# Public
#---

@click.command('pyimportcheck')
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
@click.version_option(message='%(version)s')
def pyimportcheck_cli_entry(package_prefix: Path) -> NoReturn:
    """ Python circular import detector
    """
    info = pycycle_scan_package(package_prefix)
    error = pycycle_detect_circular_import(info)
    sys.exit(0 if error == 0 else 1)
