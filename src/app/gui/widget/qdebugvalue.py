'''
Created on 8 avr. 2020

@author: fv
'''


from PyQt5.Qt import QSizePolicy, QHBoxLayout, QLabel, QSpinBox

import dapi2
from ...utils import int2bin
from .base import QBaseWidget

class QDebugValue(QBaseWidget):
    '''
    classdocs
    '''


    def __init__(self, parent, dvalue=None):
        '''
        Constructor
        '''
        self._dvalue = None
        QBaseWidget.__init__(self, parent)
        self.setMinimumSize(100, 50)
        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)

        if dvalue is not None:
            self.setDValue(dvalue)


    def _initWidget(self):
        self._layout = QHBoxLayout(self)
        self._labelLabel = QLabel(self)
        self._labelLabel.setObjectName('labelLabel')
        self._labelLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed )
        self._layout.addWidget(self._labelLabel)
        self.changed = None
        self._labelValue = None
        self.setLayout(self._layout)

    def onValueChanged(self, dvalue):
        self.update()

    def setDValue(self, dvalue=None):
        if self._dvalue is not None:
            self._dvalue.disconnect(self.onValueChanged)
        self._dvalue = dvalue
        if self._dvalue is not None:
            self._labelLabel.setText(f"{self._dvalue.index}")
            self._labelLabel.setToolTip(self._dvalue.name)
            if not self._dvalue.writable:
                self.changed = None
                self._labelValue = QLabel(self)
                self._labelValue.setObjectName(f'labelDebugValue{dvalue.reg.index}')
                #self._labelValue.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)
            else:
                self.changed = dapi2.DSignal()
                self._labelValue = QSpinBox(self)
                self._labelValue.setKeyboardTracking(False)
                self._labelValue.setMinimum(dvalue.reg.min)
                self._labelValue.setMaximum(dvalue.reg.max)
                #self._labelValue.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed)
                self._labelValue.setSingleStep(1)
                self._labelValue.setObjectName(f'spinBoxDebugSettingValue{dvalue.reg.index}')
                self._labelValue.valueChanged.connect(self.onSpinboxValueChanged)

                self.changed.connect(self._dvalue.setValue)

            self._labelValue.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            self._layout.addWidget(self._labelValue)
            self._dvalue.connect(self.onValueChanged)
        self.update()

    def update(self):
        if self._dvalue is None or self._dvalue.value is None:
            self._labelValue.clear()
        elif self._dvalue.writable:
            self._labelValue.blockSignals(True)
            self._labelValue.setValue(self._dvalue.value)
            self._labelValue.blockSignals(False)
        else:
            self._labelValue.setText('{0:d}\n0x{0:04X}'.format(self._dvalue.value))
        self._labelValue.setToolTip('0b ' + int2bin(self._dvalue.value))

    def onSpinboxValueChanged(self, value):
        self.log.debug(f'onSpinboxValueChanged({value!s})')
        self.changed.emit(value)



    @property
    def reg(self):
        return self._reg
