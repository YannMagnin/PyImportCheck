"""
pyimportcheck.core.scan._symbols    - analyse symbols declaration
"""
__all__ = [
    # function
    'pic_scan_symbol',
    'pic_scan_symbol_add',
    # data information
    'PicSymbol',
    'PIC_SYMBOL_TYPE_IMPORT',
    'PIC_SYMBOL_TYPE_FUNC',
    'PIC_SYMBOL_TYPE_VAR',
]
from typing import Dict, Any
from dataclasses import dataclass
import re

from pyimportcheck.core._logger import log_error

#---
# Internals
#---

def _pic_scan_symbol_var(file_info: Dict[str,Any], stream: Any) -> None:
    """ analyse function symbol
    """
    matcher = re.compile(
        flags   = re.MULTILINE,
        pattern = r"^(?P<var>([a-zA-Z0-9_]+( )?=( )?)+)",
    )
    for sym_record in matcher.finditer(stream):
        lineno = stream[:sym_record.start()].count('\n')
        for sym in sym_record['var'].split('='):
            if not (sym := sym.strip()):
                continue
            pic_scan_symbol_add(
                file_info   = file_info,
                lineno      = lineno,
                symname     = sym,
                symtype     = PIC_SYMBOL_TYPE_FUNC,
            )

def _pic_scan_symbol_func(file_info: Dict[str,Any], stream: Any) -> None:
    """ analyse function symbol
    """
    matcher = re.compile(
        flags   = re.MULTILINE,
        pattern = r"^def (?P<symbol>([1-9a-zA-Z_]+))\(",
    )
    for sym in matcher.finditer(stream):
        pic_scan_symbol_add(
            file_info   = file_info,
            lineno      = stream[:sym.start()].count('\n'),
            symname     = sym['symbol'],
            symtype     = PIC_SYMBOL_TYPE_FUNC,
        )

#---
# Public
#---

## classes and constants

PIC_SYMBOL_TYPE_IMPORT  = 'import'
PIC_SYMBOL_TYPE_FUNC    = 'function'
PIC_SYMBOL_TYPE_VAR     = 'var'

@dataclass
class PicSymbol():
    """ symbol information """
    lineno: int
    name:   str
    type:   str

## function

def pic_scan_symbol(
    file_info:  Dict[str,Any],
    stream: Any,
) -> None:
    """ analyse symbol declaration
    """
    file_info['symbols'] = {}
    _pic_scan_symbol_func(file_info, stream)
    _pic_scan_symbol_var(file_info, stream)

def pic_scan_symbol_add(
    file_info:  Dict[str,Any],
    lineno:     int,
    symname:    str,
    symtype:    str,
) -> None:
    """ add a symbol information into the internal dictionary
    """
    if 'symbols' not in file_info:
        file_info['symbols'] = {}
    if symname in file_info['symbols']:
        log_error(
            f"{file_info['path']}:{lineno}: symbol '{symname}' already "
            'exists,  the symbol will be ignored'
        )
        return
    file_info['symbols'][symname] = PicSymbol(
        lineno  = lineno,
        name    = symname,
        type    = symtype,
    )
