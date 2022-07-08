'''

:author:  F. Voillat
:date: 2022-06-15 Creation
:copyright: Dassym SA 2021
'''
import datetime as DT
from PyQt5.Qt import Qt, QPixmap, QDate
import dapi2

from app.db.partner import DbCustomer

from .base import WizardProdStartup, BaseWizardPage


class QWizarpageSartupCustomer(BaseWizardPage):
    

    def prepare(self):
        super().prepare()
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
    
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._customer = None
        
    def initializePage(self):
        BaseWizardPage.initializePage(self)
        temp = self.wizard().getCustomer()
        if self._customer is temp:
            return
        self._customer = temp
        self.update()
                
    def prepare(self):
        super().prepare()
        self._comboBoxBoard = self.wizard().comboBoxBoard
        self._labelBoardImage = self.wizard().labelBoardImage
        self._comboBoxBoard.currentIndexChanged.connect(self.onSelectionChanged)
        self.registerField('board*', self._comboBoxBoard)
        

    def update(self):
        assert self._customer is not None
        super().update()
        self._comboBoxBoard.clear()
        
        boards_ok, boards_nok = self.db().findBoards(self._customer) 
        
        for board in sorted(boards_ok,key=lambda x:x.id):
            self._comboBoxBoard.addItem(self.app().icon('O'), board.name, board)
        for board in sorted(boards_nok,key=lambda x:x.id):
            self._comboBoxBoard.addItem(self.app().icon('W'), board.name, board)
        if self._comboBoxBoard.count() == 0:
            raise ValueError(WizardProdStartup.tr("No board known for the client {}!",format(self._customer.name)))
        elif self.field('board') >= 0:
            self._comboBoxBoard.setCurrentIndex(self.field('board'))
        elif self._comboBoxBoard.count() == 1:
            self._comboBoxBoard.setCurrentIndex(0)
        else:
            self._comboBoxBoard.setCurrentIndex(-1)

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
        self._customer = None
        self._board = None
    
    def initializePage(self):
        BaseWizardPage.initializePage(self)
        temp = (self.wizard().getCustomer(), self.wizard().getBoard())
        if (self._customer, self._board) == temp:
            return 
        self._customer, self._board = temp
        self.update()
        
        
    def cleanupPage(self):
        pass
        # self._comboBoxBoardVariant.setCurrentIndex(-1)
        # self._comboBoxBoardVersion.setCurrentIndex(-1)
        # super().cleanupPage()
        
            
    def prepare(self):
        super().prepare()
        self._comboBoxBoardVariant = self.wizard().comboBoxBoardVariant    
        self._comboBoxBoardVersion = self.wizard().comboBoxBoardVersion
        self._labelBoardVariantImage = self.wizard().labelBoardVariantImage
        self._comboBoxBoardVariant.currentIndexChanged.connect(self.onSelectionChanged)
        self.registerField('board.variant*', self._comboBoxBoardVariant)
        self.registerField('board.version*', self._comboBoxBoardVersion)
        
        
    def update(self):
        assert self._customer is not None
        assert self._board is not None
        super().update()
        self._comboBoxBoardVariant.clear()
        self._comboBoxBoardVersion.clear()
        
        self.setSubTitle(WizardProdStartup.tr("Select a **{}** board variant for **{}** in list below.").format(self._board.name, self._customer.name))
        
        variants_ok, variants_nok = self._board.findVariants(self._customer)
        
        for v in sorted(variants_ok, key=lambda x:x.id):
            self._comboBoxBoardVariant.addItem(self.app().icon('O'), v.name, v)
        for v in sorted(variants_nok, key=lambda x:x.id):
            self._comboBoxBoardVariant.addItem(self.app().icon('W'), v.name, v)
                
        if self._comboBoxBoardVariant.count() == 0:
            raise ValueError(WizardProdStartup.tr("No board variant known for the client {}").format(self._customer.name))
        
        if self._comboBoxBoardVariant.count() == 1:
            self._comboBoxBoardVariant.setCurrentIndex(0)
        else:
            self._comboBoxBoardVariant.setCurrentIndex(-1)

        
        for v in self._board.vers:
            self._comboBoxBoardVersion.addItem(self.app().icon('OWE'[int(v.obsolete)]),  v.id, v)

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
        self.update()
        
    def update(self):
        super().update()
        assert self._customer is not None
        assert self._board_variant is not None
        self.setSubTitle(WizardProdStartup.tr("Select the **{}** firmware for **{}** in list below.").format(self._board_variant.name, self._customer.name))
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
        super().prepare()
        self._comboBoxFirmware = self.wizard().comboBoxFirmware
        self._labelFirmwareDesc = self.wizard().labelFirmwareDesc
        self._comboBoxFirmware.currentIndexChanged.connect(self.onSelectionChanged)
        self.registerField('firmware*', self._comboBoxFirmware)

    
    def cleanupPage(self):
        pass
    
    
    def onSelectionChanged(self, index):
        firmware = self._comboBoxFirmware.itemData(index)
        if firmware:
            self._labelFirmwareDesc.setText(firmware.getDescr('html'))
        else:
            self._labelFirmwareDesc.clear()


class QWizarpageSartupManufacturing(BaseWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._customer = None
        self._board_variant = None
        self._firmware = None
        self._date = None
        
    def prepare(self):
        super().prepare()
        self.registerField('serial*', self.wizard().lineEditSerialNumber)
        self.registerField('order*', self.wizard().lineEditManufacturingOrder)
        self.registerField('date', self.wizard().dateEditManufacturingDate)
        self.setField('date', QDate(DT.date.today()) )

    def initializePage(self):
        self._board_variant = self.wizard().getBoardVariant()
        self._customer = self.wizard().getCustomer()
        self._firmware = self.wizard().getFirmware()
        self._date = self.wizard().getDate()   
        BaseWizardPage.initializePage(self)
        self.setSubTitle(WizardProdStartup.tr("Enter the manufacturing data of **{}** for **{}** in list bellow.").format(self._board_variant.name, self._customer.name))
        self.wizard().labelManufacturingFirmware.setText(str(self._firmware))
        
        
        
