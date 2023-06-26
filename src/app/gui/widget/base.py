'''

:author:  F. Voillat
:date: 2022-07-08 Creation
:copyright: Dassym SA 2021
'''
from PyQt5.Qt import QFrame
import logging


class QBaseWidget(QFrame):

    def __init__(self, parent):
        '''
        Constructor
        '''
        self._log = logging.getLogger(self.__class__.__name__)
        super().__init__(parent)

        self._initWidget()

    def _initWidget(self):
        assert False, "Abstract method!"


    @property
    def log(self):
        return self._log


class QBaseBoardWidget(QBaseWidget):

    def __init__(self, parent, board=None):
        '''
        Constructor
        '''
        super().__init__(parent)
        self._board = None
        self.setBoard(board)


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
        if self._board is None: return False
        self.setEnabled(self.shouldBeEnabled())
        return True

    @property
    def board(self):
        return self._board



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
        self.log.debug(f" > shouldBeEnabled => {self.shouldBeEnabled()!s}")
        self.setEnabled(self.shouldBeEnabled())

