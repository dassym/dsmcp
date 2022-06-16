'''

:author:  F. Voillat
:date: 2022-03-07 Creation
:copyright: Dassym SA 2021
'''


from PyQt5.Qt import QDialog
import dapi2

from app.base import BaseApp
import re as RE
import serialnumbers as SN

from ..base import BaseMainWindow, BaseQtApp
from ..dlg.wzd.prod import QWizardProdStartup
from .ui_prodwindow import Ui_ProdWindow


class ProdWindow(BaseMainWindow, Ui_ProdWindow):
    '''Class of main window for *basic* GUI application.
    
    :param BaseQtApp app: The application that owns the window
    ''' 
    def __init__(self, app, *args, **kwargs):
        '''Constructor'''
        BaseMainWindow.__init__(self, app, *args, **kwargs)
        Ui_ProdWindow.__init__(self, *args, **kwargs)
        
        self.setupUi(self)
        self._startup_wzd = None
    
    def _initWin(self):
        BaseMainWindow._initWin(self)
        
        self._startup_wzd = self._addDialog('startup', QWizardProdStartup(self))
        #TODO: Window initiaization


class ProdQtApp(BaseQtApp):
    '''Class for *basic* GUI application
    
    :param Namespace config: Application configuration
    '''
    NAME = 'dcp-prod'
    '''Application name'''

    # @classmethod
    # def tr(cls, text, disambiguation=None, n=-1):
    #     return QCoreApplication.translate('ProdQtApp',text, disambiguation, n)  

    def __init__(self, config):
        '''Constructor'''
        self._memoryActions = set([])
        super().__init__(config)
        self.last_factory_data = None
        self.serial_numbers = None
        self.manufacturing_order = None
        self.firmware = None
        self.customer = None
        
        
        
    def _initWin(self):
        self._window = ProdWindow(self) 
        self._window._initWin()
        
        
    def prepareSpecificCfg(self, parser):
        super().prepareSpecificCfg(parser)
        
        parser.add_argument("-B", "--board-type", dest="board_type", metavar="BOARD", type = str,
                    #choices=[x.getCode() for x in dapi2.getBoardTypes()],                    
                    help=self.tr("Sets the board type (ex.: MB-30-P."))
        
        parser.add_argument("-F", "--firmware", dest="firmware",
                    help=self.tr("Sets the firmware with which to program the board."))

        parser.add_argument("-O", "--order", dest="order",
                    help=self.tr("Sets the work order for this production."))

        parser.add_argument("-N", "--serial-number", dest="serial_numbers", nargs="*",
                    help=self.tr("Sets the range(s) of serial numbers associated with that production."))

        parser.add_argument("-C", "--customer", dest="customer",
                    help=self.tr("Sets the customer for which the boards to be produced are intended."))

        
    
    def processSpecificCfg(self):
        super().processSpecificCfg()        
        #self.config.access_level = DApiAccessLevel[self.config.access_level.upper()]
        self.autorefresh = self.config.autorefresh_on
        if self.config.firmware:
            if not self.config.board_type:
                raise Exception(self.tr('The `--firmware` argument requires the `--board-type` argument!'))
            
            m = RE.match(r"(.*)(:?V(\d+\.\d{2}))", self.config.firmware)
            if m is not None:
                self.config.firmware = {'name':m.group(1), 'version':m.group(2)}  
            else:
                self.config.firmware = {'name':self.config.firmware, 'version':None}
    
        
        
    # def getAvailableActions(self, context={}):
    #     ret = super().getAvailableActions(context)
    #     if self.board is not None: 
    #         if self.isConnected():
    #             #ret.add('actionAboutBoard')  
    #             ret.add('actionMotorMode')
    #             if self.board.isOnStandby():
    #                 ret.add('actionAPISendFirmware')
    #             if self.board.getAccessLevel() > DApiAccessLevel.NO:
    #                 ret |= self._memoryActions
    #     return ret        
        
        
    def environmentCtrl(self):
        BaseQtApp.environmentCtrl(self)
        if not self.testSerial(self.config.serial):
            raise Exception(BaseApp.tr('The configured serial port `{0!s}` is not available!'.format(self.config.serial)))
            
    
    def startUp(self):
        
        self.sayMedium(BaseApp.tr('Starting up the application.'))
        self.startupWizard.prepare()
        
        if self.startupWizard.exec() == QDialog.Accepted:
            self.firmware = self.startupWizard.getFirmware()
            self.customer =  self.startupWizard.getCustomer()
            
            self.setBoard(self.startupWizard.getBoardVariant().board.board_class(self.dapi))
            if self.startupWizard.getSerial() != '/':
                self.serial_numbers = SN.SerialNumberList(self.startupWizard.getSerial())
            if self.startupWizard.getOrder() != '/':
                self.manufacturing_order = self.startupWizard.getOrder()

            if self.serial_numbers:
                self.sayLow(BaseApp.tr(f"Manufacturing data: {len(self.serial_numbers)!s} × {self.board.name} SN:{self.serial_numbers!s}  programmed with `{self.firmware.name} v{dapi2.versionToStr(self.firmware.version)}` for {self.customer.name}" ))
            else:
                self.sayLow(BaseApp.tr(f"Manufacturing data: {self.board.name} programmed with `{self.firmware.name} v{dapi2.versionToStr(self.firmware.version)}` for {self.customer.name}" ))
        else:
            self.sayWarning(BaseApp.tr('Startup wizard aborted!'))
            self.terminate(1)
        
        
        
    def initialize(self):
        BaseQtApp.initialize(self)
        
        
        
        
    @property
    def startupWizard(self):
        return self._window._startup_wzd
        
