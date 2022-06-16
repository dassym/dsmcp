'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from dapi2.dapi2 import DApiAccessLevel

from app.base import BaseApp

from ..common import UserActionHandler
from .basedialog import BaseDialog
from .ui_connectdialog import Ui_ConnectDialog


class ConnectDialog(BaseDialog, QDialog, Ui_ConnectDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self.setupUi(self)
        self.comboBoxAccess.currentIndexChanged.connect(self.onAccessChanged)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect( self.onReset )
        
    def _initialize(self):
        self.disableEvents()
        self.comboBoxAccess.addItem(BaseApp.tr('Select access...'), 0)
        for a in DApiAccessLevel:
            self.comboBoxAccess.addItem(a.name, a)
        self.enableEvents()
            
    def _reset(self):
        self.comboBoxAccess.setCurrentIndex(0)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.label.setText("Current access level is <b>{0:s}</b>.<br>Select the desired connection level!".format(self.board.getAccessLevel().name)) 
        
    def getAccessLevel(self):
        return self.comboBoxAccess.currentData()
    
        
    @UserActionHandler
    def onAccessChanged(self, index):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.comboBoxAccess.currentIndex()!=0)    @UserActionHandler
    
    @UserActionHandler
    def onReset(self, button):
        self._reset()