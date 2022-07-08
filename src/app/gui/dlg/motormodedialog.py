'''
Created on 27 sept. 2018

@author: fvoillat
'''

from PyQt5.QtWidgets import QDialog

from .basedialog import BaseDialog
from .ui_motormodedialog import Ui_MotorModeDialog


class MotorModeDialog(BaseDialog, QDialog, Ui_MotorModeDialog):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        BaseDialog.__init__(self, parent.app)
        self.setupUi(self)
        
    def boardInit(self):
        super().boardInit()
        self.registerAcceleration.setBoard(self.board)
        self.registerAcceleration.setReg(self.board.regs.acr)
        self.registerLightIntensity.setBoard(self.board)
        self.registerLightIntensity.setReg(self.board.regs.lir)
        self.systemMode.setBoard(self.board)
        
    def onWorkspaceChanged(self, workspace):
        super().onWorkspaceChanged(workspace)
        e = not self.board.isOnStandby()
        self.systemMode.setEnabled(e)
        self.registerAcceleration.setEnabled(e)
        self.registerLightIntensity.setEnabled(e)
            
        
    # def onConfigStateChanged(self, config=None, checked=None):
    #     try:
    #         self.log.debug('onConfigStateChanged(config={0!s}, checked={1!s})'.format(config, checked))
    #         self.board.setBit(self.board.regs.smr.bits(config.name.lower()), checked!=0)
    #     except Exception as e:
    #         self.parent.handleError(e)
            
    # def onConfigChanged(self, reg, old, value):
    #     cfg = SystemModeConfig(value)
    #     for config in SystemModeConfig:
    #         self.checkBoxConfig[config.name].blockSignals(True)
    #         self.checkBoxConfig[config.name].setChecked(cfg & config != 0)
    #         self.checkBoxConfig[config.name].blockSignals(False)
    
