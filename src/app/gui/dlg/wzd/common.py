'''

:author:  F. Voillat
:date: 2022-06-08 Creation
:copyright: Dassym SA 2021
'''
from PyQt5.Qt import QWizardPage
import logging

from ..basedialog import BaseDialog  # @UnusedImport


class BaseWizardPage(QWizardPage):
    
    def __init__(self, parent=None):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('Initialize')
        
        QWizardPage.__init__(self, parent=parent)   
    
    def prepare(self):
        return
        #assert False, 'Abstract method!'
        
    def update(self):
        return
        
    def initializePage(self):
        QWizardPage.initializePage(self)
        self.log.debug('initializePage')
        
    
    def db(self):
        return self.wizard().db    

    def app(self):
        return self.wizard().app    
    
    
    
