'''
Created on 8 avr. 2020

@author: fv
'''
from PyQt5.Qt import QFrame, QSizePolicy, QProgressBar, \
    QGridLayout, Qt
from PyQt5.QtWidgets import QLabel


class QAnalogInput(QFrame):
    '''
    classdocs
    '''


    def __init__(self, parent, analog_input=None, text=None, fmt='{0:0.02f}', maximum=100):
        '''
        Constructor
        '''
        QFrame.__init__(self, parent)
        self._input = None
        self.fmt = fmt
        
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._labelLabel = QLabel(self)
        self._labelLabel.setObjectName('labelLabel')
        self._labelLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._layout.addWidget(self._labelLabel)

        self._progress = QProgressBar(self)
        self._layout.addWidget(self._progress)
        self._progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._progress.setOrientation(Qt.Vertical)
        
        self.setLayout(self._layout)
        self.setAnalogInput(analog_input, text, fmt, maximum)
        
    
    def setAnalogInput(self, analog_input, text=None, fmt=None, maximum=100):
        if self._input is not None:
            self.reg.disconnect(self.onRegisterChange)  
        self._progress.setValue(0)
        self._progress.setMaximum(maximum)
        if fmt is not None:
            self.fmt = fmt
        self.setToolTip('')
        self._input = analog_input
        if self._input is not None:
            if text is None:
                text = self._input.name
            self.setToolTip(text)
            self.reg.changed.connect(self.onRegisterChange)
            self.refresh()
        
    def refresh(self):
        if self._input is None : return
        self._progress.setValue(self.value)
        self._labelLabel.setText(self.fmt.format(self.value))
        self.update()
        
    def onRegisterChange(self, reg, old_value=None, new_value=None):
        self.refresh()
        
            
    @property
    def analogInput(self):
        return self._input    
    @property
    def reg(self):
        return self._input.reg
    @property
    def value(self):
        return self._input.value

    
    