"""
pyimportcheck.core.detect._circular - detect circular import
"""
__all__ = [
    'pic_detect_circular_import',
]
from typing import List, Union
from pathlib import Path

from pyimportcheck.core.exception import PicException
from pyimportcheck.core.detect.types import PicDetectNotification
from pyimportcheck.core.scan import (
    PicScannedModule,
    PicScannedImport,
    PicScannedFile,
)

#---
# Internals
#---

def _pic_generate_raise_log(
    module_info:    PicScannedModule,
    import_current: PicScannedImport,
    log:            str,
) -> PicException:
    """ generate exception information
    """
    return PicException(
        f"{module_info.path}:{import_current.lineno}: unable to import "
        f"'{import_current.path}', {log}",
    )

def _pic_resolve_package(
    module_info: PicScannedModule,
    import_current: PicScannedImport,
    import_list: List[PicScannedImport],
) -> Union[List[PicScannedImport],None]:
    """ resolve a package and avoid circular import

    @notes
    - detected circular import are reported through return value
    - detected error are raised using `PicException`
    """
    for import_info in import_list:
        if import_info.name == import_current.name:
            return import_list
    target: Union[PicScannedModule,PicScannedFile] = module_info
    for shard in import_current.path.split('.')[1:]:
        if isinstance(target, PicScannedFile):
            raise _pic_generate_raise_log(
                module_info     = module_info,
                import_current  = import_current,
                log             = \
                    f"because '{target.name}' is a file, or it should be "
                    'a module',
            )
        if shard not in target.modules:
            raise _pic_generate_raise_log(
                module_info     = module_info,
                import_current  = import_current,
                log             = \
                    f"unable to find the '{shard}' file information",
            )
        target = target.modules[shard]
    if isinstance(target, PicScannedModule):
        if '__init__' not in target.modules:
            raise _pic_generate_raise_log(
                module_info     = module_info,
                import_current  = import_current,
                log             = \
                    'unable to find the \'__init__.py\' file information '
                    'required to analyse the module (this mean that all '
                    'files inside this module will be skipped)',
            )
        target = target.modules['__init__']
    assert isinstance(target, PicScannedFile)
    for next_import in target.imports:
        valid = _pic_resolve_package(
            module_info     = module_info,
            import_current  = next_import,
            import_list     = import_list + [next_import],
        )
        if valid:
            return valid
    return None

def _pic_check_circular(
    _pathfile: Path,
    import_list: List[PicScannedImport],
    package: str,
    root_info: PicScannedModule,
) -> List[PicDetectNotification]:
    """ check circular import
    """
    notifications: List[PicDetectNotification] = []
    for imp in import_list:
        try:
            circular_list = _pic_resolve_package(
                root_info,
                imp,
                [],
            )
        except PicException as err:
            notifications.append(
                PicDetectNotification(
                    type    = 'error',
                    log     = str(err),
                ),
            )
            continue
        if not circular_list:
            continue
        error = f"({str(_pathfile)}) {package}:{imp.lineno} -> "
        for import_cycle in circular_list[:-1]:
            error += f"{import_cycle.name}:{import_cycle.lineno} -> "
        error += f"{circular_list[-1].name}:{circular_list[-1].lineno}"
        notifications.append(
            PicDetectNotification(
                type    = 'error',
                log     = error,
            ),
        )
    return notifications

def _pic_check_import(
    root_info: PicScannedModule,
    info: PicScannedModule,
    package: str,
) -> List[PicDetectNotification]:
    """ recursively resolve all dependencies
    """
    notifications: List[PicDetectNotification] = []
    for module, module_info in info.modules.items():
        if isinstance(module_info, PicScannedModule):
            notifications += _pic_check_import(
                root_info,
                module_info,
                f"{package}.{module}",
            )
            continue
        notifications += _pic_check_circular(
            module_info.path.resolve().relative_to(
                (root_info.path/'..').resolve(),
            ),
            module_info.imports,
            f"{package}.{module}",
            root_info,
        )
    return notifications

#---
# Public
#---

def pic_detect_circular_import(
    info: PicScannedModule,
) -> List[PicDetectNotification]:
    """ try to detect circular import
    """
    return _pic_check_import(
        info,
        info,
        info.name,
    )
