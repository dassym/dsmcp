'''Module for class DialogComPort. This module implement a dialog for choosing a communication port. 

:author: T. Marti
:date: 2021-03-10 Creation
'''
from .ui_selectconnectiondialog import Ui_SelectionConnectionDialog
from PyQt5.QtWidgets import QDialog

class SelectConnectionDialog(QDialog, Ui_SelectionConnectionDialog):
    """class for making a dialog windows for selecting the serial coomunication port
    
    :param list ports: list of available ports
    """
    def __init__(self, options):
        super(SelectConnectionDialog, self).__init__()
        self.setupUi(self)
        self.portIndex = []
        self.portRef = []
        for option in options:
            index = "[{}] {}".format(option[0], option[1])
            self.portIndex.append(index)
            self.portRef.append(option[0])
            self.comboBox.addItem(index)
            
    def getSelectedOption(self):
        """get the selected port of the dialog
        """
        return self.portRef[self.portIndex.index(self.comboBox.currentText())]