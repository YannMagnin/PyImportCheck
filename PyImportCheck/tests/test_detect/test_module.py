"""
tests.test_detec.test_module    - check broken module
"""
from pathlib import Path

from pyimportcheck.core.scan import pic_scan_package
from pyimportcheck.core.detect._module import pic_detect_module_invalid
from pyimportcheck.core.detect import PicDetectNotification

#---
# Internals
#---

_PREFIX_PKG = Path(f"{__file__}/../../_data/brokenpkg").resolve()
_SCANINFO   = [
    PicDetectNotification(
        type    = 'error',
        path    = _PREFIX_PKG,
        log     = 'brokenpkg: missing critical `__init__.py` file',
    ),
    PicDetectNotification(
        type        = 'error',
        path        = _PREFIX_PKG/'prout',
        log         = \
            'brokenpkg/prout: missing critical `__init__.py` file',
    ),
]

#---
# Public
#---

def test_module() -> None:
    """ test broken module detection
    """
    scaninfo = pic_scan_package(_PREFIX_PKG)
    detectinfo = pic_detect_module_invalid(scaninfo)
    print('-== check each notification ==-')
    for notif in detectinfo:
        print(notif.debug_show())
    print('-== check notification validity ==-')
    for notif in _SCANINFO:
        print(f"looking for ==> {notif.debug_show()}")
        assert notif in detectinfo
        detectinfo.remove(notif)
    print("-== check remaining notifications ==-")
    assert len(detectinfo) == 0
