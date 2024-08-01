"""
tests.test_scan     - check scan analysis
"""
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
                    'a_test1' : \
                        PicScannedSymbol(
                            lineno  = 10,
                            name    = 'a_test1',
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
                    'a_test1': \
                        PicScannedSymbol(
                            lineno  = 20,
                            name    = 'a_test1',
                            type    = PicScannedSymbolType.FUNC,
                        ),
                    'a_test2': \
                        PicScannedSymbol(
                            lineno  = 25,
                            name    = 'a_test2',
                            type    = PicScannedSymbolType.FUNC,
                        ),
                },
                exports = [
                    PicScannedExport(5, 'a_test1'),
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
        },
    )
    print(fakepkg_path)
    outscan = pic_scan_package(fakepkg_path)
    for mod in ('__init__', '__main__', 'b', 'a'):
        print(f"check {mod}")
        print('-- module exists...')
        assert mod in outscan.modules
        for attr in ('path', 'symbols', 'exports', 'imports'):
            print(f"-- {attr}...")
            inp = getattr(outscan.modules[mod], attr)
            oup = getattr(assert_obj.modules[mod], attr)
            print(f"inp ==> {inp}")
            print(f"oup ==> {oup}")
            assert inp == oup
        print('-- full...')
        assert outscan.modules[mod] == assert_obj.modules[mod]
        outscan.modules.pop(mod)
        print(' -== OK!')
    print('check all')
    print(f"outscan ==> {outscan.modules}")
    assert len(outscan.modules) == 0
