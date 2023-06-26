'''

:author: fv
:date: Created on 28 mai 2021
'''

from PyQt5.Qt import QHBoxLayout, QLabel, QSizePolicy, QPixmap
from dapi2.common import DApi2ErrorLevel
from dapi2.dapi2 import DApi2

from app.base import BaseApp
from .base import QBaseBoardWidget


class QError(QBaseBoardWidget):
    '''
    classdocs
    '''

    def __init__(self, parent, board=None, reg=None):
        '''
        Constructor
        '''
        self._reg = None
        super().__init__(parent, board)
        if reg is not None:
            self.setReg(reg)

    def _initWidget(self):
        self._layout = QHBoxLayout()
        self._labelIcon = QLabel(self)
        self._labelText = QLabel(self)
        self._labelText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._layout.addWidget(self._labelIcon)
        self._layout.addWidget(self._labelText)
        self.setLayout(self._layout)
        self._dapi  = None
        self._lang = None
        self._labelText.setText("Undefined")

    def refresh(self):
        if self.board is not None:
            if not self.board.dcom.isOpen():
                self._labelIcon.setPixmap(QPixmap(':/img/32/warning.png'))
                self._labelText.setText(BaseApp.tr("No link with the electronic board!"))
            else:
                error = self.board.dapi.derrors(self._reg.value)
                self._labelIcon.setPixmap(QPixmap(':/img/32/{0:s}.png'.format(error.level.name.lower())))
                self._labelIcon.setToolTip(error.level.label)
                if error.level == DApi2ErrorLevel.OK:
                    self._labelText.setText(error.getDescription(self._lang))
                else:
                    self._labelText.setText(error.getDescription(self._lang)+" #{0:d} (0x{0:02x})".format(error.num))
                    self._labelText.setToolTip(error.name)
        elif self._reg is not None:
            level = DApi2ErrorLevel.levelOf(self._reg.value)
            self._labelIcon.setPixmap(QPixmap(':/img/32/{0:s}.png'.format(level.name.lower())))
            if self._regvalue == 0:
                self._labelText.setText(BaseApp.tr("OK"))
            else:
                self._labelText.setText(BaseApp.tr("Error #{0:d} (0x{0:02X})").format(self._regvalue))
            self._labelIcon.setToolTip(level.label)
        else:
            self._labelIcon.setPixmap(QPixmap(':/img/32/unknow.png'))
            self._labelText.setText(BaseApp.tr("The error status is unknown."))

    def onRegisterChange(self, reg, old_value=None, new_value=None):
        self.refresh()



    # def setDApi(self, dapi):
    #     assert isinstance(dapi, DApi2)
    #     self._dapi = dapi

    def setLang(self, lang):
        self._lang = lang

    def setReg(self, reg=None, board=None):
        if board is not None:
            self.setBoard(board)
        if self._reg is not None:
            self._reg.changed.disconnect(self.onRegisterChange)
        self._labelIcon.clear()
        self._labelText.clear()
        self._reg = reg
        if self._reg is not None:
            self._reg.changed.connect(self.onRegisterChange)
            self.onRegisterChange(self._reg, self._reg.value, self._reg.value)

    @property
    def reg(self):
        return self._reg
