'''
Created on 1 avr. 2020

@author: fv
'''


from PyQt5.Qt import QGridLayout, QSlider, QProgressBar, QSpinBox, Qt, QSizePolicy, \
    QLabel, QPixmap
import dapi2
from .base import QBaseWorkspaceWidget



class QSpeed(QBaseWorkspaceWidget):
    '''
    classdocs
    '''

    PAGESTEPS = {    0 :   10,
                   200 :  100,
                  2000 : 1000}

    def __init__(self, parent, board=None, graph=None):
        '''
        Constructor
        '''
        self._graph = graph
        super().__init__(parent, board)
        self.changed = dapi2.DSignal()


    def _initWidget(self):
        self._layout = QGridLayout()
        self._slider = QSlider(Qt.Horizontal, self)
        self._slider.setMaximum(40000)
        self._slider.setPageStep(100)
        self._slider.setObjectName('sliderMotorSpeed')
        self._icon = QLabel('Speed', self)
        self._icon.setPixmap(QPixmap(':/img/64/speed.png'))
        self._icon.setMinimumSize(64, 64)
        self._icon.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self._progressBar = QProgressBar(self)
        self._progressBar.setMaximum(40000)
        self._progressBar.setObjectName('progressBarMotorSpeed')
        self._progressBar.setFormat('%v')
        self._spinBox = QSpinBox(self)
        self._spinBox.setKeyboardTracking(False)
        self._spinBox.setMaximum(40000)
        self._spinBox.setSingleStep(100)
        self._spinBox.setStepType(QSpinBox.AdaptiveDecimalStepType)
        self._spinBox.setAccelerated(True)
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

        self.setGraph(self._graph)

        self.setLayout(self._layout)

        self._slider.valueChanged.connect(self._spinBox.setValue)
        self._spinBox.valueChanged.connect(self.onSpinboxValueChanged)

    def _updateStep(self):
        return
        step = [v for k,v in self.PAGESTEPS.items() if k <= self._spinBox.value()][-1]
        self._spinBox.setSingleStep(step)
        self._slider.setPageStep(step)


    def onRealSpeedChanged(self, reg, old=None, value=None):
        self._progressBar.setValue(value)


    def onSpeedChanged(self, reg, old=None, value=None):
        self.refresh()

    def onSpinboxValueChanged(self, value):
        temp = self._slider.blockSignals(True)
        try:
            self._slider.setValue(value)
            self._updateStep()
        finally:
            self._slider.blockSignals(temp)
        #self._board.setMotorSpeed(value)
        self.changed.emit(value)

    def setBoard(self, board):
        if self._board is not None:
            self._board.regs.msr.changed.disconnect(self.onRealSpeedChanged)
            self._board.regs.scr.changed.disconnect(self.onSpeedChanged)

        super().setBoard(board)
        self._progressBar.setValue(0)
        temp = self._spinBox.blockSignals(True)
        try:
            self._spinBox.setValue(0)
            self._slider.setValue(0)
            if self._board is not None:
                self.setRange(self._board.speed_range)
                self._board.regs.msr.changed.connect(self.onRealSpeedChanged)
                self._board.regs.scr.changed.connect(self.onSpeedChanged)
        finally:
            self._spinBox.blockSignals(temp)
        self.refresh()

    # def setSpeed(self, value):
    #     self.onSpeedChanged(None, value=value)

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


    def refresh(self):
        if not super().refresh(): return False
        temp = self._spinBox.blockSignals(True)
        self._slider.blockSignals(True)
        try:
            self._spinBox.setValue(self._board.regs.scr.value)
            self._slider.setValue(self._board.regs.scr.value)
            self._progressBar.setValue(self._board.regs.msr.value)
            self._updateStep()
        finally:
            self._slider.blockSignals(temp)
            self._spinBox.blockSignals(temp)
        if self._graph:
                self._graph.addData(self._board.motorRealSpeed())
        return True

    # def setEnabled(self, *args, **kwargs):
    #     return QFrame.setEnabled(self, *args, **kwargs)

    @property
    def graph(self):
        return self._graph
    @property
    def value(self):
        return self._spinBox.value()
