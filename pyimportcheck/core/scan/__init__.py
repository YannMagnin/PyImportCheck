"""
pyimportcheck.core.scan   - python package scanner
"""
__all__ = [
    'pycycle_scan_package',
]
from typing import Dict, List, Any
from pathlib import Path
import re

from pyimportcheck.core.exception import PycycleException
from pyimportcheck.core._logger import (
    log_warning,
    log_error,
)

#---
# Internals
#---

def _pycycle_analyse_file(
    file_info: Dict[str,Any],
    prefix: Path,
    package: str,
) -> None:
    """ load the file and manually parse import
    """

def _pycycle_scan_package(
    info: Dict[str,Any],
    prefix: Path,
    package: str,
) -> None:
    """ recursively scan package folders
    """
    for filepath in prefix.iterdir():
        if filepath.name in ['__pycache__', 'py.typed']:
            continue
        if filepath.name.startswith('.'):
            continue
        if filepath.is_dir():
            info[filepath.name] = {
                'type': 'module',
                'modules': {}
            }
            _pycycle_scan_package(
                info[filepath.name]['modules'],
                filepath,
                package,
            )
            continue
        if not filepath.name.endswith('.py'):
            log_warning(f"file '{str(filepath)}' is not a valid")
            continue
        info[filepath.stem] = {
            'type': 'file',
            'path': filepath,
        }
        _pycycle_analyse_file(
            info[filepath.stem],
            filepath,
            package,
        )

#---
# Public
#---

def pycycle_scan_package(prefix: Path) -> Dict[str,Any]:
    """ package scanner
    """
    if not (prefix/'__init__.py').exists():
        raise PycycleException(
            'The provided package prefix do not have __init__.py file'
        )
    info: Dict[str,Any] = {
        'prefix':   prefix,
        'package':  prefix.name,
        'type':     'module',
        'modules':  {},
    }
    _pycycle_scan_package(info['modules'], prefix, prefix.name)
    return info
