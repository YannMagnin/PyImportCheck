"""
pycycle.core.scan   - python package scanner
"""
__all__ = [
    'pycycle_scan_package',
]
from typing import Dict, List, Tuple, Any
from pathlib import Path
import re

from pycycle.core.exception import PycycleException
from pycycle.core._logger import log_warning

#---
# Internals
#---

def _pycycle_analyse_file(
    info: List[Tuple[int,str]],
    prefix: Path,
    package: str,
) -> None:
    """ load the file and manually parse import
    """
    with open(prefix, 'r', encoding='utf8') as pyfile:
        for i, line in enumerate(pyfile):
            import_info = re.match(
                rf'^from (?P<pypath>{package}((\.[a-z_]+)?)+)',
                line
            )
            if not import_info:
                continue
            info.append((i+1, import_info['pypath']))

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
            'import': [],
        }
        _pycycle_analyse_file(
            info[filepath.stem]['import'],
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
