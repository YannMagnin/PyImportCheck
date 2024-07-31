"""
tests.test_detect.test_export   - test `__all__` behaviours
"""
from pathlib import Path

from pyimportcheck.core.scan import (
    pic_scan_package,
    PicScannedModule,
)
from pyimportcheck.core.detect._exports import pic_detect_exports_mistake

#---
# Internals
#---

_MISSING_ERROR_LOG = \
    '/home/reverse/github/PyImportCheck/tests/_data/missing_export/a.py: ' \
    'missing `__all__` symbol, which can be declared as follow:\n' \
    '>>> __all__ = [\n' \
    '>>>     \'a_func0\',\n' \
    '>>>     \'a_func1\',\n' \
    '>>>     \'A_GLOB0\',\n' \
    '>>> ]'

def __scan_fake_pkg() -> PicScannedModule:
    """ open a special fake package
    """
    return pic_scan_package(
        Path(f"{__file__}/../../_data/missing_export").resolve(),
    )

#---
# Public
#---

def test_missing() -> None:
    """ test missing `__all__` declaration
    """
    scaninfo = __scan_fake_pkg()
    detectinfo = pic_detect_exports_mistake(scaninfo)
    assert len(detectinfo) == 1
    assert detectinfo[0].type == 'warning'
    assert detectinfo[0].log == _MISSING_ERROR_LOG
