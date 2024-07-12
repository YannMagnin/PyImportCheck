"""
pyimportcheck.core.detect - circular import detector
"""
__all__ = [
    'pic_detect_all',
]

from pyimportcheck.core.detect._import import pic_detect_import_circular
from pyimportcheck.core.scan import PicScannedModule

#---
# Public
#---

def pic_detect_all(info: PicScannedModule) -> int:
    """ run all detector
    """
    ret  = 0
    ret += pic_detect_import_circular(info)
    return ret
