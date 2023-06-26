'''

:author: fv
:date: Created on 29 juin 2022
'''
from PyQt5.QtWidgets import QAction

class QBoardAction(QAction):
    '''
    classdocs
    '''
    
    
    @classmethod
    def cast(cls, action, *args, **kwargs):
        action.__class__ = cls
        action._subinit(*args, **kwargs)


    def __init__(self, *args, **kwargs):
        QAction.__init__(self, *args, **kwargs)
        '''
        Constructor
        '''
        self._subinit(*args, **kwargs)
    
    def __del__(self):
        self.setBoard(None)
        super().__del__()
        
    def _subinit(self, *args, **kwargs):
        self._board = None
        if 'board' in kwargs:
            self.setBoard(kwargs['board'])
        
    def setBoard(self, board):
        self._board = board
        
            
            
        
class QRegisterAction(QBoardAction):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        QBoardAction.__init__(self, *args, **kwargs)
        self._subinit(*args, **kwargs)
        
        
    def _subinit(self, *args, **kwargs):
        super()._subinit(*args, **kwargs)
        self._reg = None
        if 'reg' in kwargs:
            self.setReg(kwargs['reg'])
            
    def __del__(self):
        self.setReg(None)
        super().__del__()
        
    def setReg(self, reg, board=None):
        if board is not None:
            self.setBoard(board)
        if self._reg is not None:
            self._reg.changed.disconnect(self.onRegChanged)
        self._reg = reg
        if self._reg is not None:
            self._reg.changed.connect(self.onRegChanged)
            
    def onRegChanged(self, reg, old_value=None, new_value=None):
        self._value = new_value
    
    
class QRegBitAction(QBoardAction):
    '''
    classdocs
    '''
    
    
    

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        QBoardAction.__init__(self, *args, **kwargs)
        self._subinit()
        
    def _subinit(self, *args, **kwargs):
        super()._subinit(*args, **kwargs)
        self._bit = None
        self._neg = 0
        if 'bit' in kwargs:
            self.setBit(kwargs['bit'])

            
    def __del__(self):
        self.setBit(None)
        super().__del__()
            
        
    def setBit(self, bit, board=None):
        if board is not None:
            self.setBoard(board)
        if self._bit is not None:
            self._bit.parent.changed.disconnect(self.onRegChanged)
        self._bit = bit
        if self._bit is not None:
            self._bit.parent.changed.connect(self.onRegChanged)
            
    def onRegChanged(self, reg, old_value=None, new_value=None):
        self.parent().log.debug(f"QRegBitAction[{self._bit!s}].onRegChanged({reg!s}, {old_value}, {new_value})")
        self.blockSignals(True)
        v = (self._bit.get() ^ self._neg) != 0
        self.parent().log.debug(f".setChecked({v!s})")
        self.setEnabled(v != 0)
        self.blockSignals(False)     
        
class QRegBitNegAction(QRegBitAction):
    
    def setBit(self, bit, board=None):
        self._neg = (1<<bit.size)-1
        super().setBit(bit, board=board)
    
        
            
                