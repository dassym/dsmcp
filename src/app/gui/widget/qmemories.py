'''

:author: fv
:date: Created on 28 mai 2021
'''

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QGroupBox, QHBoxLayout, \
    QGridLayout

from .qactionbutton import QActionButton


#from PyQt5.Qt import pyqtSignal
class QMemory(QFrame):
    
    #memoryStore = pyqtSignal(int)
    #memoryRecall = pyqtSignal(int)
    
    def __init__(self, number, parent):
        self._number = number
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout0 = QHBoxLayout()
        self._labelName = QLabel(self.caption, self)
        self._labelStatus = QLabel(self)
        self._layout0.addWidget(self._labelName)
        self._layout0.addWidget(self._labelStatus)
        self._labelStatus.setPixmap(QPixmap(':img/24/status-off.png'))
        self._layout1 = QVBoxLayout()
        self._actionButtonRecall = QActionButton(self)
        self._actionButtonRecall.setObjectName('actionButtonRecall_M{0:d}'.format(self._number))
        self._actionButtonRecall.setToolTip('Recall')
        self._actionButtonStore = QActionButton(self)
        self._actionButtonStore.setObjectName('actionButtonStore_M{0:d}'.format(self._number))
        self._actionButtonStore.setToolTip('Store')
        self._layout1.addWidget(self._actionButtonRecall)
        self._layout1.addWidget(self._actionButtonStore)
        self._layout.addLayout(self._layout0)
        self._layout.addLayout(self._layout1)
        
        #self._pushButtonRecall.clicked.connect(self.onRecall)
        #self._pushButtonStore.clicked.connect(self.onStore)

    def refresh(self):
        #if (not self.board.isOnStandby()) and self.isCurrent():
        if self.isCurrent():
            self._labelStatus.setPixmap(QPixmap(':img/24/status-on.png'))
        else:
            self._labelStatus.setPixmap(QPixmap(':img/24/status-off.png'))
            
    # def onStore(self):
    #     self.memoryStore.emit(self._number)
    #
    # def onRecall(self):
    #     self.memoryRecall.emit(self._number)
    
    def isCurrent(self):
        if self.board.isOnStandby():
            return False
        return self.board.getWorkspace().memories[self._number].isCurrent()  
    
    def setStoreAction(self, action):
        self._actionButtonStore.setAction(action)
                
    def setRecallAction(self, action):
        self._actionButtonRecall.setAction(action)
    
    @property
    def number(self):
        return self._number

    @property
    def caption(self):
        return "M{0:2d}".format(self.number)
    
    @property
    def board(self):
        return self.parent().board
    
class QMemories(QGroupBox):
    '''
    classdocs
    '''
    
    #memoryStore = pyqtSignal(int)
    #memoryRecall = pyqtSignal(int)
    
    def __init__(self, *args, board=None, count=4):
        '''
        Constructor
        '''
        self._lang = None
        self._board = None
        self._cols = 4
        self._count = count
        self._widgets = []
        super().__init__(*args)
        
        self._layout = QGridLayout(self)
        
        if board is not None:
            self.setBoard(board)

    def __getitem__(self, index):
        return self._widgets[index]
    
    def __len__(self):
        return len(self._widgets)
    
    def __iter__(self):
        for w in self._widgets:
            yield w     
    
    def _add(self, i):
        o = QMemory(i+1 , self)
        self._widgets.append(o)
        self._layout.addWidget( o, i // self._cols, i % self._cols, 1, 1)
        
    def _initialize(self):
        for i in range(self._count):
            self._add(i)
        
    def _clear(self):
        for w in self._widgets:
            del w
        self._widgets = []   
        
    def _refreshMemories(self):
        for w in self:
            w.refresh()
             
    def refresh(self):
        if self._board is None: return
        self._refreshMemories()

    def setLang(self, lang):
        if self._lang != lang:
            self._lang = lang
            self._clear()
            self._initialize()
        
    def setBoard(self, board=None):
        if board != self._board:
            self._board = board
        self.refresh()
                
    def setCount(self, count):
        if self._count < count:
            for i in range(self._count, count):
                self._add(i)
            self._count = count
        elif self._count > count:
            self._widgets[:count]
        self.refresh()
                
    # def onMemoryStore(self, number):
    #     self.memoryStore.emit(number)
    #
    # def onMemoryRecall(self, number):
    #     self.memoryRecall.emit(number)

    @property
    def count(self):
        return self._count
                    
    @property
    def board(self):
        return self._board
                
        