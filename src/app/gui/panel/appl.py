'''Definition of main window for *basic* GUI application.

:author: F. Voillat
:date: 2021-0-24 Creation
:copyright: Dassym 2021
'''

from PyQt5.Qt import QDialog
from dapi2 import DApiAccessLevel, DBoardPreferredDapiMode
from functools import partial

from app.base import BaseApp

from ..base import BaseMainWindow, BaseQtApp, UserActionHandler, UserBoardActionHandler
from ..common import DisableEvent
from ..dlg import AboutBoardDialog, FlashProgressDialog, MotorModeDialog, SendFirmwareDialog
from ..widget.qsvgpanel import ReverseKey, LightKey, IncrementKey, DecrementKey, MemoryKey, GearKey, \
    ParametersKey, WorkspaceKey, WorkspaceToggleKey
from .ui_panelwindow import Ui_PanelWindow


class PanelWindow(BaseMainWindow, Ui_PanelWindow):
    '''Class of main window for *basic* GUI application.
    
    :param BaseQtApp app: The application that owns the window
    ''' 
    def __init__(self, app, *args, **kwargs):
        '''Constructor'''
        BaseMainWindow.__init__(self, app, *args, **kwargs)
        Ui_PanelWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
    
    def _initWin(self):
        BaseMainWindow._initWin(self)
        
        self.pushButtonStart.setAction(self.actionMotorStart)
        self.actionMotorStart.triggered.connect(self.doMotorStart)
        self.pushButtonStop.setAction(self.actionMotorStop)
        self.actionMotorStop.triggered.connect(self.doMotorStop)
        self.actionLightEnabled.triggered.connect(self.doLightEnable)
        self.actionLightBlue.triggered.connect(self.doLightAlternate)
        self.actionMotorReverse.triggered.connect(self.doMotorReverse)
        self.actionAboutBoard.triggered.connect(self.doAboutBoard)
        self.actionAPISendFirmware.triggered.connect(self.doSendFirmware)
        self.actionMotorMode.triggered.connect(self.doShowMotorMode)
        
        
        self._addDialog('aboutboard', AboutBoardDialog(self))
        self._addDialog('motormode', MotorModeDialog(self))
        
        
        self.frameError.setLang(self.app.lang)
        
        self.graphicsViewPanel.setSvg(self.app.getLayoutFile(self.app.config.layout))
        
        for key in self.graphicsViewPanel.keys:
            if isinstance(key, ReverseKey):
                key.pressShort.connect(self.doMotorReverse)
            elif isinstance(key, LightKey):
                key.pressShort.connect(self.doLightToggle)
                key.pressLong.connect(self.doLightAlternateToggle)
            elif isinstance(key, IncrementKey):
                key.pressShort.connect(self.doSpeedInc)
            elif isinstance(key, DecrementKey):
                key.pressShort.connect(self.doSpeedDec)
            elif isinstance(key, MemoryKey):
                key.pressShort.connect(partial(self.doRecallMem, key.num))
                key.pressLong.connect(partial(self.doStoreMem, key.num))
            elif isinstance(key, GearKey):
                key.pressShort.connect(partial(self.doSelectGear, key.numerator, key.denominator))
            elif isinstance(key, ParametersKey):
                key.pressShort.connect(self.doParameters)
            elif isinstance(key, WorkspaceToggleKey):
                key.pressShort.connect(partial(self.doWorkspaceToggle, key.num))
            elif isinstance(key, WorkspaceKey):
                key.pressShort.connect(partial(self.doWorkspace, key.num))
                
                
    def saveGeometries(self, settings):
        '''Saves the geometries of this window and its children windows
        
        :param settings: the data container.
        ''' 
        super().saveGeometries(settings)
        settings.beginGroup("Dialogs")
        for n, d in self.dialogs.items(): 
            settings.setValue(n+".geometry", d.saveGeometry())
            #settings.setValue(dlg.objectName()+".state", dlg.saveState())
        settings.endGroup()
        
    def restoreGeometries(self, settings):
        '''Restores the geometries of this window and its children windows
        
        :param settings: the data container.
        ''' 
        super().restoreGeometries(settings)
        settings.beginGroup("Dialogs")
        for n, d in self.dialogs.items():
            d.restoreGeometry(settings.value(n+".geometry"))
            #dlg.restoreState(settings.value(dlg.objectName()+"state"))
        settings.endGroup()
        
    def initialize(self):
        '''Initialize the window'''
        super().initialize()
        if self.board:
            self.frameError.setReg(self.board.regs.wer, self.board.dapi)
            self.widgetSpeed.setBoard(self.board)
            self.graphicsViewPanel.setBoard(self.board)
        
        
    @DisableEvent
    def refresh(self):
        '''Refresh the windows according board setpoints'''
        super().refresh()
        
        def formatSpeed(speed):
            if speed >= 10:
                d = '0'
            elif speed >= 1:
                d = '1'
            else:
                d = '2'
            return ("{0:0."+d+"f}").format(speed)
            
    
        self.actionLightEnabled.setChecked(self.board.isLightEnabled())
        self.actionLightBlue.setChecked(self.board.isLightAlternate())
        self.actionMotorReverse.setChecked(self.board.isMotorReverse())
        
        
        if self.board.isOnStandby():
                #self.label.setText('Standby')
                self.graphicsViewPanel.setDisplayText('---')
        else:
            if self.board.isMotorRunning():
                speed = self.board.motorRealSpeed()
                self.graphicsViewPanel.setDisplayText(formatSpeed(speed/1000))
                #self.label.setText('Running:{0:d}'.format(speed))
            else:
                speed = self.board.motorSpeed()
                self.graphicsViewPanel.setDisplayText(formatSpeed(speed/1000))
                #self.label.setText('Stopped:{0:d}'.format(speed))
            
        self.graphicsViewPanel.initialize()    
        self.graphicsViewPanel.refresh()
        
        
    @UserBoardActionHandler
    def doMotorStart(self, checked=None):
        '''Handler for  *motor start* action'''
        self.board.motorStart()
                
    @UserBoardActionHandler
    def doMotorStop(self, checked=None):
        '''Handler for  *motor stop* action'''
        self.board.motorStop()

    @UserBoardActionHandler
    def doMotorReverse(self, checked=None):
        '''Handler for  *motor reverse* action'''
        self.board.motorReverse()
            
    
    def doLightToggle(self):
        self.doLightEnable(not self.board.isLightEnabled())
            
    @UserBoardActionHandler
    def doLightEnable(self, checked=None):
        '''Handler for  *light enable* action'''
        self.board.lightOn(checked)
            
    @UserBoardActionHandler
    def doSpeedInc(self):
        if self.board.motorSpeed() <= 2000:
            i = 100
        elif self.board.motorSpeed() < 10000:
            i = 1000
        else:
            i = 2000
        self.board.motorIncSpeed(i)
        
    @UserBoardActionHandler
    def doParameters(self):
        if self.dialogs['motormode'].isVisible():
            self.dialogs['motormode'].hide()
        else:
            self.dialogs['motormode'].show()
        
            
    @UserBoardActionHandler
    def doSpeedDec(self):
        if self.board.motorSpeed() <= 2000:
            i = 100
        elif self.board.motorSpeed() <= 10000:
            i = 1000
        else:
            i = 2000
        self.board.motorDecSpeed(i)
        
            
    @UserBoardActionHandler
    def doStoreMem(self, num):
        '''Handler for  *store memory* action'''
        self.board.memoryStore(num)
                 

    @UserBoardActionHandler
    def doWorkspace(self, num):
        '''Handler for  *Worspace* action'''
        self.app.board.setWorkspace(num)

    @UserBoardActionHandler
    def doWorkspaceToggle(self, num):
        '''Handler for  *Toggle Worspace* action'''
        if self.app.board.getWorkspace().standby:
            self.app.board.setWorkspace(num)
        else:
            self.app.board.setWorkspace(0)
            
            
    @UserBoardActionHandler
    def doRecallMem(self, num):
        '''Handler for  *recall memory* action'''
        self.board.memoryRecall(num)
        self.board.getRegisters('setpoints')
            
    @UserBoardActionHandler
    def doSelectGear(self, num, den):
        '''Handler for  *select gear ratio* action'''
        self.board.setGearRatio(num, den)

    def doLightAlternateToggle(self):
        '''Handler for  *toggle kind of light* action'''
        self.doLightAlternate(not self.board.isLightAlternate())

    @UserBoardActionHandler
    def doLightAlternate(self, checked=None):
        '''Handler for  *light alternate selection* action'''
        self.board.lightAlternate(checked)
            
    @UserActionHandler
    def doAboutBoard(self, checked=None):
        '''Handler for  *about board* action'''
        self._dialogs['aboutboard'].exec()


    @UserActionHandler
    def doShowMotorMode(self, checked=None):
        '''Handler for  *Show motor mode dialog* action'''
        self.dialogs['motormode'].show()

    @UserBoardActionHandler
    def doSendFirmware(self, checked=None):
        '''Handler for  *send firmware* action'''
        dlg = SendFirmwareDialog(self)
        if dlg.exec() == QDialog.Accepted:
            temp = (self.app.autorefresh, self.app.board.getAccessLevel())
            self.app.autorefresh = False
            self.app.board.connect(DApiAccessLevel.SERVICE, DApiAccessLevel.SERVICE.passwd ) #@UndefinedVariable
            firmware = dlg.getFirmware()
            self.log.info('Firmware programming `{0!s}` '.format(firmware))
            self._flasProgressDialog = FlashProgressDialog(self,firmware)
            self._flasProgressDialog.show()
            self.app.processEvents()
            self.board.flashFirm(dlg.getFirmware(), self._flasProgressDialog.progress)
            self._flasProgressDialog.hide()
            del self._flasProgressDialog
            self.log.info('wait before reconnection ({}s)'.format(self.app.board.wait_after_reprogramming))
            self.app.sleep(self.app.board.wait_after_reprogramming)
            
            self.app.board.connect(temp[1], temp[1].passwd )
            self.app.autorefresh = temp[0]
        self.update()
    

