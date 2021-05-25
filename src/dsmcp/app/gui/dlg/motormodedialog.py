'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.QtWidgets import QDialog
import logging
from functools import partial
from PyQt5.Qt import QIcon, QCheckBox, QSize

from .ui_motormodedialog import Ui_MotorModeDialog
from app.gui.res import SystemModeConfigIcon
from dboard import SystemModeConfig


class MotorModeDialog(QDialog, Ui_MotorModeDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.app = parent.app
        self._board = None
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug( 'Initialize' )
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
        
        
    def _update(self):
        self.log.debug('_update')
        
    def setBoard(self, board):
        self._board = board
        self.registerAcceleration.setBoard(self._board)
        self.registerAcceleration.setReg(self._board.regs.acr)
        self.registerLightIntensity.setBoard(self._board)
        self.registerLightIntensity.setReg(self._board.regs.lir)
        self._board.regs.smr.connect(self.onConfigChanged)
        
        self._update() 
        
        
    def onConfigStateChanged(self, config=None, checked=None):
        try:
            self.log.debug('onConfigStateChanged(config={0!s}, checked={1!s})'.format(config, checked))
            self._board.setBit(self._board.regs.smr(config.name.lower()), checked!=0)
        except Exception as e:
            self.parent.handleError(e)
            
    def onConfigChanged(self, reg, old, value):
        cfg = SystemModeConfig(value)
        for config in SystemModeConfig:
            self.checkBoxConfig[config.name].blockSignals(True)
            self.checkBoxConfig[config.name].setChecked(cfg & config != 0)
            self.checkBoxConfig[config.name].blockSignals(False)
    
