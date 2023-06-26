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
        
    def _initialize(self, **kwargs):
        self.disableEvents()
        self.comboBoxAccess.addItem(BaseApp.tr('Select access...'), 0)
        for a in DApiAccessLevel:
            self.comboBoxAccess.addItem(a.name, a)
        self.enableEvents()
            
    def _reset(self, **kwargs):
        if 'index' in kwargs and kwargs['index'] is not None:
            self.comboBoxAccess.setCurrentIndex(kwargs['index'])
        if 'level' in kwargs and kwargs['level'] is not None:
            self.setAccessLevel(kwargs['level'])
        else:
            self.comboBoxAccess.setCurrentIndex(0)
            #self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        
        self.label.setText("Current access level is <b>{0:s}</b>.<br>Select the desired connection level!".format(self.board.getAccessLevel().name)) 
        
    
    def setAccessLevel(self, level):
        index = self.comboBoxAccess.findData(level)
        if index >= 0:
            self.comboBoxAccess.setCurrentIndex(index)
        
    
    def getAccessLevel(self):
        return self.comboBoxAccess.currentData()
    
    def getLevelIndex(self):
        return self.comboBoxAccess.currentIndex()
    
    @UserActionHandler
    def onAccessChanged(self, index):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.comboBoxAccess.currentIndex()!=0)
    
    @UserActionHandler
    def onReset(self, button):
        self._reset()