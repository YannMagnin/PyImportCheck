"""
pyimportcheck.core.scan._imports    - analyse import statement
"""
__all__ = [
    # function
    'pic_scan_imports',
    # data information
    'PicImport',
    'PIC_IMPORT_TYPE_RAW',
    'PIC_IMPORT_TYPE_FROM',
    'PIC_IMPORT_TYPE_FROM_INLINE',
]
from typing import Dict, Any
from dataclasses import dataclass
import re

from pyimportcheck.core._logger import log_warning
from pyimportcheck.core.scan._symbols import (
    pic_scan_symbol_add,
    PIC_SYMBOL_TYPE_IMPORT,
)

#---
# Internals
#---

def _pic_scan_check_from_multiline(
    file_info: Dict[str,Any],
    package: str,
    stream: Any,
) -> None:
    """ check multilined `from` import

    @notes
    - check only `from <package> import (<symbols>, ...)`
    - register import information
    - register implicit symbols information
    """
    matcher = re.compile(
        flags   = re.MULTILINE,
        pattern = \
            rf"^from (?P<path>{package}(\.[a-zA-Z0-9_]+)*) import "
            '\\(( )*(#.*(?=\n))?(\n)?'
            '(?P<sym>(( )*[a-zA-Z0-9_]+(,)?( )*(#.*(?=\n))?(\n)?)+)'
            '\\)',
    )
    for imp in matcher.finditer(stream):
        lineno = stream[:imp.start()].count('\n')
        file_info['imports'].append(
            PicImport(
                lineno  = lineno,
                path    = imp['path'],
                type    = PIC_IMPORT_TYPE_FROM,
            )
        )
        for symbol in imp['sym'].split('\n'):
            symbol = symbol.split('#')[0].strip()
            for sym in symbol.split(','):
                sym = sym.strip()
                if not sym:
                    continue
                pic_scan_symbol_add(
                    file_info   = file_info,
                    lineno      = lineno,
                    symname     = sym,
                    symtype     = PIC_SYMBOL_TYPE_IMPORT,
                )

def _pic_scan_check_from_inline(
    file_info: Dict[str,Any],
    package: str,
    stream: Any,
) -> None:
    """ check inlined `from` import

    @notes
    - check only `from <package> import <symbols>`
    - register import information
    - register implicit symbols information
    """
    matcher = re.compile(
        flags   = re.MULTILINE,
        pattern = \
            rf"^from (?P<path>{package}(\.[a-zA-Z0-9_]+)*) import "
            '(?P<sym>[a-zA-Z0-9_]+(,( )*[a-zA-Z0-9_]+( )*)*)'
            '([ \t]*(#.*))?$',
    )
    for imp in matcher.finditer(stream):
        lineno = stream[:imp.start()].count('\n')
        file_info['imports'].append(
            PicImport(
                lineno  = lineno,
                path    = imp['path'],
                type    = PIC_IMPORT_TYPE_FROM_INLINE,
            )
        )
        for symbol in imp['sym'].split(','):
            pic_scan_symbol_add(
                file_info   = file_info,
                lineno      = lineno,
                symname     = symbol.strip(),
                symtype     = PIC_SYMBOL_TYPE_IMPORT,
            )

def _pic_scan_check_raw(
    file_info: Dict[str,Any],
    package: str,
    stream: Any,
) -> None:
    """ check raw import statement

    @notes
    - check only `import <package statement>`
    - register import information
    - display warning
    """
    matcher = re.compile(
        flags   = re.MULTILINE,
        pattern = \
            rf"^import (?P<path>{package}(\.[a-z_0-9]+)*)"
            '([ \t]*(#.*))?$',
    )
    for imp in matcher.finditer(stream):
        print(imp)
        log_warning(
            f"{file_info['path']}:{imp.start()}: avoid using raw "
            '`import`, prefer using `from ... import ...` instead'
        )
        file_info['imports'].append(
            PicImport(
                lineno  = stream[:imp.start()].count('\n'),
                path    = imp['path'],
                type    = PIC_IMPORT_TYPE_RAW,
            )
        )

#---
# Public
#---

## classes and constants

PIC_IMPORT_TYPE_RAW = 'raw'
PIC_IMPORT_TYPE_FROM = 'from'
PIC_IMPORT_TYPE_FROM_INLINE = 'from-inline'

@dataclass
class PicImport():
    """ import information """
    lineno: int
    path:   str
    type:   str

## functions

def pic_scan_imports(
    file_info: Dict[str,Any],
    package: str,
    stream: Any,
) -> None:
    """ analyse import statements

    @notes
    - check for raw import (`import <package>`)
    - analyse fragmented import (`from <package> import ...`)
    """
    file_info['imports'] = []
    _pic_scan_check_raw(file_info, package, stream)
    _pic_scan_check_from_inline(file_info, package, stream)
    _pic_scan_check_from_multiline(file_info, package, stream)
