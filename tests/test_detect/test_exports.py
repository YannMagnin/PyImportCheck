"""
tests.test_detect.test_export   - test `__all__` behaviours
"""
from pathlib import Path

from pyimportcheck.core.scan import pic_scan_package
from pyimportcheck.core.detect._exports import pic_detect_exports_mistake
from pyimportcheck.core.detect import PicDetectNotification

#---
# Internals
#---

_PREFIX_PKG = Path(f"{__file__}/../../_data/missing_export").resolve()
_EXPORT_INFO = [
    PicDetectNotification(
        type    = 'error',
        path    = _PREFIX_PKG/'b.py',
        log     = f"{_PREFIX_PKG}/b.py: missing exported symbol 'b_func1'",
    ),
    PicDetectNotification(
        type    = 'warning',
        path    = _PREFIX_PKG/'a.py',
        log     = \
            f"{_PREFIX_PKG}/a.py: missing `__all__` "
            'symbol, which can be declared as follow:\n'
            '>>> __all__ = [\n'
            '>>>     \'a_func0\',\n'
            '>>>     \'a_func1\',\n'
            '>>>     \'A_GLOB0\',\n'
            '>>> ]',
    ),
    PicDetectNotification(
        type    = 'warning',
        path    = _PREFIX_PKG/'c.py',
        log     = \
            f"{_PREFIX_PKG}/c.py:7: symbol 'c_func0' has "
            'already been exported, you can remove this line',
    ),
    PicDetectNotification(
        type    = 'warning',
        path    = _PREFIX_PKG/'c.py',
        log     = \
            f"{_PREFIX_PKG}/c.py:8: symbol 'c_func1' has "
            'already been exported, you can remove this line',
    ),
]

#---
# Public
#---

def test_missing() -> None:
    """ test missing `__all__` declaration
    """
    scaninfo = pic_scan_package(_PREFIX_PKG)
    detectinfo = pic_detect_exports_mistake(scaninfo)
    print(detectinfo)
    expect_list = _EXPORT_INFO.copy()
    for check in _EXPORT_INFO:
        print(check)
        assert check in detectinfo
        expect_list.remove(check)
    print(expect_list)
    assert len(expect_list) == 0
