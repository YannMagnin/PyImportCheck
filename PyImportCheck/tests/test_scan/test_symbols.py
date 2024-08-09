"""
tests.test_scan_symbols     - check symbols analysis
"""
from typing import Any
from pathlib import Path

from pyimportcheck.core.scan._symbols import pic_scan_symbols
from pyimportcheck.core.scan.types import (
    PicScannedSymbol,
    PicScannedFile,
    PicScannedSymbolType,
)


#---
# Internals
#---

def __check_request(
    file_info: PicScannedFile,
    assert_table: Any,
) -> None:
    """ check scanned content
    """
    assert len(file_info.symbols) == len(assert_table)
    for assert_check in assert_table:
        assert assert_check['name'] in file_info.symbols
        print(file_info.symbols[assert_check['name']])
        refimp = PicScannedSymbol(
            lineno  = assert_check['lineno'],
            name    = assert_check['name'],
            type    = getattr(
                PicScannedSymbolType,
                assert_check['type'].upper(),
            )
        )
        print(refimp)
        assert file_info.symbols[assert_check['name']] == refimp

#---
# Public
#---

def test_scan_symbols_var() -> None:
    """ check var symbols
    """
    assert_table = (
        {'lineno' : 1,  'name' : 'var0',  'type' : 'var'},
        {'lineno' : 2,  'name' : 'var1',  'type' : 'var'},
        {'lineno' : 3,  'name' : 'var2',  'type' : 'var'},
        {'lineno' : 4,  'name' : 'var3',  'type' : 'var'},
        {'lineno' : 10, 'name' : 'VAR_5', 'type' : 'var'},
        {'lineno' : 10, 'name' : 'VAR_5', 'type' : 'var'},
        {'lineno' : 10, 'name' : 'var6',  'type' : 'var'},
        {'lineno' : 10, 'name' : 'var7',  'type' : 'var'},
    )
    file_info = PicScannedFile(
        path    = Path('aaaa'),
        relpath = Path('aaaa'),
        symbols = {},
        exports = [],
        imports = [],
    )
    pic_scan_symbols(
        file_info   = file_info,
        stream      = \
            'var0=0\n'
            'var1= 0\n'
            'var2 = 0\n'
            'var3       =           salut\n'
            '\n'
            '   var_4=0\n'
            'VAR_5 == nop\n'
            '#VAR_X = renop\n'
            '#import test.invalid\n'
            'VAR_5 = var6 = var7 = var8 = 667'
    )
    __check_request(file_info, assert_table)

def test_scan_symbols_func() -> None:
    """ check function symbols
    """
    assert_table = (
        {'lineno': 1, 'name': 'func_0', 'type': 'func'},
        {'lineno': 3, 'name': 'func_1', 'type': 'func'},
        {'lineno': 4, 'name': 'func_2', 'type': 'func'},
    )
    file_info = PicScannedFile(
        path    = Path('aaaa'),
        relpath = Path('aaaa'),
        symbols = {},
        exports = [],
        imports = [],
    )
    pic_scan_symbols(
        file_info   = file_info,
        stream      = \
            'def func_0(raaa, bbbb) -> None:\n'
            '\n'
            'def      func_1     (  raaa, bbbb  )\n'
            'def      func_2(  raaa, bbbb  )'
    )
    __check_request(file_info, assert_table)

def test_scan_symbols_class() -> None:
    """ check class symbols
    """
    assert_table = (
        {'lineno': 1, 'name': 'Cls_0', 'type': 'class'},
        {'lineno': 3, 'name': 'Cls_1', 'type': 'class'},
        {'lineno': 4, 'name': 'Cls_2', 'type': 'class'},
    )
    file_info = PicScannedFile(
        path    = Path('aaaa'),
        relpath = Path('aaaa'),
        symbols = {},
        exports = [],
        imports = [],
    )
    pic_scan_symbols(
        file_info   = file_info,
        stream      = \
            'class Cls_0(object):\n'
            '\n'
            'class      Cls_1     (  Test  )\n'
            'class      Cls_2(  raaa, bbbb  )'
    )
    __check_request(file_info, assert_table)
