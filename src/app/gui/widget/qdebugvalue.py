'''
Created on 8 avr. 2020

@author: fv
'''


from PyQt5.Qt import QFrame, QSizePolicy, QHBoxLayout, QLabel


class QDebugValue(QFrame):
    '''
    classdocs
    '''


    def __init__(self, parent, dvalue=None):
        '''
        Constructor
        '''
        QFrame.__init__(self, parent)
        self._dvalue = None
        self._layout = QHBoxLayout(self)
        self._labelLabel = QLabel(self)
        self._labelLabel.setObjectName('labelLabel') 
        self._labelLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed )
        self._layout.addWidget(self._labelLabel)
        self._labelValue = QLabel(self)
        self._labelValue.setObjectName('labelValue') 
        self._labelValue.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self._layout.addWidget(self._labelValue)
        
        
        # self._graph_canevas = QGraphValueFigCanvas()
        # self._graph_canevas.setContentsMargins(0,0,0,0)
        #self._layout.addWidget(self._graph_canevas)
        
        self.setLayout(self._layout)
        
        if dvalue is not None:
            self.setDValue(dvalue) 
        
    def onValueChanged(self, dvalue):
        self.update()
    
    def setDValue(self, dvalue=None):
        if self._dvalue is not None:
            self._dvalue.disconnect(self.onValueChanged)
            self._labelLabel.clear()
        self._dvalue = dvalue
        if self._dvalue is not None:
            self._labelLabel.setText('#{0:d}'.format(self._dvalue.index))
            self._dvalue.connect(self.onValueChanged)
        self.update()
        
    def update(self):
        if self._dvalue is None or self._dvalue.value is None:
            self._labelValue.clear()
        else:
            self._labelValue.setText('{0:d}\n(0x{0:04x})'.format(self._dvalue.value))
            # self._graph_canevas.addData(self._dvalue.value)
            
    @property
    def reg(self):
        return self._reg
    # @property
    # def graph(self):
    #     return self._graph_canevas
    
    