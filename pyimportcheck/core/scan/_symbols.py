"""
pyimportcheck.core.scan._symbols    - analyse symbols declaration
"""
__all__ = [
    'pic_scan_symbols',
    'pic_scan_symbol_add',
]
from typing import Any
import re

from pyimportcheck.core._logger import log_error
from pyimportcheck.core.scan.types import (
    PicScannedFile,
    PicScannedSymbol,
    PIC_SYMBOL_TYPE_VAR,
    PIC_SYMBOL_TYPE_FUNC,
)

#---
# Internals
#---

def _pic_scan_symbol_var(file_info: PicScannedFile, stream: Any) -> None:
    """ analyse function symbol
    """
    matcher = re.compile(
        flags   = re.MULTILINE,
        pattern = r"^(?P<var>([a-zA-Z0-9_]+( )*=(?!=)( )*)+)",
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
                symtype     = PIC_SYMBOL_TYPE_VAR,
            )

def _pic_scan_symbol_func(file_info: PicScannedFile, stream: Any) -> None:
    """ analyse function symbol
    """
    matcher = re.compile(
        flags   = re.MULTILINE,
        pattern = r"^def( )+(?P<symbol>([a-zA-Z0-9_]+))( )*\(",
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

def pic_scan_symbols(
    file_info:  PicScannedFile,
    stream: Any,
) -> None:
    """ analyse symbol declaration
    """
    _pic_scan_symbol_func(file_info, stream)
    _pic_scan_symbol_var(file_info, stream)

def pic_scan_symbol_add(
    file_info:  PicScannedFile,
    lineno:     int,
    symname:    str,
    symtype:    str,
) -> None:
    """ add a symbol information into the internal dictionary
    """
    if symname in file_info.symbols:
        log_error(
            f"{file_info.path}:{lineno + 1}: symbol '{symname}' already "
            'exists,  the symbol will be ignored'
        )
        return
    file_info.symbols[symname] = PicScannedSymbol(
        lineno  = lineno + 1,
        name    = symname,
        type    = symtype,
    )
