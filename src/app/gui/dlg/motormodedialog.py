'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.Qt import QIcon, QCheckBox, QSize
from PyQt5.QtWidgets import QDialog
from dapi2 import SystemModeConfig
from functools import partial

from ..res import SystemModeConfigIcon
from .basedialog import BaseDialog
from .ui_motormodedialog import Ui_MotorModeDialog


class MotorModeDialog(BaseDialog, QDialog, Ui_MotorModeDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self.setupUi(self)
        self.checkBoxConfig = {}
        
        for i, config in enumerate(SystemModeConfig):
            o = QCheckBox(config.descr, self)
            o.setIcon(QIcon(SystemModeConfigIcon[config]))
            o.setIconSize(QSize(48,48))
            o.setToolTip(config.help) 
            o.setObjectName('checkBoxConfig'+config.name)
            self.checkBoxConfig[config.name] = o
            o.stateChanged.connect(partial(self.onConfigStateChanged, config))
            self.gridLayoutConfig.addWidget( o, i % 4, i // 4, 1, 1)
            i += 1        
        
        
    def _initialize(self):
        if not self.board: return
        self.registerAcceleration.setBoard(self.board)
        self.registerAcceleration.setReg(self.board.regs.acr)
        self.registerLightIntensity.setBoard(self.board)
        self.registerLightIntensity.setReg(self.board.regs.lir)
        self.board.regs.smr.changed.connect(self.onConfigChanged)
        
    def onConfigStateChanged(self, config=None, checked=None):
        try:
            self.log.debug('onConfigStateChanged(config={0!s}, checked={1!s})'.format(config, checked))
            self.board.setBit(self.board.regs.smr.bits(config.name.lower()), checked!=0)
        except Exception as e:
            self.parent.handleError(e)
            
    def onConfigChanged(self, reg, old, value):
        cfg = SystemModeConfig(value)
        for config in SystemModeConfig:
            self.checkBoxConfig[config.name].blockSignals(True)
            self.checkBoxConfig[config.name].setChecked(cfg & config != 0)
            self.checkBoxConfig[config.name].blockSignals(False)
    
