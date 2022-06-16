'''
Created on 5 mai 2020

@author: fv
'''
from PyQt5.Qt import QWizard, QCoreApplication

from .base import BaseDialog, WizardProdStartup
from .ui_startup import Ui_WizardProdStartup


class QWizardProdStartup(WizardProdStartup, QWizard, Ui_WizardProdStartup): 

    @classmethod
    def tr(cls, text, disambiguation=None, n=-1):
        return QCoreApplication.translate('WizardProdStartup', text, disambiguation, n)       
    
    def __init__(self, parent):
        QWizard.__init__(self,parent)
        BaseDialog.__init__(self, parent.app)
        self.setupUi(self)
        

    
    def prepare(self):
        self.log.debug('prepare')
        start = 0
        board_variant = None
        for page in [self.page(pid) for pid in self.pageIds() ]:
            page.prepare()
        
                
        if self.config.customer:
            self.setCustomer(self.db.getCustomer(self.config.customer))
            start = 1
            #self.setField('customer', self.db.getCustomer(self.config.customer))
        if self.config.board_type:
            board_variant = self.db.getBoardVariant(self.config.board_type.upper())
            self.setBoardVariant(board_variant)
            if start != 0:
                start = 3
            
        if self.config.firmware:
            if board_variant is None:
                raise Exception(WizardProdStartup.tr('Board variant undefined!'))
            
            self.log.debug('find firmware with : {name!s} and version {version!s}'.format(**self.config.firmware))
            firm = self.db.firmwares.get(board_variant.board, **self.config.firmware)
            if firm is None:
                self.app.sayError(WizardProdStartup.tr("Firmware {name!s} v {version!s} not found!").format(**self.config.firmware))
            else:
                self.setFirmware(firm)
                if start != 0:
                    start = 4
            
                
        if self.config.serial_numbers:
            self.setSerial(';'.join(self.config.serial_numbers))
        if self.config.order:
            self.setOrder(self.config.order)
            
        self.setStartId(start)

    
    def restart(self):
        self._customer = None
        self._board_variant = None
        self._board_version = None
        self._firmware = None
        QWizard.restart(self)
        
    def setCustomer(self, customer):
        self.log.debug('setCustomer({0!s})'.format(customer))
        self.setField('customer', self.comboBoxCustomer.findData(customer))
        
        #self.comboBoxCustomer.setCurrentIndex(self.comboBoxCustomer.findData(customer))

    def setBoardVariant(self, board_variant):
        self.log.debug('setBoardVariant({0!s})'.format(board_variant))
        self.setField('board', self.comboBoxBoard.findData(board_variant.board))
        self.wizardPageVariant.update()
        self.comboBoxBoard.setCurrentIndex(self.comboBoxBoard.findData(board_variant.board))
        self.comboBoxBoardVariant.setCurrentIndex(self.comboBoxBoardVariant.findData(board_variant))
        self.comboBoxBoardVersion.setCurrentIndex(self.comboBoxBoardVersion.findData(board_variant.board.getLastVersion()))
        self.wizardPageFirmware.initializePage()
        
    def setFirmware(self, firmware):
        self.log.debug('setFirmware({0!s})'.format(firmware))
        self.comboBoxFirmware.setCurrentIndex(self.comboBoxFirmware.findData(firmware))
        
    def setSerial(self, serial):
        self.log.debug('setSerial({0!s})'.format(serial))
        self.lineEditSerialNumber.setText(serial)

    def setOrder(self, order):
        self.log.debug('setOrder({0!s})'.format(order))
        self.lineEditManufacturingOrder.setText(order)
    

    def getFirmware(self):
        return self.comboBoxFirmware.itemData(self.field('firmware'))
            
    def getCustomer(self):
        return self.comboBoxCustomer.itemData(self.field('customer'))

    def getBoardVariant(self):
        return self.comboBoxBoardVariant.itemData(self.field('board.variant'))

    def getBoardVersion(self):
        return self.comboBoxBoardVersion.itemData(self.field('board.version'))

    def getSerial(self):
        return self.field('serial')
    
    def getOrder(self):
        return self.field('order')
    

