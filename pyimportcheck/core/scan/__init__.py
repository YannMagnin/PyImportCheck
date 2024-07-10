"""
pyimportcheck.core.scan   - python package scanner
"""
__all__ = [
    'pic_scan_package',
    'PicScannedFile',
    'PicScannedSymbol',
    'PicScannedImport',
    'PicScannedExport',
    'PicScannedModule',
]
from dataclasses import dataclass
from pathlib import Path
import re
import mmap

from pyimportcheck.core.exception import PycycleException
from pyimportcheck.core._logger import (
    log_warning,
    log_error,
)
from pyimportcheck.core.scan._imports import pic_scan_imports
from pyimportcheck.core.scan._exports import pic_scan_exports
from pyimportcheck.core.scan._symbols import pic_scan_symbols
from pyimportcheck.core.scan.types import (
    PicScannedModule,
    PicScannedFile,
    PicScannedSymbol,
    PicScannedExport,
    PicScannedImport,
)

#---
# Internals
#---

def _pic_analyse_file(
    filepath:   Path,
    package:    str
) -> PicScannedFile:
    """ load the file and manually parse import
    """
    fileinfo = PicScannedFile(
        path    = filepath,
        symbols = {},
        exports = [],
        imports = [],
    )
    with open(filepath, 'r', encoding='utf-8') as filestream:
        mfile = filestream.read()
        pic_scan_imports(fileinfo, mfile, package)
        pic_scan_symbols(fileinfo, mfile)
        pic_scan_exports(fileinfo, mfile)
    return fileinfo

def _pic_analyse_package(
    module:     PicScannedModule,
    package:    str,
) -> PicScannedModule:
    """ recursively scan package folders
    """
    for filepath in module.path.iterdir():
        if filepath.name in ['__pycache__', 'py.typed']:
            continue
        if filepath.name.startswith('.'):
            continue
        if filepath.is_dir():
            module.modules[filepath.name] = _pic_analyse_package(
                PicScannedModule(
                    name    = filepath.name,
                    path    = filepath,
                    modules = {},
                ),
                package,
            )
            continue
        if not filepath.name.endswith('.py'):
            log_warning(f"file '{str(filepath)}' is not a valid")
            continue
        module.modules[filepath.stem] = _pic_analyse_file(
            filepath    = filepath,
            package     = package,
        )
    return module

#---
# Public
#---

def pic_scan_package(prefix: Path) -> PicScannedModule:
    """ package scanner
    """
    return _pic_analyse_package(
        PicScannedModule(
            name    = prefix.name,
            path    = prefix,
            modules = {}
        ),
        prefix.name,
    )
