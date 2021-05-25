'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.QtWidgets import QDialog
import logging
from PyQt5.Qt import QIcon, QT_VERSION_STR, PYQT_VERSION_STR
import platform
import sys

from .ui_aboutdialog import Ui_AboutDialog


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        
        self._app = parent.app
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Initialize' )
        self.setupUi(self)
        self.labelLogo.setPixmap(QIcon(':/img/icon_dcp.svg').pixmap(64,64) )
        
        
    def exec(self):
        #self.setWindowTitle()
        self.labelApplication.setText( self._app.applicationName() )
        self.labelVersion.setText( self._app.applicationVersion() )
        
        sys_info = '<html><body>'+\
            '<a href="https://www.python.org/">Python</a> : {} ({})'.format( ".".join([str(x) for x in sys.version_info[:3]]), platform.architecture()[0] ) + \
            '<br>OS : {}'.format(platform.platform()) + \
            '<br><a href="https://www.qt.io/">Qt</a> : {0!s} '.format(QT_VERSION_STR) + \
            '<a href="https://riverbankcomputing.com/software/pyqt/intro">PyQt</a> : {0!s}'.format(PYQT_VERSION_STR) + \
            '<br>Qt locale : `{0!s}` ; décimal: `{1!s}`'.format(self._app.locale.name(), self._app.locale.decimalPoint()) + \
            '<br><a href="https://github.com/dassym/PyDapi2">PyDapi2</a> : `{0!s}`'.format(self._app.dapi.version()) + \
            '</body></html>' 
 
        self.labelSystem.setText( sys_info )
        self.labelSystem.setOpenExternalLinks(True)
        return super().exec()
        
