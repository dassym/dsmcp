'''

:author: fv
:date: Created on 12 mai 2021
'''
from PyQt5.Qt import QSpinBox

class QSpinBoxRegister(QSpinBox):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        QSpinBox.__init__(self, parent)
        self._reg = None
        self._board = None
        self._disable_events_cnt = 0
        self.valueChanged.connect(self.spinboxValueChanged)
        
    def onRegisterChange(self, reg, old_value=None, new_value=None):
        if not self.eventsEnabled: return
        self.blockSignals(True)
        try:
            if new_value is None:
                new_value = self._reg.value
            self.setValue(new_value)
        finally:
            self.blockSignals(False)
            
    def spinboxValueChanged(self, value):
        if not self.eventsEnabled: return 
        if self._reg is not None and self._board is not None:
            self.disableEvents()
            try:
                self._board.setReg(self._reg, value)
            finally:
                self.enableEvents()
    
    def setBoard(self, board):
        self._board = board    
        
    def setReg(self, reg=None ):
        if self._reg is not None:
            self._reg.disconnect(self.onRegisterChange)  
        self._reg = reg
        if self._reg is not None:
            self.setToolTip(self._reg.name+":"+self._reg.descr)
            self._reg.connect(self.onRegisterChange)
            self.setMinimum(self._reg.min)
            self.setMaximum(self._reg.max)
            self.onRegisterChange(self._reg, self._reg.value, self._reg.value)
        else:
            self.setToolTip('')
            
    def disableEvents(self):
        self._disable_events_cnt += 1
        return self._disable_events_cnt
    
    def enableEvents(self):
        if self._disable_events_cnt > 0:
            self._disable_events_cnt -= 1
        return self._disable_events_cnt            
        
    @property
    def board(self):
        return self._board
    @property
    def reg(self):
        return self._reg
    
    @property
    def eventsEnabled(self):
        return self._disable_events_cnt == 0  
    
        