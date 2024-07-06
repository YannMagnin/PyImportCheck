"""
pyimportcheck.core.detect - circular import detector
"""
__all__ = [
    'pycycle_detect_circular_import',
]
from typing import List, Tuple, Dict, Any, Union
from pathlib import Path

from pyimportcheck.core.exception import PycycleException
from pyimportcheck.core._logger import log_warning, log_error

#---
# Internals
#---

def _resolve_package(
    root_info: Dict[str,Any],
    import_name: str,
    import_lineno: int,
    import_list: List[Tuple[int,str]],
) -> Union[List[Tuple[int,str]],None]:
    """ resolve a package and avoid circular import
    """
    for import_info in import_list:
        if import_info[1] == import_name:
            return import_list
    target = root_info
    import_shard = import_name.split('.')
    assert import_shard[0] == root_info['package']
    for shard in import_shard[1:]:
        if target['type'] == 'file':
            raise PycycleException('Bad file type')
        if shard not in target['modules']:
            raise PycycleException(f"Unable to import {import_name}")
        target = target['modules'][shard]
    if target['type'] == 'module':
        if '__init__' not in target['modules']:
            log_warning('Missing __init__ file')
            return None
        target = target['modules']['__init__']
    for next_import_lineno, next_import_name in target['imports']:
        valid = _resolve_package(
            root_info,
            next_import_name,
            next_import_lineno,
            import_list + [(import_lineno, import_name)],
        )
        if valid:
            return valid
    return None

def _check_circular(
    _pathfile: Path,
    import_list: List[Tuple[int,str]],
    package: str,
    root_info: Dict[str,Any],
) -> int:
    """ check circular import
    """
    error_counter = 0
    for import_line, import_name in import_list:
        circular_list = _resolve_package(
            root_info,
            import_name,
            import_line,
            [],
        )
        if not circular_list:
            continue
        error = f"({str(_pathfile)}) {package}:{import_line} -> "
        for import_cycle_lineno, import_cycle_name in circular_list[:-1]:
            error += f"{import_cycle_name}:{import_cycle_lineno} -> "
        error += f"{circular_list[-1][1]}:{circular_list[-1][0]}"
        log_error(error)
        error_counter += 1
    return error_counter

def _pycycle_check_import(
    root_info: Dict[str,Any],
    info: Dict[str,Any],
    package: str,
) -> int:
    """ recursively resolve all dependencies
    """
    error_counter = 0
    for module, module_info in info.items():
        if module_info['type'] == 'module':
            error_counter += _pycycle_check_import(
                root_info,
                module_info['modules'],
                f"{package}.{module}",
            )
            continue
        error_counter += _check_circular(
            module_info['path'].resolve().relative_to(
                (root_info['prefix']/'..').resolve(),
            ),
            module_info['imports'],
            f"{package}.{module}",
            root_info,
        )
    return error_counter

#---
# Public
#---

def pycycle_detect_circular_import(info: Dict[str,Any]) -> int:
    """ try to detect circular import
    """
    error_counter = _pycycle_check_import(
        info,
        info['modules'],
        info['package'],
    )
    if error_counter > 0:
        log_error(f"Detected {error_counter} cyclic import")
    return error_counter
