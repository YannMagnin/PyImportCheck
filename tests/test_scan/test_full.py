"""
tests.test_scan     - check scan analysis
"""
from typing import cast, Iterable
from pathlib import Path

from pyimportcheck.core.scan import (
    pic_scan_package,
    PicScannedModule,
    PicScannedFile,
    PicScannedSymbol,
    PicScannedImport,
    PicScannedExport,
    PicScannedSymbolType,
    PicScannedImportType,
)

#---
# Internals
#---

def _test_scan_fileinfo(
    ref: PicScannedFile,
    scanned: PicScannedFile,
) -> None:
    """ check fileinfo
    """
    for attr in ('path', 'symbols', 'exports', 'imports'):
        print(f"-- {attr}...")
        inp = getattr(scanned, attr)
        oup = getattr(ref, attr)
        print(f"inp ==> {inp}")
        print(f"oup ==> {oup}")
        assert inp == oup
    print('-- full...')
    assert scanned == ref

def _test_scan_module(
    refscan:  PicScannedModule,
    outscan:  PicScannedModule,
    to_check: Iterable[str],
) -> None:
    """ check module information
    """
    for mod in to_check:
        print(f"-== check '{mod}' ==-")
        print('-- module exists...')
        assert mod in outscan.modules
        _test_scan_fileinfo(
            cast(PicScannedFile, refscan.modules[mod]),
            cast(PicScannedFile, outscan.modules[mod]),
        )
        outscan.modules.pop(mod)
        print(' -== OK!')

#---
# Public
#---

def test_scan_complet() -> None:
    """ full scan check
    """
    fakepkg_path = Path(f"{__file__}/../../_data/fakepkg").resolve()
    assert_obj = PicScannedModule(
        name    = 'fakepkg',
        path    = fakepkg_path,
        modules = {
            '__init__': PicScannedFile(
                path    = fakepkg_path/'__init__.py',
                symbols = {
                    '__all__' : \
                        PicScannedSymbol(
                            lineno  = 4,
                            name    = '__all__',
                            type    = PicScannedSymbolType.VAR,
                        ),
                    'ACls' : \
                        PicScannedSymbol(
                            lineno  = 10,
                            name    = 'ACls',
                            type    = PicScannedSymbolType.IMPORT,
                        ),
                    'b_test1' : \
                        PicScannedSymbol(
                            lineno  = 12,
                            name    = 'b_test1',
                            type    = PicScannedSymbolType.IMPORT,
                        ),
                    'b_test2' : \
                        PicScannedSymbol(
                            lineno  = 12,
                            name    = 'b_test2',
                            type    = PicScannedSymbolType.IMPORT,
                        ),
                },
                exports = [
                    PicScannedExport(5, 'b_test2'),
                    PicScannedExport(6, 'b_test1'),
                ],
                imports = [
                    PicScannedImport(
                        lineno      = 10,
                        import_path = 'fakepkg.a',
                        type        = PicScannedImportType.FROM_INLINE,
                    ),
                    PicScannedImport(
                        lineno      = 12,
                        import_path = 'fakepkg.b',
                        type        = PicScannedImportType.FROM_INLINE,
                    ),
                ],
            ),
            '__main__' : PicScannedFile(
                path    = fakepkg_path/'__main__.py',
                symbols = {},
                exports = [],
                imports = [],
            ),
            'a' : PicScannedFile(
                path    = fakepkg_path/'a.py',
                symbols = {
                    '__all__': \
                        PicScannedSymbol(
                            lineno  = 4,
                            name    = '__all__',
                            type    = PicScannedSymbolType.VAR,
                        ),
                    'ACls': \
                        PicScannedSymbol(
                            lineno  = 20,
                            name    = 'ACls',
                            type    = PicScannedSymbolType.CLASS,
                        ),
                    'a_test2': \
                        PicScannedSymbol(
                            lineno  = 25,
                            name    = 'a_test2',
                            type    = PicScannedSymbolType.FUNC,
                        ),
                },
                exports = [
                    PicScannedExport(5, 'ACls'),
                    PicScannedExport(6, 'a_test2'),
                ],
                imports = [
                    PicScannedImport(
                        lineno      = 17,
                        import_path = 'fakepkg',
                        type        = PicScannedImportType.RAW,
                    ),
                ],
            ),
            'b' : PicScannedFile(
                path    = fakepkg_path/'b.py',
                symbols = {
                    'b_test1': \
                        PicScannedSymbol(
                            lineno  = 8,
                            name    = 'b_test1',
                            type    = PicScannedSymbolType.FUNC,
                        ),
                    'b_test2': \
                        PicScannedSymbol(
                            lineno  = 12,
                            name    = 'b_test2',
                            type    = PicScannedSymbolType.FUNC,
                        ),
                },
                exports = [],
                imports = [],
            ),
            'test': PicScannedModule(
                name    = 'test',
                path    = fakepkg_path/ 'test',
                modules = {
                    '__init__': \
                        PicScannedFile(
                            path    = fakepkg_path/'test/__init__.py',
                            symbols = {
                                '__all__': \
                                    PicScannedSymbol(
                                        lineno  = 4,
                                        name    = '__all__',
                                        type    = PicScannedSymbolType.VAR,
                                    ),
                                'a_func0': \
                                    PicScannedSymbol(
                                        lineno  = 8,
                                        name    = 'a_func0',
                                        type    = \
                                            PicScannedSymbolType.IMPORT,
                                ),
                                'TEST0': \
                                    PicScannedSymbol(
                                        lineno  = 9,
                                        name    = 'TEST0',
                                        type    = \
                                            PicScannedSymbolType.VAR,
                                ),
                            },
                            exports = [
                                PicScannedExport(5, 'TEST0'),
                            ],
                            imports = [
                                PicScannedImport(
                                    lineno      = 8,
                                    import_path = 'fakepkg.a',
                                    type        = \
                                        PicScannedImportType.FROM_INLINE,
                                ),
                            ],
                        )
                    },
            ),
        },
    )
    print(fakepkg_path)
    outscan = pic_scan_package(fakepkg_path)
    print(f"TEST ====> {outscan}")
    _test_scan_module(
        assert_obj,
        outscan,
        ('__init__', '__main__', 'b', 'a'),
    )
    assert 'test' in outscan.modules
    assert isinstance(outscan.modules['test'], PicScannedModule)
    assert isinstance(assert_obj.modules['test'], PicScannedModule)
    _test_scan_module(
        assert_obj.modules['test'],
        outscan.modules['test'],
        ('__init__', ),
    )
    outscan.modules.pop('test')
    print('-=== final check ===-')
    print(f"outscan ==> {outscan.modules}")
    assert len(outscan.modules) == 0
