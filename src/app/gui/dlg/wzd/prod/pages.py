'''

:author:  F. Voillat
:date: 2022-06-15 Creation
:copyright: Dassym SA 2021
'''
from PyQt5.Qt import Qt, QPixmap
import dapi2

from app.db.partner import DbCustomer

from .base import WizardProdStartup, BaseWizardPage


class QWizarpageSartupCustomer(BaseWizardPage):
    

    def prepare(self):
        self._comboBoxCustomer = self.wizard().comboBoxCustomer
        self._labelCustomerLogo = self.wizard().labelCustomerLogo
        # self._comboBoxCustomer.addItem(BaseWizardpage.tr('Select customer...'), None)
        # self._comboBoxCustomer.insertSeparator(1)
        self._comboBoxCustomer.addItem(self.db().standard_cust.name, self.db().standard_cust)
        # self._comboBoxCustomer.insertSeparator(3)
        self._comboBoxCustomer.currentIndexChanged.connect(self.onSelectionChanged)
        for customer in sorted(self.db().getCustomers(),key=DbCustomer.getKey):
            self._comboBoxCustomer.addItem(customer.name, customer)
        self._comboBoxCustomer.setCurrentIndex(-1)
        self.registerField('customer*', self._comboBoxCustomer)
        
            
    def onSelectionChanged(self, index):
        customer = self._comboBoxCustomer.itemData(index)
        if customer:
            if customer.logo is not None:   
                self._labelCustomerLogo.setPixmap( QPixmap(str(customer.logo)).scaled(self._labelCustomerLogo.minimumSize(),  Qt.KeepAspectRatio, Qt.SmoothTransformation) )
            else:
                self._labelCustomerLogo.clear()
        else:
            self._labelCustomerLogo.clear()
            

class QWizarpageSartupBoard(BaseWizardPage):
        
    def prepare(self):
        self._comboBoxBoard = self.wizard().comboBoxBoard
        self._labelBoardImage = self.wizard().labelBoardImage
        self._comboBoxBoard.currentIndexChanged.connect(self.onSelectionChanged)
        self.registerField('board*', self._comboBoxBoard)
        self.update()


    def update(self):
        for board in sorted(self.db().boards.values(),key=lambda x:x.id):
            self._comboBoxBoard.addItem(board.name, board)
        
    def cleanupPage(self):
        pass        


    def onSelectionChanged(self, index):
        board = self._comboBoxBoard.itemData(index)
        if board:
            if board.img is not None:   
                self._labelBoardImage.setPixmap( QPixmap(board.img).scaled(self._labelBoardImage.minimumSize(),  Qt.KeepAspectRatio, Qt.SmoothTransformation) )
            else:
                self._labelBoardImage.clear()
        else:
            self._labelBoardImage.clear()


class QWizarpageSartupVariant(BaseWizardPage):
        
        
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._board = None
    
    def initializePage(self):
        BaseWizardPage.initializePage(self)
        board  = self.wizard().comboBoxBoard.itemData(self.field('board'))
        if self._board is board:
            return
        else:  
            self._board = board
            self.update()
        
        
    def cleanupPage(self):
        pass
        # self._comboBoxBoardVariant.setCurrentIndex(0)
        # self._comboBoxBoardVersion.setCurrentIndex(0)
        # BaseWizardpage.cleanupPage(self)
        
            
    def prepare(self):
        self._comboBoxBoardVariant = self.wizard().comboBoxBoardVariant    
        self._comboBoxBoardVersion = self.wizard().comboBoxBoardVersion
        self._labelBoardVariantImage = self.wizard().labelBoardVariantImage
        self._comboBoxBoardVariant.currentIndexChanged.connect(self.onSelectionChanged)
        self.registerField('board.variant*', self._comboBoxBoardVariant)
        self.registerField('board.version*', self._comboBoxBoardVersion)
        
        
    def update(self):
        if self._board is None:
            self._board = self.wizard().comboBoxBoard.itemData(self.field('board'))
        
        self._comboBoxBoardVariant.clear()
        self._comboBoxBoardVersion.clear()
        
        if self._board is None:
            self.setSubTitle(WizardProdStartup.tr(f"The board type has not been defined!"))
            return
        
        self.setSubTitle(WizardProdStartup.tr(f"Select a <b>{self._board.name}</b> board variant in list below."))
        
        for v in sorted(self._board.variants, key=lambda x:x.id):
            self._comboBoxBoardVariant.addItem(v.name, v)
        
        if self.field('board.variant') >= 0:
            self._comboBoxBoardVariant.setCurrentIndex(self.field('board.variant'))
        else:
            self._comboBoxBoardVariant.setCurrentIndex(-1)

        
        for v in self._board.vers:
            self._comboBoxBoardVersion.addItem(self.app().icon('OWE'[int(v.obsolete)]),  v.id, v)

        if self.field('board.version') >= 0:
            self._comboBoxBoardVersion.setCurrentIndex(self.field('board.version'))
        else:
            self._comboBoxBoardVersion.setCurrentIndex(0)

    def onSelectionChanged(self, index):
        variant = self._comboBoxBoardVariant.itemData(index)
        if variant:
            if variant.img is not None:   
                self._labelBoardVariantImage.setPixmap( QPixmap(variant.img).scaled(self._labelBoardVariantImage.minimumSize(),  Qt.KeepAspectRatio, Qt.SmoothTransformation) )
            else:
                self._labelBoardVariantImage.clear()
        else:
            self._labelBoardVariantImage.clear()


