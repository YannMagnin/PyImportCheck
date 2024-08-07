"""
tests.test_scan_modules     - check imports analysis
"""
from typing import Any
from pathlib import Path

from pyimportcheck.core.scan._imports import pic_scan_imports
from pyimportcheck.core.scan.types import (
    PicScannedFile,
    PicScannedImport,
    PicScannedSymbol,
    PicScannedImportType,
    PicScannedSymbolType,
)

#---
# Internals
#---

def __check_import(
    file_info: PicScannedFile,
    assert_table: Any,
) -> None:
    """ check scanned import
    """
    assert len(file_info.imports) == len(assert_table)
    for i, assert_check in enumerate(assert_table):
        print(file_info.imports[i])
        refimp = PicScannedImport(
            lineno      = assert_check['lineno'],
            import_path = assert_check['path'],
            type    = getattr(
                PicScannedImportType,
                assert_check['type'].upper(),
            ),
        )
        print(refimp)
        assert file_info.imports[i] == refimp

def __check_symbols(
    file_info: PicScannedFile,
    assert_table: Any,
) -> None:
    """ check scanned content
    """
    print(file_info.symbols)
    assert len(file_info.symbols) == len(assert_table)
    for assert_check in assert_table:
        print(file_info.symbols[assert_check['name']])
        assert assert_check['name'] in file_info.symbols
        refimp = PicScannedSymbol(
            lineno  = assert_check['lineno'],
            name    = assert_check['name'],
            type    = getattr(
                PicScannedSymbolType,
                assert_check['type'].upper(),
            ),
        )
        print(refimp)
        assert file_info.symbols[assert_check['name']] == refimp

#---
# Public
#---

def test_scan_import_raw() -> None:
    """ check raw import
    """
    assert_table_imp = (
        {'lineno': 1,  'path': 'test.aaa',            'type': 'raw'},
        {'lineno': 2,  'path': 'test',                'type': 'raw'},
        {'lineno': 4,  'path': 'test.ekip.afon',      'type': 'raw'},
        {'lineno': 7,  'path': 'test.abcd',           'type': 'raw'},
        {'lineno': 10, 'path': 'test.lvl0.lvl1.lvl2', 'type': 'raw'},
    )
    file_info = PicScannedFile(
        path    = Path('aaaa'),
        symbols = {},
        exports = [],
        imports = [],
    )
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
    __check_import(file_info, assert_table_imp)

def test_scan_import_inline() -> None:
    """ check inlined import
    """
    assert_table_imp = (
        {'lineno': 1,  'path': 'test',                'type': 'from_inline'},
        {'lineno': 2,  'path': 'test.ekip',           'type': 'from_inline'},
        {'lineno': 4,  'path': 'test.check0',         'type': 'from_inline'},
        {'lineno': 5,  'path': 'test.check1',         'type': 'from_inline'},
        {'lineno': 6,  'path': 'test.check2',         'type': 'from_inline'},
        {'lineno': 8,  'path': 'test.check3',         'type': 'from_inline'},
        {'lineno': 9,  'path': 'test.lvl0.lvl1.lvl2', 'type': 'from_inline'},
        {'lineno': 10, 'path': 'test.check4',         'type': 'from_inline'},
    )
    assert_table_sym = (
        {'lineno': 1, 'name': 'sym_0', 'type': 'import'},
        {'lineno': 2, 'name': 'sym_1', 'type': 'import'},
        {'lineno': 4, 'name': 'sym_2', 'type': 'import'},
        {'lineno': 4, 'name': 'sym_3', 'type': 'import'},
        {'lineno': 5, 'name': 'sym_4', 'type': 'import'},
        {'lineno': 5, 'name': 'sym_5', 'type': 'import'},
        {'lineno': 6, 'name': 'sym_6', 'type': 'import'},
        {'lineno': 6, 'name': 'sym_7', 'type': 'import'},
        {'lineno': 6, 'name': 'sym_8', 'type': 'import'},
        {'lineno': 8, 'name': 'sym_9', 'type': 'import'},
        {'lineno': 8, 'name': 'sym_A', 'type': 'import'},
        {'lineno': 8, 'name': 'sym_B', 'type': 'import'},
        {'lineno': 9, 'name': 'a',     'type': 'import'},
        {'lineno': 9, 'name': 'b',     'type': 'import'},
        {'lineno': 9, 'name': 'c',     'type': 'import'},
        {'lineno': 9, 'name': 'd',     'type': 'import'},
    )
    file_info = PicScannedFile(
        path    = Path('aaaa'),
        symbols = {},
        exports = [],
        imports = [],
    )
    pic_scan_imports(
        file_info   = file_info,
        package     = 'test',
        stream      = \
            'from test import sym_0\n'
            'from test.ekip import sym_1\n'
            '\n'
            'from test.check0 import sym_2,sym_3\n'
            'from test.check1 import sym_4, sym_5\n'
            'from test.check2 import sym_6, sym_7,sym_8\n'
            '\n'
            'from test.check3 import sym_9,sym_A,sym_B  # strastrs\n'
            'from test.lvl0.lvl1.lvl2 import a,b,c,d\n'
            'from test.check4 import *'
    )
    __check_import(file_info, assert_table_imp)
    __check_symbols(file_info, assert_table_sym)

