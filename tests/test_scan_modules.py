"""
tests.test_scan_modules     - check imports analysis
"""
__all__ = [
    'test_scan_import_raw',
]
from typing import Dict, Any

from pyimportcheck.core.scan._imports import (
    pic_scan_imports,
    PicImport,
)

def test_scan_import_raw() -> None:
    """ check raw import
    """
    assert_table = (
        {'lineno' : 0, 'path' : 'test.aaa',            'type' : 'raw'},
        {'lineno' : 1, 'path' : 'test',                'type' : 'raw'},
        {'lineno' : 3, 'path' : 'test.ekip.afon',      'type' : 'raw'},
        {'lineno' : 6, 'path' : 'test.abcd',           'type' : 'raw'},
        {'lineno' : 9, 'path' : 'test.lvl0.lvl1.lvl2', 'type' : 'raw'},
    )
    file_info: Dict[str,Any] = {'path': 'aaa'}
    pic_scan_imports(
        file_info   = file_info,
        package     = 'test',
        stream      = \
            'import test.aaa\n'
            'import test\n'
            '\n'
            'import test.ekip.afon\n'
            '  import aaaa\n'
            '\n'
            'import test.abcd   # aaassss\n'
            '#import test.invalid\n'
            '\n'
            'import test.lvl0.lvl1.lvl2'
    )
    assert 'imports' in file_info
    assert len(file_info['imports']) == len(assert_table)
    for i, assert_check in enumerate(assert_table):
        print(file_info['imports'][i])
        refimp = PicImport(**assert_check) # type: ignore
        assert file_info['imports'][i] == refimp

def test_scan_import_inline() -> None:
    """ check inlined import
    """
    assert_table = (
        {'lineno': 0, 'path': 'test',               'type': 'from-inline'},
        {'lineno': 1, 'path': 'test.ekip',          'type': 'from-inline'},
        {'lineno': 3, 'path': 'test.check0',        'type': 'from-inline'},
        {'lineno': 4, 'path': 'test.check1',        'type': 'from-inline'},
        {'lineno': 5, 'path': 'test.check2',        'type': 'from-inline'},
        {'lineno': 7, 'path': 'test.check3',        'type': 'from-inline'},
        {'lineno': 8, 'path': 'test.lvl0.lvl1.lvl2','type': 'from-inline'},
    )
    file_info: Dict[str,Any] = {'path' : 'aaa'}
    pic_scan_imports(
        file_info   = file_info,
        package     = 'test',
        stream      = \
            'from test import sym_0\n'
            'from test.ekip import sym_9\n'
            '\n'
            'from test.check0 import sym0,sym1\n'
            'from test.check1 import sym0, sym1\n'
            'from test.check2 import sym0, sym1,sym2\n'
            '\n'
            'from test.check3 import sym0,sym1,sym2  # strastrs\n'
            'from test.lvl0.lvl1.lvl2 import a,b,c,d'
    )
    assert 'imports' in file_info
    assert len(file_info['imports']) == len(assert_table)
    for i, assert_check in enumerate(assert_table):
        print(file_info['imports'][i])
        refimp = PicImport(**assert_check) # type: ignore
        assert file_info['imports'][i] == refimp
    # (todo) : check symbols

def test_scan_import_multiline() -> None:
    """ check multilined import
    """
    assert_table = (
        {'lineno': 0,   'path': 'test',                 'type': 'from'},
        {'lineno': 1,   'path': 'test.ekip',            'type': 'from'},
        {'lineno': 3,   'path': 'test.check0',          'type': 'from'},
        {'lineno': 4,   'path': 'test.check1',          'type': 'from'},
        {'lineno': 5,   'path': 'test.check2',          'type': 'from'},
        {'lineno': 7,   'path': 'test.check3',          'type': 'from'},
        {'lineno': 8,   'path': 'test.lvl0.lvl1.lvl2',  'type': 'from'},
        {'lineno': 10,  'path': 'test.abcd',            'type': 'from'},
    )
    file_info: Dict[str,Any] = {'path' : 'aaa'}
    pic_scan_imports(
        file_info   = file_info,
        package     = 'test',
        stream      = \
            'from test import (sym_0)\n'
            'from test.ekip import (sym_9)\n'
            '\n'
            'from test.check0 import (sym0,sym1)\n'
            'from test.check1 import (sym0, sym1)\n'
            'from test.check2 import (sym0, sym1,sym2)\n'
            '\n'
            'from test.check3 import (sym0,sym1,sym2)  # strastrs\n'
            'from test.lvl0.lvl1.lvl2 import (a,b,c,d)\n'
            '\n'
            'from test.abcd import (\n'
            '    sym0,\n'
            '    sym1,  # test aaaa\n'
            '    sym2\n'
            '    sym3,sym4    # aa bbbbbb\n'
            ')'
    )
    assert 'imports' in file_info
    assert len(file_info['imports']) == len(assert_table)
    for i, assert_check in enumerate(assert_table):
        print(file_info['imports'][i])
        refimp = PicImport(**assert_check) # type: ignore
        assert file_info['imports'][i] == refimp
    # (todo) : check symbols
