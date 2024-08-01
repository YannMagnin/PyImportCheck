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
# Public
#---

def pic_detect_module_invalid(
    current: PicScannedModule,
) -> List[PicDetectNotification]:
    """ check missing `__init__.py` file
    """
    notifications: List[PicDetectNotification] = []
    for _, module_info in current.modules.items():
        if not isinstance(module_info, PicScannedModule):
            continue
        if '__init__' not in module_info.modules:
            notifications.append(
                PicDetectNotification(
                    type    = 'error',
                    path    = module_info.path,
                    log     = \
                        f"{module_info.path}: missing critical "
                        '`__init__.py` file'
                )
            )
        notifications += pic_detect_module_invalid(module_info)
    return notifications
