"""
tests.test_scan_exports     - check exports analysis
"""
from typing import Any

from pyimportcheck.core.scan._exports import pic_scan_exports

#---
# Public
#---

def test_scan_exports() -> None:
    """ check var symbols
    """
    assert_table = (
        (0, 'aaa'),
        (0, 'bb_b'),
        (0, 'ccc'),
        (1, 'ekip'),
        (2, 'test'),
        (2, 'mix'),
        (5, 'mms'),
        (6, 'ldo'),
        (6, '667'),
        (7, 'gam3rz'),
        (9, 'comment'),
    )
    file_info: Any = {'path': 'aaa'}
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
    assert 'exports' in file_info
    assert len(assert_table) == len(file_info['exports'])
    for i, exp in enumerate(assert_table):
        print(file_info['exports'][i])
        assert exp == file_info['exports'][i]
