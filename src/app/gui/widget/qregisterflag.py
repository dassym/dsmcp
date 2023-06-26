'''

:author: fv
:date: Created on 28 mai 2021
'''

from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QCheckBox, \
    QVBoxLayout
    
from ...utils import int2bin     


class QRegisterFlag(QFrame):
    '''
    classdocs
    '''
    
    def __init__(self, parent, reg=None):
        '''
        Constructor
        '''
        self._lang = None
        self._reg = None
        self._cols = 4
        self._widgets = {}
        super().__init__(parent)
        
        self._vlayout = QVBoxLayout(self)
        self._labelText = QLabel(self)
        self._vlayout.addWidget(self._labelText)
        self._glayout = QGridLayout()
        self._vlayout.addLayout(self._glayout)
        
        self._labelText.setVisible(False)
        
        if reg is not None:
            self.setReg(reg)
        
    
    def _initialize(self):
        for flag in self._reg:
            o = QCheckBox("{0:d}:{1!s}".format(flag.addr,flag.name), self)
            o.setToolTip(flag.descr)
            o.setObjectName(self._reg.name+'CheckBox'+flag.name)
            self._widgets[flag.name] = o
            self._glayout.addWidget( o, flag.addr // self._cols, flag.addr % self._cols, 1, 1)
        
    def _clear(self):
        self._labelText.clear()
        for w in list(self._widgets.values()):
            del w
        self._widgets = {}       
        
    def _refreshFlags(self):
        for flag in self._reg:
            w = self._widgets[flag.name]
            w.blockSignals(True)
            w.setChecked(flag.value != 0)
            w.blockSignals(False)
             
    def refresh(self):
        if self._reg is None: return
        self._refreshFlags()

    def onRegisterChange(self, reg, old_value=None, new_value=None):
        self.refresh()
            
    def setLang(self, lang):
        self._lang = lang
        # for config in SystemModeConfig:
        #     self.checkBoxConfig[config.name].setText(config.description(lang)) 
        
    def setReg(self, reg=None):
        if reg != self._reg:
            if self._reg is not None:
                self._reg.changed.disconnect(self.onRegisterChange)
            self._clear()
            self._reg = reg
            if self._reg is not None:
                self._initialize()
                self._reg.changed.connect(self.onRegisterChange)
                self.refresh()
                
    @property
    def reg(self):
        return self._reg
                
        
class QRegisterFlagDev(QRegisterFlag):
    
    def refresh(self):
        if self._reg is None: return
        self._labelText.setText("{r.name:s} = 0x{r.value:04X} <small>{r.value:d}</small>".format(r=self._reg))
        self._labelText.setToolTip('0b ' + int2bin(self._reg.value))
        self._labelText.setVisible(True)
        self._refreshFlags()        