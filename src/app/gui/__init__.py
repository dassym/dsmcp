import logging

from .base import BaseQtApp


try:
    from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
    #logging.debug('Module PyQt5 v{0!s} based on Qt5 v{1!s} is loaded.'.format(PYQT_VERSION_STR, QT_VERSION_STR))
except ModuleNotFoundError:
    logging.error("The pyqt5 module isn't installed!")
    exit(1)
    
