"""
pyimportcheck.core.detect._circular - detect circular import
"""
__all__ = [
    'pic_detect_circular_import',
]
from typing import List, Union
from pathlib import Path

from pyimportcheck.core.exception import PicException
from pyimportcheck.core._logger import log_warning, log_error
from pyimportcheck.core.scan import (
    PicScannedModule,
    PicScannedImport,
    PicScannedFile,
)

#---
# Internals
#---

def _pic_resolve_package(
    root_info: PicScannedModule,
    import_current: PicScannedImport,
    import_list: List[PicScannedImport],
) -> Union[List[PicScannedImport],None]:
    """ resolve a package and avoid circular import
    """
    for import_info in import_list:
        if import_info.name == import_current.name:
            return import_list
    target: Union[PicScannedModule,PicScannedFile] = root_info
    for shard in import_current.path.split('.')[1:]:
        if isinstance(target, PicScannedFile):
            raise PicException('Bad file type')
        if shard not in target.modules:
            raise PicException(f"Unable to import {import_current.name}")
        target = target.modules[shard]
    if isinstance(target, PicScannedModule):
        if '__init__' not in target.modules:
            log_warning('Missing __init__ file')
            return None
        target = target.modules['__init__']
    assert isinstance(target, PicScannedFile)
    for next_import in target.imports:
        valid = _pic_resolve_package(
            root_info,
            next_import,
            import_list + [next_import],
        )
        if valid:
            return valid
    return None

def _pic_check_circular(
    _pathfile: Path,
    import_list: List[PicScannedImport],
    package: str,
    root_info: PicScannedModule,
) -> int:
    """ check circular import
    """
    error_counter = 0
    for imp in import_list:
        circular_list = _pic_resolve_package(
            root_info,
            imp,
            [],
        )
        if not circular_list:
            continue
        error = f"({str(_pathfile)}) {package}:{imp.lineno} -> "
        for import_cycle in circular_list[:-1]:
            error += f"{import_cycle.name}:{import_cycle.lineno} -> "
        error += f"{circular_list[-1].name}:{circular_list[-1].lineno}"
        log_error(error)
        error_counter += 1
    return error_counter

def _pic_check_import(
    root_info: PicScannedModule,
    info: PicScannedModule,
    package: str,
) -> int:
    """ recursively resolve all dependencies
    """
    error_counter = 0
    for module, module_info in info.modules.items():
        if isinstance(module_info, PicScannedModule):
            error_counter += _pic_check_import(
                root_info,
                module_info,
                f"{package}.{module}",
            )
            continue
        error_counter += _pic_check_circular(
            module_info.path.resolve().relative_to(
                (root_info.path/'..').resolve(),
            ),
            module_info.imports,
            f"{package}.{module}",
            root_info,
        )
    return error_counter

#---
# Public
#---

def pic_detect_circular_import(info: PicScannedModule) -> int:
    """ try to detect circular import
    """
    error_counter = _pic_check_import(
        info,
        info,
        info.name,
    )
    return error_counter
