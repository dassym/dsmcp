'''

:author: fv
:date: Created on 12 mai 2021
'''

from PyQt5.Qt import QFrame, QLabel, QHBoxLayout, QSizePolicy

class QRegister(QFrame):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        QFrame.__init__(self, parent)
        self._reg = None
        self.setContentsMargins(0,0,0,0)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._labelText = QLabel(self)
        self._labelText.setObjectName('labelText')
        self._labelText.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._layout.addWidget(self._labelText)
        
        self._labelValue = QLabel(self)
        self._labelValue.setObjectName('labelValue') 
        self._labelValue.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._layout.addWidget(self._labelValue)
        
        
        self.setLayout(self._layout)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
    def onRegisterChange(self, reg, old_value=None, new_value=None):
        if new_value is None:
            new_value = self._reg.value
        self._labelValue.setText( '{0:d} (0x{0:04x})'.format(new_value) )
        
    
        
    def setReg(self, reg=None ):
        if self._reg is not None:
            self._reg.disconnect(self.onRegisterChange)  
        self._labelValue.clear()
        self._reg = reg
        if self._reg is not None:
            self._labelText.setText(self._reg.name)
            self.setToolTip(self._reg.descr)
            self._reg.connect(self.onRegisterChange)
            self.onRegisterChange(self._reg, self._reg.value, self._reg.value)
        else:
            self._labelText.setText('~')
            self.setToolTip('')
        
    @property
    def reg(self):
        return self._reg
    
    