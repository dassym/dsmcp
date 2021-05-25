'''
Created on 1 avr. 2020

@author: fv
'''


from PyQt5.Qt import QFrame, QGridLayout, QSlider, QProgressBar, QSpinBox, Qt, QSizePolicy,\
    QLabel, QIcon, QSize

class QSpeed(QFrame):
    '''
    classdocs
    '''

    def __init__(self, parent, board=None, graph=None):
        '''
        Constructor
        '''
        self._board = None
        self._graph = graph
        super().__init__(parent)
        self._layout = QGridLayout()
        
        self._slider = QSlider(Qt.Horizontal, self)
        self._slider.setMaximum(40000)
        self._slider.setPageStep(1000)
        self._slider.setObjectName('sliderMotorSpeed')
        self._icon = QLabel('Speed', self)
        self._icon.setPixmap(QIcon(':/img/speed.svg').pixmap(QSize(64,64)))
        self._icon.setMinimumSize(64, 64)
        self._icon.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self._progressBar = QProgressBar(self)
        self._progressBar.setMaximum(40000)
        self._progressBar.setObjectName('progressBarMotorSpeed')
        self._progressBar.setFormat('%v')
        self._spinBox = QSpinBox(self)
        self._spinBox.setMaximum(40000)
        self._spinBox.setSingleStep(1000)
        self._spinBox.setObjectName('spinBoxMotorSpeed')
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._spinBox.sizePolicy().hasHeightForWidth())
        self._spinBox.setSizePolicy(sizePolicy)
        
        self._layout.addWidget(self._icon, 0, 0, 2, 1)
        self._layout.addWidget(self._slider, 0, 1, 1, 1)
        self._layout.addWidget(self._progressBar, 1, 1, 1, 1)
        self._layout.addWidget(self._spinBox, 0, 2, 2, 1)

        self.setGraph(graph)
        
        self.setLayout(self._layout)        
        
        self._slider.valueChanged.connect(self._spinBox.setValue)
        self._spinBox.valueChanged.connect(self.onSpinboxValueChanged)
        
        self.setBoard(board)
        
    def onRealSpeedChanged(self, reg, old=None, value=None):
        self._progressBar.setValue(value)
        
    
    def onSpeedChanged(self, reg, old=None, value=None):
        self._spinBox.blockSignals(True)
        self._spinBox.setValue(value)
        self._slider.setValue(value)
        self._spinBox.blockSignals(False)
        
    def onSpinboxValueChanged(self, value):
        self._slider.setValue(value)
        self._board.setMotorSpeed(value)
        
    def setBoard(self, board=None):
        if self._board is not None:
            pass  
        self._progressBar.setValue(0)
        self._spinBox.blockSignals(True)
        self._spinBox.setValue(0)
        self._slider.setValue(0)
        self._board = board
        if self._board is not None:
            self.setRange(self._board.speed_range)
            self._board.regs.msr.connect(self.onRealSpeedChanged)
            self._board.regs.scr.connect(self.onSpeedChanged)
        self._spinBox.blockSignals(False)
        
    def setSpeed(self, value):
        self.onSpeedChanged(None, value=value)

    def setGraph(self, graph):
        self._graph = graph
        if self._graph:
            self._layout.addWidget(self._graph, 2, 0, 1, 3)
            #self._graph.draw_idle()
            
    def setRange(self, valuerange):
        self._spinBox.setMaximum(valuerange.upper)
        self._slider.setMaximum(valuerange.upper)
        self._progressBar.setMaximum(valuerange.upper)
        if self._graph:
            self._graph.set_ylim(0,valuerange.upper)
         
            
    def update(self):
        if self._graph:
                self._graph.addData(self._motor.get_real_speed())
    
    @property
    def graph(self):
        return self._graph      
    @property
    def value(self):
        return self._spinBox.value()
        