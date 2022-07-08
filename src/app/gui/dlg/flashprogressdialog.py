'''

:author: fv
:date: Created on 5 mai 2021
'''
from PyQt5.Qt import QDialog, QPixmap
import time

from app.base import BaseApp

from .basedialog import BaseDialog
from .ui_flashprogressdiaog import Ui_FlashProgressDialog


class FlashProgressDialog(BaseDialog, QDialog, Ui_FlashProgressDialog):
    
    def __init__(self, parent, firmware):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self.firmware = firmware
        self.setupUi(self)
        self.t0 = time.time()
        self.labelIcon.setPixmap( QPixmap(':/img/128/upload-firmware.png'))
        self.labelText.setText(BaseApp.tr('Writing of `{f!s}` in progress...'.format(f=self.firmware)))
    
    def _initialize(self):
        pass

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