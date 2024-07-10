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
)

#---
# Public
#---

def test_scan_complet() -> None:
    """ full scan check
    """
    fakepkg_path = Path(f"{__file__}/../_data/fakepkg").resolve()
    assert_obj = PicScannedModule(
        name    = 'fakepkg',
        path    = fakepkg_path,
        modules = {
            '__init__': PicScannedFile(
                path    = fakepkg_path/'__init__.py',
                symbols = {
                    '__all__' : PicScannedSymbol(4,  '__all__', 'var'),
                    'a_test1' : PicScannedSymbol(10, 'a_test1', 'import'),
                    'b_test1' : PicScannedSymbol(12, 'b_test1', 'import'),
                    'b_test2' : PicScannedSymbol(12, 'b_test2', 'import'),
                },
                exports = [
                    PicScannedExport(5, 'b_test2'),
                    PicScannedExport(6, 'b_test1'),
                ],
                imports = [
                    PicScannedImport(10, 'fakepkg.a', 'from-inline'),
                    PicScannedImport(12, 'fakepkg.b', 'from-inline'),
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
                    '__all__': PicScannedSymbol(4,  '__all__', 'var'),
                    'a_test1': PicScannedSymbol(20, 'a_test1', 'function'),
                    'a_test2': PicScannedSymbol(25, 'a_test2', 'function'),
                },
                exports = [
                    PicScannedExport(5, 'a_test1'),
                    PicScannedExport(6, 'a_test2'),
                ],
                imports = [
                    PicScannedImport(17, 'fakepkg', 'raw'),
                ],
            ),
            'b' : PicScannedFile(
                path    = fakepkg_path/'b.py',
                symbols = {
                    'b_test1': PicScannedSymbol(8,  'b_test1', 'function'),
                    'b_test2': PicScannedSymbol(12, 'b_test2', 'function'),
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
            print(inp)
            print(oup)
            assert inp == oup
        print('-- full...')
        assert outscan.modules[mod] == assert_obj.modules[mod]
        print(' -== OK!')
    print('check all')
    print(outscan)
    assert outscan == assert_obj
