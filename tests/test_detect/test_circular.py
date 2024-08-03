"""
tests.test_detect.test_circular - check circular dependency
"""
from pathlib import Path

from pyimportcheck.core.scan import pic_scan_package
from pyimportcheck.core.detect._circular import pic_detect_circular_import
from pyimportcheck.core.detect import PicDetectNotification

#---
# Internals
#---

_PREFIX_PKG = Path(f"{__file__}/../../_data/fakepkg").resolve()
_SCANINFO = [
    PicDetectNotification(
        type    = 'error',
        path    = Path('fakepkg/a.py'),
        log     = \
            '(fakepkg/a.py) '
            'fakepkg.a:17 -> fakepkg.__init__:10 -> fakepkg.a:17 '
            '-> ...',
    ),
    PicDetectNotification(
        type    = 'error',
        path    = Path('fakepkg/__init__.py'),
        log     = \
            '(fakepkg/__init__.py) '
            'fakepkg.__init__:10 -> fakepkg.a:17 -> fakepkg.__init__:10 -> '
            'fakepkg.a:17 -> ...',
    ),
    PicDetectNotification(
        type    = 'error',
        path    = Path('fakepkg/test/__init__.py'),
        log     = \
            '(fakepkg/test/__init__.py) fakepkg.test.__init__:8 -> '
            'fakepkg.a:17 -> fakepkg.__init__:10 -> fakepkg.a:17 -> ...',
    ),
]

#---
# Public
#---

def test_detec_circular() -> None:
    """ check circular dependencies
    """
    scaninfo = pic_scan_package(_PREFIX_PKG)
    detectinfo = pic_detect_circular_import(scaninfo)
    print('-== check each notification ==-')
    for notif in detectinfo:
        print(notif.debug_show())
    for notif in _SCANINFO:
        print(f"looking for ==> {notif.debug_show()}")
        assert notif in detectinfo
        detectinfo.remove(notif)
    print("-== check remaining notifications ==-")
    assert len(detectinfo) == 0
