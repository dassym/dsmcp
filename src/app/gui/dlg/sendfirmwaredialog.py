'''

:author: fv
:date: Created on 5 mai 2021
'''
from PyQt5.Qt import QDialog, QIcon

from app.base import BaseApp

from .basedialog import BaseDialog
from .ui_sendfirmwaredialog import Ui_SendFirmwareDialog


class SendFirmwareDialog(BaseDialog, QDialog, Ui_SendFirmwareDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self.setupUi(self)
        
        self.icons = {'O': QIcon(':/img/32/ok.png'),
                    'W': QIcon(':/img/32/warning.png'),
                    'E': QIcon(':/img/32/error.png')
                    }
        
        firm = self.db.firmwares.get(
                        type(self.app.board),
                        self.app.board.getFirmwareTag(),
                        self.app.board.getFirmwareVersion(),
                        self.app.board.getFirmwareDate(),
                        )
        if firm is not None:
            self.labelActual.setText("Actual: "+str(firm))
        else:
            self.labelActual.setText("Actual: undefined (0x{0:04x})".format(self.app.board.getFirmwareTag()) )
        
        #self._updateFirmwareList()
        
        
    def _initialize(self):
        self.comboBoxFirmware.clear()
        self.labelFirmwareDesc.clear()
        #self.labelFirmwareIcon.clear()
        self.comboBoxFirmware.addItem(BaseApp.tr('Select firmware...'), None)
        self.comboBoxFirmware.insertSeparator(1)

        for firmware in sorted(self.db.firmwares.find(type(self.app.board)), key=lambda x: str(x) ):
            if self.db.firmwares.isLast(firmware):
                icon = self.icons['O']
            else: 
                icon = self.icons['W']
            self.comboBoxFirmware.addItem(icon, str(firmware), firmware)
        
    def getFirmware(self):
        return self.comboBoxFirmware.currentData()
        
