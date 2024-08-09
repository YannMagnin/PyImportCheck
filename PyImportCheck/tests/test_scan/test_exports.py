"""
tests.test_scan_exports     - check exports analysis
"""
from typing import Any
from pathlib import Path

from pyimportcheck.core.scan._exports import pic_scan_exports
from pyimportcheck.core.scan.types import (
    PicScannedExport,
    PicScannedFile,
)

#---
# Public
#---

def test_scan_exports() -> None:
    """ check var symbols
    """
    assert_table: Any = (
        {'lineno': 1, 'name': 'aaa'},
        {'lineno': 1, 'name': 'bb_b'},
        {'lineno': 1, 'name': 'ccc'},
        {'lineno': 2, 'name': 'ekip'},
        {'lineno': 3, 'name': 'test'},
        {'lineno': 3, 'name': 'mix'},
        {'lineno': 6, 'name': 'mms'},
        {'lineno': 7, 'name': 'ldo'},
        {'lineno': 7, 'name': '667'},
        {'lineno': 8, 'name': 'gam3rz'},
        {'lineno': 10, 'name': 'comment'},
    )
    file_info = PicScannedFile(
        path    = Path('aaaa'),
        relpath = Path('aaaa'),
        symbols = {},
        exports = [],
        imports = [],
    )
    pic_scan_exports(
        file_info   = file_info,
        stream      = \
            "__all__ = ['aaa', 'bb_b', 'ccc']\n"
            "__all__ = ['ekip', ]\n"
            "__all__ = [\"test\", 'mix',]\n"
            "\n"
            "__all__ = [\n"
            "    'mms',\n"
            "    'ldo', '667',\n"
            "    'gam3rz'\n"
            "     \n"
            "     \"comment\"   #aaaaa\n"
            "]"
    )
    assert len(assert_table) == len(file_info.exports)
    for i, exp in enumerate(assert_table):
        print(file_info.exports[i])
        assert PicScannedExport(**exp) == file_info.exports[i]
