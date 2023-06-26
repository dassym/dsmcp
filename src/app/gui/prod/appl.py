'''Implementation of the 'prod' application.

:author:  F. Voillat
:date: 2022-03-07 Creation
:copyright: Dassym SA 2022
'''


from PyQt5.Qt import QDialog, QPixmap, Qt
import dapi2
import datetime as DT

from app.base import BaseApp
import re as RE
import serialnumbers as SN

from ..base import BaseMainWindow, BaseQtApp
from ..dlg.wzd.prod import QWizardProdStartup
from .ui_prodwindow import Ui_ProdWindow
from app.gui.common import UserActionHandler


class ProdWindow(BaseMainWindow, Ui_ProdWindow):
    '''Class of main window for *prod* GUI application.

    Args:
        app (BaseQtApp): The application that owns the window
    '''
    def __init__(self, app, *args, **kwargs):
        '''Constructor'''
        BaseMainWindow.__init__(self, app, *args, **kwargs)
        Ui_ProdWindow.__init__(self, *args, **kwargs)

        self.setupUi(self)
        self._startup_wzd = None

        self.actionWriteFirmware.triggered.connect(self.doWriteFirmware)
        self.pushButtonWriteFirmware.setAction(self.actionWriteFirmware)
        self.pushButtonFirmReset.setAction(self.actionFirmReset)

    def _initWin(self):
        BaseMainWindow._initWin(self)

        self._startup_wzd = self._addDialog('startup', QWizardProdStartup(self))
        #TODO: Window initiaization

    def initialize(self):
        super().initialize()
        self.log.debug('Initialize ProdWindow...')

        self.labelPrgBoard.setText(self.app.board_variant.name)
        self.labelPrgFirmware.setText(f"{self.app.firmware.name} V{'{0:d}.{1:02d}'.format(*self.app.firmware.version)}")
        self.labelPrgFirmwareDesc.setText(self.app.firmware.getDescr('html'))
        self.labelPrgBoardImage.setPixmap(
            QPixmap(self.app.board_variant.img).scaled(self.labelPrgBoardImage.minimumSize(),
                            Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        self.labelPrgCustomer.setText(self.app.customer.name)
        self.labelPrgCustomerImage.setPixmap(
            QPixmap(str(self.app.customer.logo)).scaled(self.labelPrgCustomerImage.minimumSize(),
                            Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
        s = []
        if self.app.manufacturing_order is not None:
            s.append( f"Order: <big>{self.app.manufacturing_order}</big>" )
        if self.app.serial_numbers:
            s.append( f"SN: <big>{self.app.serial_numbers!s}</big> ({len(self.app.serial_numbers):d})" )
            self.progressBarPrg.setMaximum(len(self.app.serial_numbers))
            self.progressBarPrg.setValue(0)
        else:
            self.progressBarPrg.hide()


        self.labelPrgData.setText(' — '.join(s))

    @UserActionHandler
    def doWriteFirmware(self, checked=None):
        pass



class ProdQtApp(BaseQtApp):
    '''Class for *prod* GUI application

    Args:
        app_dir (str): Application root directory
        lang (str): If defined the language to use, otherwise the local session language.
    '''
    NAME = 'dcp-prod'
    '''Application name'''

    DEFAULT_ACCESS_LEVEL = dapi2.DApiAccessLevel.FACTORY

    # @classmethod
    # def tr(cls, text, disambiguation=None, n=-1):
    #     return QCoreApplication.translate('ProdQtApp',text, disambiguation, n)

    def __init__(self, app_dir, lang):
        '''Constructor'''
        self._memoryActions = set([])
        super().__init__(app_dir, lang)
        self.last_factory_data = None
        self.serial_numbers = None
        self.manufacturing_order = None
        self.board_variant = None
        self.firmware = None
        self.customer = None
        self.configuration = None



    def _initWin(self):
        self._window = ProdWindow(self)
        self._window._initWin()


    def prepareSpecificCfg(self, parser):
        '''Prepares specific configuration arguments

        Args:
            parser (ArgumentParser): Parser to which must be added the arguments
        '''
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

        parser.add_argument("-MD", "--manufacturing-date", dest="date",
                    help=self.tr("Sets the manufacturing date for this production. Format : YYYY-MM-DD, according ISO-8601 (default: today)."))


    def processSpecificCfg(self):
        '''Processing of specific configuration arguments'''
        super().processSpecificCfg()
        #self.config.access_level = DApiAccessLevel[self.config.access_level.upper()]
        self._autorefresh = self.config.autorefresh_on

        if self.config.date:
            try:
                self.config.date = DT.datetime.strptime(self.config.date, '%Y-%m-%d').date()
            except ValueError:
                raise Exception(self.tr('The argument `--date` cannot be converted to a date according "YYYY-MM-DD" format!'))

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


    def environmentCheck(self):
        '''Checking the application environment'''
        BaseQtApp.environmentCheck(self)
        if not self.testSerial(self.config.serial):
            raise Exception(BaseApp.tr('The configured serial port `{0!s}` is not available!'.format(self.config.serial)))

        if self.db.isEmpty():
            raise Exception(BaseApp.tr('The database is empty!'))

        if self.db.standard_cust is None:
            raise Exception(BaseApp.tr('The standard/default customer is not defined!'))


    def startUp(self):
        '''Starting up the application.'''
        super().startUp()
        self.log.debug('Startup ProdQtApp ...')
        self.sayMedium(BaseApp.tr('Launch of the start-up wizard...'))
        self.startupWizard.prepare()

        if self.startupWizard.exec() == QDialog.Accepted:
            self.firmware = self.startupWizard.getFirmware()
            self.customer =  self.startupWizard.getCustomer()
            self.board_variant = self.startupWizard.getBoardVariant()
            self.date = self.startupWizard.getDate()
            if self.startupWizard.getSerial() != '/':
                self.serial_numbers = SN.SerialNumberList(self.startupWizard.getSerial())
            if self.startupWizard.getOrder() != '/':
                self.manufacturing_order = self.startupWizard.getOrder()

            del self._window._startup_wzd
            print(self.date)
        else:
            self.sayWarning(BaseApp.tr('Startup wizard aborted!'))
            self.terminate(1)



    def initialize(self):
        '''Initialize the application.'''
        self.setBoard(self.board_variant.board.board_class(self.dapi))
        BaseQtApp.initialize(self)
        self.log.debug('Initialize application '+self.NAME)


        if self.serial_numbers:
            self.sayLow(BaseApp.tr(f"Manufacturing data {self.manufacturing_order or ''}:  {len(self.serial_numbers)!s} × {self.board_variant.name} SN:{self.serial_numbers!s}  programmed with `{self.firmware.name} v{dapi2.versionToStr(self.firmware.version)}` for {self.customer.name}" ))
        else:
            self.sayLow(BaseApp.tr(f"Manufacturing data {self.manufacturing_order or ''}: {self.board_variant.name} programmed with `{self.firmware.name} v{dapi2.versionToStr(self.firmware.version)}` for {self.customer.name}" ))




    def run(self):
        '''Executes application'''
        self.closeSplashScreen()
        self.sayLow(BaseApp.tr('Run')+" "+self.NAME+"...")
        self.log.debug('Show main window...')
        self._window.show()

        self.startTimer()
        self.log.debug('Start Qt main loop...')
        exit_code = self.exec()
        self.log.debug('Exit from Qt main loop...')
        self.saveUserConfig()
        self._window.finalize()
        self.stopTimer()
        del self._window
        return self.terminate(exit_code)

    @property
    def startupWizard(self):
        return self._window._startup_wzd

