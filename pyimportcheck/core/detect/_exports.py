"""
pyimportcheck.core.detect._exports  - check missing / bad `__all__` symbol
"""
__all__ = [
    'pic_detect_exports_mistake',
]
from typing import Dict, List, Any

from pyimportcheck.core.detect.types import PicDetectNotification
from pyimportcheck.core.scan import (
    PicScannedModule,
    PicScannedFile,
)

#---
# Internals
#---

def _pic_check_missing_export(
    info: PicScannedFile,
) -> List[PicDetectNotification]:
    """ check missing `__all__` declaration
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

def _pic_check_mismatched_export(
    info: PicScannedFile,
) -> List[PicDetectNotification]:
    """ check mismatched `__all__` declaration

    @notes
    - check that no private symbols has been exported
    - check if a symbols has been exported multiple time
    - check that exported symbols exists
    """
    notifications = []
    expected_exports: Dict[str,Any] = {}
    for syminfo in info.symbols.values():
        if not syminfo.name.startswith('_'):
            expected_exports[syminfo.name] = 0
    for exp in info.exports:
        if exp.name in expected_exports:
            if expected_exports[exp.name] > 0:
                notifications.append(
                    PicDetectNotification(
                        type    = 'warning',
                        log     = \
                            f"{info.path}:{exp.lineno}: exported symbol "
                            f"'{exp.name}' has already been exported, "
                            'you can remove this line',
                    ),
                )
            expected_exports[exp.name] += 1
            continue
        if exp.name in info.symbols:
            notifications.append(
                PicDetectNotification(
                    type    = 'warning',
                    log     = \
                        f"{info.path}:{exp.lineno}: exported symbol "
                        f"'{exp.name}' should not be exported",
                )
            )
            continue
        notifications.append(
            PicDetectNotification(
                type    = 'error',
                log     = \
                    f"{info.path}:{exp.lineno}: exported symbol "
                    f"'{exp.name}' doest not exists",
            ),
        )
    for expname, expcnt in expected_exports.items():
        if expcnt != 0:
            continue
        notifications.append(
            PicDetectNotification(
                type    = 'error',
                log     = \
                    f"{info.path}: missing exported symbol '{expname}'"
            ),
        )
    return notifications

def _pic_check_export_validity(
    info: PicScannedFile,
) -> List[PicDetectNotification]:
    """ check `__all__` declaration
    """
    if notifications := _pic_check_missing_export(info):
        return notifications
    if notifications := _pic_check_mismatched_export(info):
        return notifications
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
