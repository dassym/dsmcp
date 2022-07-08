'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.Qt import QT_VERSION_STR, PYQT_VERSION_STR, QPixmap
from PyQt5.QtWidgets import QDialog
import platform
import sys

from .basedialog import BaseDialog
from .ui_aboutdialog import Ui_AboutDialog


class AboutDialog(BaseDialog, QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self.setupUi(self)
        self.labelLogo.setPixmap(QPixmap(':/img/64/icon_dcp.png'))
        
    def _initialize(self):
        self.labelApplication.setText( self.app.applicationName() )
        self.labelVersion.setText( self.app.applicationVersion() )
        
        sys_info = '<html><body>'+\
            '<a href="https://www.python.org/">Python</a> : {} ({})'.format( ".".join([str(x) for x in sys.version_info[:3]]), platform.architecture()[0] ) + \
            '<br>OS : {}'.format(platform.platform()) + \
            '<br><a href="https://www.qt.io/">Qt</a> : {0!s} '.format(QT_VERSION_STR) + \
            '<a href="https://riverbankcomputing.com/software/pyqt/intro">PyQt</a> : {0!s}'.format(PYQT_VERSION_STR) + \
            '<br>Qt locale : `{0!s}` ; décimal: `{1!s}`'.format(self.app.locale.name(), self.app.locale.decimalPoint()) + \
            '<br><a href="https://github.com/dassym/PyDapi2">PyDapi2</a> : `{0!s}`'.format(self.app.dapi.version()) + \
            '</body></html>' 
 
        self.labelSystem.setText( sys_info )
        self.labelSystem.setOpenExternalLinks(True)
        
