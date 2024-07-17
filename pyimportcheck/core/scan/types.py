"""
pyimportcheck.core.scan.types   - glossary of all scanner types
"""
# use this magical import to allow the use of partialed initialized classes
# needed by the `PicScannedModule` which can store other module information
from __future__ import annotations

__all__ = [
    'PicScannedFile',
    'PicScannedSymbol',
    'PicScannedImport',
    'PicScannedExport',
]
from typing import Dict, Union, List
from dataclasses import dataclass
from pathlib import Path

#---
# Public
#---

## constants

PIC_IMPORT_TYPE_RAW         = 'raw'
PIC_IMPORT_TYPE_FROM        = 'from'
PIC_IMPORT_TYPE_FROM_INLINE = 'from-inline'

PIC_SYMBOL_TYPE_IMPORT      = 'import'
PIC_SYMBOL_TYPE_FUNC        = 'function'
PIC_SYMBOL_TYPE_VAR         = 'var'

## dataclasses

@dataclass
class PicScannedSymbol():
    """ symbol information """
    lineno: int
    name:   str
    type:   str

@dataclass
class PicScannedImport():
    """ import information """
    lineno: int
    path:   str
    type:   str

    @property
    def name(self) -> str:
        """ shortcut to fetch the import name """
        return self.path.split('.')[-1]

@dataclass
class PicScannedExport():
    """ scanned export symbol information """
    lineno: int
    name:   str

@dataclass
class PicScannedFile():
    """ scanned python file information """
    path:       Path
    symbols:    Dict[str,PicScannedSymbol]
    exports:    List[PicScannedExport]
    imports:    List[PicScannedImport]

    @property
    def name(self) -> str:
        """ shortcut to fetch the import name """
        return self.path.stem

@dataclass
class PicScannedModule():
    """ scanned module information """
    name:       str
    path:       Path
    modules:    Dict[str,Union[PicScannedModule,PicScannedFile]]
