"""
pyimportcheck.core.detect._circular - detect circular import
"""
__all__ = [
    'pic_detect_circular_import',
]
from typing import List, Union

from pyimportcheck.core.exception import PicException
from pyimportcheck.core.detect.types import PicDetectNotification
from pyimportcheck.core.scan import (
    PicScannedModule,
    PicScannedImport,
    PicScannedFile,
)

#---
# Internals
#---

#def _pic_generate_raise_log(
#    module_info:    PicScannedModule,
#    import_current: PicScannedImport,
#    log:            str,
#) -> PicException:
#    """ generate exception information
#    """
#    return PicException(
#        f"{module_info.path}:{import_current.lineno}: unable to import "
#        f"'{import_current.import_path}', {log}",
#    )
#
#def _pic_find_fileinfo(
#    root_module_info:       PicScannedModule,
#    current_import_info:    PicScannedImport,
#) -> PicScannedFile:
#    """ resolve manual import path
#
#    @notes
#    - if the last part of the `current_import_info.import_path` is a module
#        then it will automatically try to find the `__init__.py` file that
#        refer the module
#    """
#    target: Union[PicScannedModule,PicScannedFile] = root_module_info
#    for shard in current_import_info.import_path.split('.')[1:]:
#        if isinstance(target, PicScannedFile):
#            raise _pic_generate_raise_log(
#                module_info     = root_module_info,
#                import_current  = current_import_info,
#                log             = \
#                    f"because '{target.name}' is a file, or it should be "
#                    'a module',
#            )
#        if shard not in target.modules:
#            raise _pic_generate_raise_log(
#                module_info     = root_module_info,
#                import_current  = current_import_info,
#                log             = \
#                    f"unable to find the '{shard}' file information",
#            )
#        target = target.modules[shard]
#    if isinstance(target, PicScannedModule):
#        if '__init__' not in target.modules:
#            raise _pic_generate_raise_log(
#                module_info     = root_module_info,
#                import_current  = current_import_info,
#                log             = \
#                    'unable to find the \'__init__.py\' file information '
#                    'required to analyse the module (this mean that all '
#                    'files inside this module will be skipped)',
#            )
#        target = target.modules['__init__']
#    assert isinstance(target, PicScannedFile)
#    return target
#
#def _pic_search_circular_import(
#    root_module_info:    PicScannedModule,
#    current_import_info: PicScannedImport,
#    import_history_list: List[PicScannedImport],
#) -> Union[List[PicScannedImport],None]:
#    """ resolve a package and avoid circular import
#
#    @notes
#    - if a circular dependency has been detected the the import history
#        will be returned, otherwise an explicit `None` will be returned
#        instead
#    """
#    print(f"searching for '{current_import_info.import_path}'")
#    for import_info in import_history_list:
#        if import_info.name == current_import_info.name:
#            print(f"already matched -> {import_history_list}")
#            return import_history_list
#    target = _pic_find_fileinfo(root_module_info, current_import_info)
#    for next_import in target.imports:
#        valid = _pic_search_circular_import(
#            root_module_info    = root_module_info,
#            current_import_info = next_import,
#            import_history_list = import_history_list + [next_import],
#        )
#        if valid:
#            return valid
#    return None
#
#def _pic_check_circular(
#    root_module_info:    PicScannedModule,
#    current_file_info: PicScannedFile,
#    import_prefix:       str,
#) -> List[PicDetectNotification]:
#    """ check circular import
#    """
#    pathfile = current_file_info.path.resolve().relative_to(
#        (root_module_info.path/'..').resolve(),
#    )
#    notifications: List[PicDetectNotification] = []
#    for imp in current_file_info.imports:
#        try:
#            circular_list = _pic_search_circular_import(
#                root_module_info    = root_module_info,
#                current_import_info = imp,
#                import_history_list = [],
#            )
#        except PicException as err:
#            notifications.append(
#                PicDetectNotification(
#                    type    = 'error',
#                    path    = pathfile,
#                    log     = str(err),
#                ),
#            )
#            continue
#        if not circular_list:
#            continue
#        error = f"({str(pathfile)}) {import_prefix}:{imp.lineno} -> "
#        print(error)
#        for imp in circular_list:
#            #print(f"looking for -> {imp.import_path}")
#            #impinfo = _pic_find_fileinfo(root_module_info, imp)
#            import_path = imp.import_path
#            #print(f"fing -> '{impinfo.name}'")
#            #if impinfo.name == '__init__':
#            #    import_path = f"{import_path}.__init__"
#            #    print(f"modified path --> {import_path}")
#            error += f"{import_path}:{imp.lineno} -> "
#        error += '...'
#        notifications.append(
#            PicDetectNotification(
#                type    = 'error',
#                path    = pathfile,
#                log     = error,
#            ),
#        )
#    return notifications
#
#def _pic_check_import(
#    root_module_info: PicScannedModule,
#    current_module_info: PicScannedModule,
#    import_prefix: str,
#) -> List[PicDetectNotification]:
#    """ recursively resolve all dependencies
#    """
#    notifications: List[PicDetectNotification] = []
#    for module, module_info in current_module_info.modules.items():
#        if isinstance(module_info, PicScannedModule):
#            notifications += _pic_check_import(
#                root_module_info,
#                module_info,
#                f"{import_prefix}.{module}",
#            )
#            continue
#        notifications += _pic_check_circular(
#            root_module_info,
#            module_info,
#            f"{import_prefix}.{module}",
#        )
#    return notifications

#---
# Public
#---

def pic_detect_circular_import(
    root_module_info: PicScannedModule,
) -> List[PicDetectNotification]:
    """ try to detect circular import
    """
    print(root_module_info.debug_show())
    return []
#    return _pic_check_import(
#        root_module_info,
#        root_module_info,
#        root_module_info.name,
#    )