class QWizarpageSartupFirmware(BaseWizardPage):


    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._board_variant = None
        self._customer = None

    def initializePage(self):
        BaseWizardPage.initializePage(self)
        temp = (self.wizard().getBoardVariant(),self.wizard().getCustomer())
        if temp == (self._board_variant ,self._customer):
            return
        self._board_variant ,self._customer = temp
        del temp 
        self.setSubTitle(WizardProdStartup.tr(f"Select the <b>{self._board_variant.name}</b> firmware for <b>{self._customer.name}</b> in list below."))
        self.update()
        
    def update(self):
        self.wizard().comboBoxFirmware.clear()
        self.wizard().labelFirmwareDesc.clear()
        self.wizard().labelFirmwareIcon.clear()
        
        softs = self.db().firmwares.find(self._board_variant.board, self._customer)
        for soft in softs:
            self._comboBoxFirmware.addItem(
                    self.app().icon('OWE'[int(not soft.isLast()) + int(soft.obsolete)*2]),
                    f"{soft.name} V{dapi2.versionToStr(soft.version)} ({soft.date.isoformat()})",
                    soft)
        
    
    
    def prepare(self):
        self._comboBoxFirmware = self.wizard().comboBoxFirmware
        self._labelFirmwareDesc = self.wizard().labelFirmwareDesc
        self._comboBoxFirmware.currentIndexChanged.connect(self.onSelectionChanged)
        self.registerField('firmware*', self._comboBoxFirmware)

    
    def cleanupPage(self):
        pass
    
    
    def onSelectionChanged(self, index):
        firmware = self._comboBoxFirmware.itemData(index)
        if firmware:
            self._labelFirmwareDesc.setText(
                    f"""<i>file: </i>{firmware.fpath.name}<br/>
                    <i>version: </i>0x{dapi2.versionToStr(firmware.version)}  <i>date: </i>{firmware.date.isoformat()}  <i>tag: </i>0x{firmware.tag:04X}<br/>
                    <i>customer: </i>{firmware.customer.name}<br/>
                    """
                )
        else:
            self._labelFirmwareDesc.clear()


class QWizarpageSartupManufacturing(BaseWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._customer = None
        self._board_variant = None
        self._firmware = None
        
    def prepare(self):
        self.registerField('serial*', self.wizard().lineEditSerialNumber)
        self.registerField('order*', self.wizard().lineEditManufacturingOrder)

    def initializePage(self):
        self._board_variant = self.wizard().getBoardVariant()
        self._customer = self.wizard().getCustomer()
        self._firmware = self.wizard().getFirmware()   
        BaseWizardPage.initializePage(self)
        self.setSubTitle(WizardProdStartup.tr(f"Enter the manufacturing data of <b>{self._board_variant.name}</b> for <b>{self._customer.name}</b> in list bellow."))
        self.wizard().labelManufacturingFirmware.setText(str(self._firmware))
        
        
        
