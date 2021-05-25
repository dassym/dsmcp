'''

:author: fv
:date: Created on 5 mai 2021
'''
from PyQt5.Qt import QDialog, QIcon

from .ui_sendfirmwaredialog import Ui_SendFirmwareDialog
import logging
from app.base import BaseApp

class SendFirmwareDialog(QDialog, Ui_SendFirmwareDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.app = parent.app
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Initialize' )
        self.setupUi(self)
        
        self.icons = {'O': QIcon(':/img/ok.svg'),
                    'W': QIcon(':/img/warning.svg'),
                    'E': QIcon(':/img/error.svg')
                    }
        
        firm = self.app.firmwares.get(
                        self.app.board,
                        self.app.board.getFirmwareTag(),
                        self.app.board.getFirmwareVersion(),
                        self.app.board.getFirmwareDate(),
                        )
        if firm is not None:
            self.labelActual.setText("Actual: "+str(firm))
        else:
            self.labelActual.setText("Actual: undefined (0x{0:04x})".format(self.app.board.getFirmwareTag()) )
        
        self._updateFirmwareList()
        
        
    def _updateFirmwareList(self):
        self.comboBoxFirmware.clear()
        self.labelFirmwareDesc.clear()
        #self.labelFirmwareIcon.clear()
        self.comboBoxFirmware.addItem(BaseApp.tr('Select firmware...'), None)
        self.comboBoxFirmware.insertSeparator(1)

        for firmware in self.app.firmwares:
            if self.app.firmwares.isLast(firmware):
                icon = self.icons['O']
            else: 
                icon = self.icons['W']
            self.comboBoxFirmware.addItem(icon, str(firmware), firmware)
        
        
        
    def getFirmware(self):
        return self.comboBoxFirmware.currentData()
        
    @property
    def board(self):
        return self.app.board