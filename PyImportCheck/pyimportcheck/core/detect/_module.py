"""
pyimportcheck.core.detect._import   - check module validity
"""
__all__ = [
    'pic_detect_module_invalid',
]
from typing import List

from pyimportcheck.core.scan import PicScannedModule
from pyimportcheck.core.detect.types import PicDetectNotification

#---
# Internals
#---

def _pic_generate_notification(
    root:   PicScannedModule,
    module: PicScannedModule,
) -> PicDetectNotification:
    """ generate a notification
    """
    pathfile = module.path.resolve().relative_to(
        (root.path/'..').resolve(),
    )
    return PicDetectNotification(
        type    = 'error',
        path    = pathfile,
        log     = f"{pathfile}: missing critical `__init__.py` file",
    )


def _pic_detect_module_invalid(
    root:    PicScannedModule,
    current: PicScannedModule,
) -> List[PicDetectNotification]:
    """ check missing `__init__.py` file
    """
    notifications: List[PicDetectNotification] = []
    if '__init__' not in current.modules:
        notifications.append(_pic_generate_notification(root, current))
    for module_info in current.modules.values():
        if isinstance(module_info, PicScannedModule):
            notifications += _pic_detect_module_invalid(root, module_info)
    return notifications

#---
# Public
#---

def pic_detect_module_invalid(
    current: PicScannedModule,
) -> List[PicDetectNotification]:
    """ check missing `__init__.py` file
    """
    return _pic_detect_module_invalid(current, current)
