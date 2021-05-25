'''

:author: fv
:date: Created on 5 mai 2021
'''
from PyQt5.Qt import QDialog, QIcon
from .ui_flashprogressdiaog import Ui_FlashProgressDialog
import logging
import time
from app.base import BaseApp

class FlashProgressDialog(QDialog, Ui_FlashProgressDialog):
    
    def __init__(self, parent, firmware):
        QDialog.__init__(self, parent)
        self.app = parent.app
        self.firmware = firmware
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Initialize' )
        self.setupUi(self)
        self.t0 = time.time()
        self.labelIcon.setPixmap( QIcon(':/img/upload-firmware.svg').pixmap(128,128) )
        self.labelText.setText(BaseApp.tr('Wrinting of `{f!s}` in progress...'.format(f=self.firmware)))
    

    def progress(self, i, n):
        p = i/n
        self.progressBar.setValue(int(p*100))
        if p >= 0.05:
            t = time.time() 
            d = t - self.t0
            r = d*((1/p) - 1)  
            self.labelRemainingTime.setText(BaseApp.tr('Remaining time: {0:.0f}s'.format(r)))
        else:
            self.labelRemainingTime.setText('')
            
        self.app.processEvents()