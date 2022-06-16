'''

:author: fv
:date: Created on 28 mai 2021
'''

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QCheckBox, \
    QVBoxLayout
from dapi2 import SystemModeConfig
from functools import partial

from ..res import SystemModeConfigIcon


class QSystemMode(QFrame):
    '''
    classdocs
    '''
    dev_mode=False
    
    def __init__(self, parent, cols=4):
        '''
        Constructor
        '''
        self._board = None
        self._lang = None
        self.checkBoxConfig = {}
        super().__init__(parent)
        
        self._vlayout = QVBoxLayout(self)
        self._labelText = QLabel(self)
        self._vlayout.addWidget(self._labelText)
        self._glayout = QGridLayout()
        self._vlayout.addLayout(self._glayout)
        
    
        
        for i, config in enumerate(SystemModeConfig):
            o = QCheckBox(config.descr, self)
            o.setIcon(QIcon(SystemModeConfigIcon[config]))
            o.setIconSize(QSize(48,48))
            o.setToolTip(config.help) 
            o.setObjectName('checkBoxConfig'+config.name)
            self.checkBoxConfig[config.name] = o
            o.stateChanged.connect(partial(self.onConfigStateChanged, config))
            self._glayout.addWidget( o, i // cols, i % cols, 1, 1)
            i += 1    
            
        self._labelText.setVisible(self.dev_mode)
        
        
    def refresh(self):
        if self._board is None: return
        cfg = SystemModeConfig(self._board.regs.smr.value)
        if self.dev_mode:
            self._labelText.setText("{r.name:s} = 0x{r.value:04x} ({r.value:d})".format(r=self._board.regs.smr))
        for config in SystemModeConfig:
            self.checkBoxConfig[config.name].blockSignals(True)
            self.checkBoxConfig[config.name].setChecked(cfg & config != 0)
            self.checkBoxConfig[config.name].blockSignals(False)

    def onRegisterChange(self, reg, old_value=None, new_value=None):
        self.refresh()
            
    def onConfigStateChanged(self, config=None, checked=None):
        self._board.setBit(self._board.regs.smr.bits(config.name.lower()), checked!=0)
            
    def setLang(self, lang):
        self._lang = lang
        # for config in SystemModeConfig:
        #     self.checkBoxConfig[config.name].setText(config.description(lang)) 
        
    def setBoard(self, board=None):
        if board != self._board:
            if self._board is not None:
                self._board.regs.smr.changed.disconnect(self.onRegisterChange)
            self._labelText.clear()
            self._board = board
            if self._board is not None:
                self._board.regs.smr.changed.connect(self.onRegisterChange)
                self.refresh()

    
class QSystemModeDev(QSystemMode):
    dev_mode=True
