"""
pyimportcheck.core.detect - circular import detector
"""
__all__ = [
    'pic_detect_all',
    'PicDetectReport',
    'PicDetectNotification',
]

from pyimportcheck.core.detect.types import (
    PicDetectReport,
    PicDetectNotification,
)
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

def pic_detect_all(info: PicScannedModule) -> PicDetectReport:
    """ run all detector
    """
    report = PicDetectReport(notifications={})
    mapping = {
        'circular import': pic_detect_circular_import,
        '`__all__` declaration': pic_detect_exports_mistake,
        'missing `__init__.py` file': pic_detect_module_invalid,
    }
    for desc, func in mapping.items():
        report.notifications[desc] = func(info)
    return report
