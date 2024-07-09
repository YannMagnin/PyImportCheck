"""
tests.test_scan_symbols     - check symbols analysis
"""
from typing import Dict, Any

from pyimportcheck.core.scan._symbols import (
    pic_scan_symbols,
    PicSymbol,
)

#---
# Internals
#---

def __check_request(
    file_info: Any,
    assert_table: Any,
) -> None:
    """ check scanned content
    """
    assert 'symbols' in file_info
    assert len(file_info['symbols']) == len(assert_table)
    for assert_check in assert_table:
        assert assert_check['name'] in file_info['symbols']
        print(file_info['symbols'][assert_check['name']])
        refimp = PicSymbol(**assert_check)
        assert file_info['symbols'][assert_check['name']] == refimp

#---
# Public
#---

def test_scan_symbols_var() -> None:
    """ check var symbols
    """
    assert_table = (
        {'lineno' : 0, 'name' : 'var0',  'type' : 'var'},
        {'lineno' : 1, 'name' : 'var1',  'type' : 'var'},
        {'lineno' : 2, 'name' : 'var2',  'type' : 'var'},
        {'lineno' : 3, 'name' : 'var3',  'type' : 'var'},
        {'lineno' : 9, 'name' : 'VAR_5', 'type' : 'var'},
        {'lineno' : 9, 'name' : 'VAR_5', 'type' : 'var'},
        {'lineno' : 9, 'name' : 'var6',  'type' : 'var'},
        {'lineno' : 9, 'name' : 'var7',  'type' : 'var'},
    )
    file_info: Dict[str,Any] = {'path': 'aaa'}
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
        {'lineno': 0, 'name': 'func_0', 'type': 'function'},
        {'lineno': 2, 'name': 'func_1', 'type': 'function'},
        {'lineno': 3, 'name': 'func_2', 'type': 'function'},
    )
    file_info = {'path': 'aaa'}
    pic_scan_symbols(
        file_info   = file_info,
        stream      = \
            'def func_0(raaa, bbbb) -> None:\n'
            '\n'
            'def      func_1     (  raaa, bbbb  )\n'
            'def      func_2(  raaa, bbbb  )'
    )
    __check_request(file_info, assert_table)