def test_scan_import_multiline() -> None:
    """ check multilined import
    """
    assert_table_imp = (
        {'lineno': 1,   'path': 'test',                 'type': 'from'},
        {'lineno': 2,   'path': 'test.ekip',            'type': 'from'},
        {'lineno': 4,   'path': 'test.check0',          'type': 'from'},
        {'lineno': 5,   'path': 'test.check1',          'type': 'from'},
        {'lineno': 6,   'path': 'test.check2',          'type': 'from'},
        {'lineno': 8,   'path': 'test.check3',          'type': 'from'},
        {'lineno': 9,   'path': 'test.lvl0.lvl1.lvl2',  'type': 'from'},
        {'lineno': 11,  'path': 'test.abcd',            'type': 'from'},
    )
    assert_table_sym = (
        {'lineno': 1,  'name': 'sym_0', 'type': 'import'},
        {'lineno': 2,  'name': 'sym_1', 'type': 'import'},
        {'lineno': 4,  'name': 'sym_2', 'type': 'import'},
        {'lineno': 4,  'name': 'sym_3', 'type': 'import'},
        {'lineno': 5,  'name': 'sym_4', 'type': 'import'},
        {'lineno': 5,  'name': 'sym_5', 'type': 'import'},
        {'lineno': 6,  'name': 'sym_6', 'type': 'import'},
        {'lineno': 6,  'name': 'sym_7', 'type': 'import'},
        {'lineno': 6,  'name': 'sym_8', 'type': 'import'},
        {'lineno': 8,  'name': 'sym_9', 'type': 'import'},
        {'lineno': 8,  'name': 'sym_A', 'type': 'import'},
        {'lineno': 8,  'name': 'sym_B', 'type': 'import'},
        {'lineno': 9,  'name': 'a',     'type': 'import'},
        {'lineno': 9,  'name': 'b',     'type': 'import'},
        {'lineno': 9,  'name': 'c',     'type': 'import'},
        {'lineno': 9,  'name': 'd',     'type': 'import'},
        {'lineno': 12, 'name': 'sym_E', 'type': 'import'},
        {'lineno': 13, 'name': 'sym_K', 'type': 'import'},
        {'lineno': 14, 'name': 'sym_I', 'type': 'import'},
        {'lineno': 16, 'name': 'sym_P', 'type': 'import'},
        {'lineno': 16, 'name': 'sym_S', 'type': 'import'},
    )
    file_info = PicScannedFile(
        path    = Path('aaaa'),
        symbols = {},
        exports = [],
        imports = [],
    )
    pic_scan_imports(
        file_info   = file_info,
        package     = 'test',
        stream      = \
            'from test import (sym_0)\n'
            'from test.ekip import (sym_1)\n'
            '\n'
            'from test.check0 import (sym_2,sym_3)\n'
            'from test.check1 import (sym_4, sym_5)\n'
            'from test.check2 import (sym_6, sym_7,sym_8)\n'
            '\n'
            'from test.check3 import (sym_9,sym_A,sym_B)  # strastrs\n'
            'from test.lvl0.lvl1.lvl2 import (a,b,c,d)\n'
            '\n'
            'from test.abcd import (\n'
            '    sym_E,\n'
            '    sym_K,  # test aaaa\n'
            '    sym_I\n'
            '    \n'
            '    sym_P,sym_S    # aa bbbbbb\n'
            ')'
    )
    __check_import(file_info, assert_table_imp)
    __check_symbols(file_info, assert_table_sym)
