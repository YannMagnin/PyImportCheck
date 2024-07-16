"""
pyimportcheck.core.detect - circular import detector
"""
__all__ = [
    'pic_detect_all',
]

from pyimportcheck.core.detect._circular import pic_detect_circular_import
from pyimportcheck.core.detect._exports import pic_detect_exports_mistake
from pyimportcheck.core.detect._module import pic_detect_module_invalid
from pyimportcheck.core.scan import PicScannedModule
from pyimportcheck.core._logger import (
    log_error,
    log_info,
)

#---
# Public
#---

def pic_detect_all(info: PicScannedModule) -> int:
    """ run all detector
    """
    error = {'total' : 0}
    mapping = {
        'circular import': pic_detect_circular_import,
        '`__all__` declaration': pic_detect_exports_mistake,
        'missing `__init__.py` file': pic_detect_module_invalid,
    }
    for desc, func in mapping.items():
        error[desc] = func(info)
        error['total'] += error[desc]
    if error['total'] > 0:
        log_info('==========================')
    for desc, total in error.items():
        if desc == 'total':
            continue
        if total > 0:
            log_info(f"Detected {total} {desc} error")
    return error['total']
