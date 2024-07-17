"""
pyimportcheck.cli   - Crupy CLI entry
"""
__all__ = [
    'pyimportcheck_cli_entry',
]
from typing import NoReturn
from pathlib import Path
import sys

import click

from pyimportcheck.core.scan import pic_scan_package
from pyimportcheck.core.detect import pic_detect_all
from pyimportcheck.core.output import pic_output_stdout

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
    info = pic_scan_package(package_prefix)
    report = pic_detect_all(info)
    sys.exit(pic_output_stdout(report))
