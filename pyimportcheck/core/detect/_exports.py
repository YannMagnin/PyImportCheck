"""
pyimportcheck.core.detect._exports  - check missing / bad `__all__` symbol
"""
__all__ = [
    'pic_detect_exports_mistake',
]
from typing import List

from pyimportcheck.core.detect.types import PicDetectNotification
from pyimportcheck.core.scan import (
    PicScannedModule,
    PicScannedFile,
)

#---
# Internals
#---

def _pic_check_export_validity(
    info: PicScannedFile,
) -> List[PicDetectNotification]:
    """ check `__all__` declaration

    @notes
    - check that the `__all__` exist
    - check that exported symbols exists
    - check if internal symbols is exported (only if its a public file)
    """
    if '__all__' not in info.symbols:
        if not info.symbols:
            return []
        log  = f"{info.path}: missing `__all__` symbol, which can be "
        log += 'declared as follow:\n'
        log += '>>> __all__ = [\n'
        for sym in info.symbols.keys():
            if not sym.startswith('_'):
                log += f">>>     '{sym}',\n"
        log += '>>> ]'
        return [
            PicDetectNotification(
                type    = 'warning',
                log     = log,
            ),
        ]
    return []

#---
# Public
#---

def  pic_detect_exports_mistake(
    current: PicScannedModule,
) -> List[PicDetectNotification]:
    """ check missing / bad `__all__` declaration
    """
    notifications: List[PicDetectNotification] = []
    for _, module_info in current.modules.items():
        if isinstance(module_info, PicScannedModule):
            notifications += pic_detect_exports_mistake(module_info)
            continue
        notifications += _pic_check_export_validity(module_info)
    return notifications
