"""
pyimportcheck.core.detect._exports  - check missing / bad `__all__` symbol
"""
__all__ = [
    'pic_detect_exports_mistake',
]

from pyimportcheck.core._logger import log_warning
from pyimportcheck.core.scan import (
    PicScannedModule,
    PicScannedFile,
)

#---
# Internals
#---

def _pic_check_export_validity(info: PicScannedFile) -> int:
    """ check `__all__` declaration

    @notes
    - check that the `__all__` exist
    - check that exported symbols exists
    - check if internal symbols is exported (only if its a public file)
    """
    if '__all__' not in info.symbols:
        if not info.symbols:
            return 0
        log_warning(
            f"{info.path}: missing `__all__` symbol, which can be declared "
            'as follow:'
        )
        log_warning('>>> __all__ = [')
        for sym in info.symbols.keys():
            if not sym.startswith('_'):
                log_warning(f">>>     '{sym}',")
        log_warning('>>> ]')
        return 1
    return 0

def _pic_check_export_walk(
    root:    PicScannedModule,
    current: PicScannedModule,
) -> int:
    """ walk through scanned information and performs various check
    """
    error_counter = 0
    for _, module_info in current.modules.items():
        if isinstance(module_info, PicScannedModule):
            error_counter += _pic_check_export_walk(
                root    = root,
                current = module_info,
            )
            continue
        error_counter += _pic_check_export_validity(module_info)
    return error_counter

#---
# Public
#---

def  pic_detect_exports_mistake(info: PicScannedModule) -> int:
    """ check missing / bad `__all__` declaration
    """
    return _pic_check_export_walk(
        root    = info,
        current = info,
    )
