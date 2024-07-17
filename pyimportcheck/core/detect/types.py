"""
pyimportcheck.core.detect.types - all exposed types unsed by the detector
"""
__all__ = [
    'PicDetectReport',
    'PicDetectNotification',
]
from typing import List, Dict
from dataclasses import dataclass

#---
# Public
#---

@dataclass
class PicDetectNotification():
    """ warning / error information """
    type:   str
    log:    str

@dataclass
class PicDetectReport():
    """ repport of all detected information """
    notifications:   Dict[str,List[PicDetectNotification]]

    def __count_notification_type(self, notif_type: str) -> int:
        """ count the number of `notif_type` type
        """
        counter = 0
        for notifs in self.notifications.values():
            counter += sum(x.type == notif_type for x in notifs)
        return counter

    @property
    def error(self) -> int:
        """ return the number of error in the notification list """
        return self.__count_notification_type('error')

    @property
    def warning(self) -> int:
        """ return the number of error in the notification list """
        return self.__count_notification_type('warning')
