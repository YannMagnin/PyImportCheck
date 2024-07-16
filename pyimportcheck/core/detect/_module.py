"""
pyimportcheck.core.detect._import   - check module validity
"""
__all__ = [
    'pic_detect_module_invalid',
]

from pyimportcheck.core._logger import log_error
from pyimportcheck.core.scan import PicScannedModule

#---
# Internals
#---

def _pic_check_module_walk(
    root:    PicScannedModule,
    current: PicScannedModule,
) -> int:
    """ walk through scanned information and performs various check
    """
    error_counter = 0
    for _, module_info in current.modules.items():
        if not isinstance(module_info, PicScannedModule):
            continue
        if '__init__' not in module_info.modules:
            log_error(
                f"{module_info.path}: missing critical `__init__.py` file"
            )
        error_counter += _pic_check_module_walk(
            root    = root,
            current = module_info,
        )
    return error_counter

#---
# Public
#---

def pic_detect_module_invalid(info: PicScannedModule) -> int:
    """ check missing `__init__.py` file
    """
    return _pic_check_module_walk(
        root    = info,
        current = info,
    )
