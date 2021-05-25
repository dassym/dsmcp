'''
Created on 14 oct. 2020

@author: fv
'''
from PyQt5.Qt import QPushButton

class QActionButton(QPushButton):
    '''
    classdocs
    '''


    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self._action = None
        if 'action' in kwargs:
            self.setAction(kwargs['action'])
            
    def _updateButtonStatus(self):
        if self._action is not None:
            self.setText(self._action.text())
            self.setStatusTip(self._action.statusTip())
            self.setToolTip(self._action.toolTip())
            self.setIcon(self._action.icon())
            self.setEnabled(self._action.isEnabled())
            self.setCheckable(self._action.isCheckable())
            self.setChecked(self._action.isChecked())
            
    def setAction(self, action):
        if self._action is not None:
            #TODO: reset action 
            pass 
        
        if action is not None:
            self._action = action
            self._updateButtonStatus()
            self._action.changed.connect(self._updateButtonStatus)
            self.clicked.connect( self._action.triggered )
            
            
            