class PanelQtApp(BaseQtApp):
    '''Class for *panel* GUI application
    
    :param Namespace config: Application configuration
    '''
    NAME = 'dcp-panel-gui'
    '''Application name'''

    def __init__(self, config):
        '''Constructor'''
        BaseQtApp.__init__(self, config)
        
        
    def _initWin(self):
        self._window = PanelWindow(self) 
        self._window._initWin()
        
        
    def prepareSpecificCfg(self, parser):
        parser.add_argument("--layout",  help=BaseApp.tr("The GUI layout name or SVG file. (default: vantage)"), dest="layout", default="vantage")
        autorefresh_grp = parser.add_mutually_exclusive_group()
        autorefresh_grp.add_argument("--autorefresh-off", dest="autorefresh_on", action="store_false", default=True, help=BaseApp.tr("Disables auto refresh on start up."))
        autorefresh_grp.add_argument("--autorefresh-on", dest="autorefresh_on", action="store_true", default=True, help=BaseApp.tr("Enables auto refresh on start up."))
         
    
    def processSpecificCfg(self):
        self.autorefresh = self.config.autorefresh_on       
        
        
    def getAvailableActions(self, context={}):
        ret = super().getAvailableActions(context)
        if self._board is not None: 
            if self.isConnected():
                #ret.add('actionAboutBoard')  
                ret.add('actionMotorMode')
                if self._board.isOnStandby():
                    ret.add('actionAPISendFirmware')
        return ret        
        
    def initialize(self):
        BaseQtApp.initialize(self)
        if self.board and self.board.dmode == DBoardPreferredDapiMode.COMMAND and not self.dapi.dev_mode:
            self.board.connect()
            

#        if self.board.isOnStandby():
#            self.board.setWorkspace(1)
        
         
    
        
        
        
        
