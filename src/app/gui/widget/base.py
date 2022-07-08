'''

:author:  F. Voillat
:date: 2022-07-08 Creation
:copyright: Dassym SA 2021
'''
from PyQt5.Qt import QFrame
import logging


class QBaseBoardWidget(QFrame):

    def __init__(self, parent, board=None):
        '''
        Constructor
        '''
        self._log = logging.getLogger(self.__class__.__name__)
        super().__init__(parent)
        self._board = None
        
        self._initWidget()
        
        self.setBoard(board)

    def _initWidget(self):
        assert False, "Abstract method!"
    
    def setBoard(self, board):
        if self._board is not None:
            self._board.connectionChanged.disconnect(self.onConnectionChanged)
        self._board = board
        if self._board is not None:
            self._board.connectionChanged.connect(self.onConnectionChanged)
            
    def shouldBeEnabled(self):
        try:
            return self._board.dcom.isOpen()
        except Exception as e:
            self.log.error(str(e))
            return False
        
            
    def onConnectionChanged(self, state, level):
        self.log.debug(f"onConnectionChanged({state!s}, {level!s})")
        self.setEnabled(self.shouldBeEnabled())
            
    def refresh(self):
        pass
    
    @property
    def board(self):
        return self._board
    @property
    def log(self):
        return self._log
            
    

class QBaseWorkspaceWidget(QBaseBoardWidget):
    '''
    classdocs
    '''

    def setBoard(self, board):
        if self._board is not None:
            self._board.workspaceChanged.disconnect(self.onWorkspaceChanged)
        super().setBoard(board)
        if self._board is not None:
            self._board.workspaceChanged.connect(self.onWorkspaceChanged)
       
    def shouldBeEnabled(self):
        try:
            return super().shouldBeEnabled() and self.board.getWorkspace().isFunctional()
        except Exception as e:
            self.log.error(str(e))
            return False


    def onWorkspaceChanged(self, workspace):
        self.log.debug(f"onWorkspaceChanged({workspace!s})")
        self.setEnabled(self.shouldBeEnabled())
