'''

:author: fv
:date: Created on 24 mars 2021
'''
from PyQt5.Qt import QDialog, QMessageBox, Qt
import dapi2
from functools import partial

from app.base import BaseApp

from ..base import BaseQtApp, BaseMainWindow, UserBoardActionHandler, UserActionHandler
from ..common import DisableEvent
from ..dlg import AboutBoardDialog, FlashProgressDialog, MotorModeDialog, SendFirmwareDialog
from ..widget import QAnalogInput, QDebugValue
from .ui_devwindow import Ui_DevWindow



class DevWindow(BaseMainWindow, Ui_DevWindow):
    '''Class of main window for *basic* GUI application.
    
    :param BaseQtApp app: The application that owns the window
    ''' 
    def __init__(self, app, *args, **kwargs):
        '''Constructor'''
        BaseMainWindow.__init__(self, app, *args, **kwargs)
        Ui_DevWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        
    def _initWin(self):
        BaseMainWindow._initWin(self)     
        self._addDialog('aboutboard', AboutBoardDialog(self))
        self._addDialog('motormode', MotorModeDialog(self))
        
        self.pushButtonStart.setAction(self.actionMotorStart)
        self.actionMotorStart.triggered.connect(self.doMotorStart)
        self.pushButtonStop.setAction(self.actionMotorStop)
        self.actionMotorStop.triggered.connect(self.doMotorStop)
        self.actionLightEnabled.triggered.connect(self.doLightEnable)
        self.actionLightBlue.triggered.connect(self.doLightAlternate)
        self.actionMotorReverse.triggered.connect(self.doMotorReverse)
        self.actionAboutBoard.triggered.connect(self.doAboutBoard)
        self.actionAPISendFirmware.triggered.connect(self.doSendFirmware)
        self.actionFirmReset.triggered.connect(self.doFirmReset)
        self.actionMotorMode.triggered.connect(self.doShowMotorMode)
        self.actionRefreshDebug.triggered.connect(self.doRefreshDebug)
        self.actionRefreshAnalogInputs.triggered.connect(self.doRefreshAnalogInputs)
        self.pushButtonRefreshDebug.setAction(self.actionRefreshDebug)
        

        self.comboBoxDebugDac0.currentIndexChanged.connect(partial(self.doChangeDac, 0) )
        self.comboBoxDebugDac1.currentIndexChanged.connect(partial(self.doChangeDac, 1) )        
                
        self.frameBoardError.setLang(self.app.lang)   
        
        self.widgetSpeed.changed.connect(self.doSetSpeed)
        self.widgetTorque.changed.connect(self.doSetTorque)
        
        
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
    
    @DisableEvent    
    def initialize(self):
        '''Initialize the window'''
        super().initialize()
                
            
    @DisableEvent            
    def boardInit(self):
        super().boardInit()
        self.frameBoardError.setReg(self.board.regs.wer, self.board)
        self.widgetSpeed.setBoard(self.board)
        self.widgetTorque.setBoard(self.board)
        self.frameSystemMode.setBoard(self.board)
        
        self.frameBoardStatus1.setReg(self.board.regs.ssr1)
        self.frameBoardStatus2.setReg(self.board.regs.ssr2)
        
        for w in self.findChildren(QAnalogInput):
            w.setParent(None)
        for ai in self.board.analogInputs:
            w = QAnalogInput(self, ai, ai.name)
            self.groupBoxAnalogInputs.layout().addWidget(w)
            
        self.comboBoxDebugDac0.clear()
        for sig in self.board.DAC_SIGNAL: 
            t = "{0:2d}:{1:s}".format(sig.value, sig.name)
            self.comboBoxDebugDac0.addItem(t, sig)
            self.comboBoxDebugDac1.addItem(t, sig)
        
        for w in self.findChildren(QDebugValue):
            w.setParent(None)
        for i, dv in enumerate(self.board.debugValues):
            qdv = QDebugValue(self, dv)
            self.groupBoxDebugValues.layout().addWidget(qdv, i // 2 , i % 2  )
            qdv.update()
        for i, dv in enumerate(self.board.debugSettingValues):
            qdv = QDebugValue(self, dv)
            self.groupBoxDebugSettingValues.layout().addWidget(qdv, i // 2 , i % 2  )
            qdv.update()
            
            
        if self.board.getAdditionalBoard() in [dapi2.DApiAdditionalBoard.AB14,dapi2.DApiAdditionalBoard.AB0314, dapi2.DApiAdditionalBoard.AB1214]:
            self.dipswitch_ab14.setVisible(True) 
            self.dipswitch_ab14.setReg(self.board.regs.cfg0, shift=0)
        else:
            self.dipswitch_ab14.setVisible(False)
            
        self.statusBar.showMessage(f"Nb QAnalogInput = {len(self.findChildren(QAnalogInput))}")
        
    @DisableEvent
    def refresh(self):
        if self.board is not None:
            self.frameBoardError.refresh()
            self.tabWidget.setEnabled(self.app.dcom.isOpen())
            self.actionLightEnabled.setChecked(self.board.isLightEnabled())
            self.actionLightBlue.setChecked(self.board.isLightAlternate())
            self.actionMotorReverse.setChecked(self.board.isMotorReverse())
            
        else:
            self.tabWidget.setEnabled(False)
        BaseMainWindow.refresh(self)
            
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
    def doSetSpeed(self, speed):
        self.board.setMotorSpeed(speed)

    @UserBoardActionHandler
    def doSetTorque(self, torque):
        self.board.setMotorCurrent(torque)            
            
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
        #self._dialogs['aboutboard'].setBoard(self.board)
        dlg = self._dialogs['aboutboard']
        if dlg.exec() == QDialog.Accepted:
            try:
                sn, fd =  dlg.sn, dlg.fd
            except Exception as e:
                self.app.displayError(e)
            self.app.board.setFactoryData(sn, fd)
            

    @UserActionHandler
    def doShowMotorMode(self, checked=None):
        '''Handler for  *Show motor mode dialog* action'''
        self.dialogs['motormode'].show()
        
    @UserBoardActionHandler
    def doRefreshDebug(self, checked=None):
        '''Handler for  *Refresh debug* action'''
        self.app.board.refreshDebug()

    @UserBoardActionHandler
    def doRefreshAnalogInputs(self, checked=None):
        '''Handler for  *Refresh analog inputs* action'''
        self.app.board.refreshAnalogInputs()


    @UserBoardActionHandler
    def doSendFirmware(self, checked=None):
        '''Handler for  *send firmware* action'''
        dlg = SendFirmwareDialog(self)
        if dlg.exec() == QDialog.Accepted:
            temp = (self.app._autorefresh, self.app.board.getAccessLevel())
            self.app._autorefresh = False
            self.app.board.connect(dapi2.DApiAccessLevel.SERVICE, dapi2.DApiAccessLevel.SERVICE.passwd ) #@UndefinedVariable
            firmware = dlg.getFirmware()
            self.log.info('Firmware programming `{0!s}` '.format(firmware))
            self._flasProgressDialog = FlashProgressDialog(self,firmware)
            self._flasProgressDialog.show()
            self.app.processEvents()
            with open( dlg.getFirmware().fpath, 'rb' ) as f:
                self.board.flashBinaryFirm(f, self._flasProgressDialog.progress)
            self._flasProgressDialog.hide()
            del self._flasProgressDialog
            self.log.info('Wait before reconnection ({}s)'.format(self.app.board.wait_after_reprogramming))
            self.app.sleep(self.app.board.wait_after_reprogramming)
            
            self.app.board.connect(temp[1], temp[1].passwd )
            self.app._autorefresh = temp[0]
            
    @UserBoardActionHandler
    def doFirmReset(self, checked=None):
        '''Handler for  *Firmware Reset* action'''
        temp = (self.app._autorefresh, self.app.board.getAccessLevel())
        self.app._autorefresh = False
        if QMessageBox.question(self, self.app.name,
                                BaseApp.tr("Are you sure you want to replace the current settings with the firmware settings?")
                                ) == QMessageBox.Yes :
            
            self.app.board.eepromReset()
            self.log.info('Wait before reconnection ({}s)'.format(self.app.board.wait_after_reprogramming))
            self.app.sleep(self.app.board.wait_after_reprogramming)
            
            self.app.board.connect(temp[1], temp[1].passwd )
            self.app._autorefresh = temp[0]
            
    @UserBoardActionHandler
    def doChangeDac(self, dac, index):
        '''Handler for  *Debug DAC selection change* action'''
        
        signal = self.comboBoxDebugDac0.model().data(self.comboBoxDebugDac0.model().index(index,0), Qt.UserRole)
        self.board.setDacSignal(dapi2.DacChannel(dac), signal)
            

        
class DevQtApp(BaseQtApp):
    '''Class for *development* GUI application
    
    
    Args:
        app_dir (str): Application root directory
        lang (str): If defined the language to use, otherwise the local session language.
    '''
    NAME = 'dcp-dev'
    
    DEFAULT_ACCESS_LEVEL = dapi2.DApiAccessLevel.FACTORY

    def __init__(self, app_dir, lang):
        '''Constructor'''
        super().__init__(app_dir, lang)
        
    def _initWin(self):
        self._window = DevWindow(self) 
        self._window._initWin()        
        
    def _refresh(self):        
        if self._board is not None and self.isConnected():
            if not self._dcom.isOk(): return
            self._board.refreshHeader() 
            self._board.refreshState()
            self._board.refreshSetpoints()    
            self._board.refreshDebug()
    
    # def prepareSpecificCfg(self, parser):
    #     super().prepareSpecificCfg(parser)
    #     #parser.add_argument("-A", "--access-level", dest="access_level", choices=[x.name.lower() for x in DApiAccessLevel],  help=BaseApp.tr("Sets access level'. (Default=factory)"), default=DApiAccessLevel.FACTORY.name)
    #     autorefresh_grp = parser.add_mutually_exclusive_group()
    #     autorefresh_grp.add_argument("--_autorefresh-off", dest="autorefresh_on", action="store_false", default=False, help=BaseApp.tr("Disables auto refresh on start up."))
    #     autorefresh_grp.add_argument("--_autorefresh-on", dest="autorefresh_on", action="store_true", default=False, help=BaseApp.tr("Enables auto refresh on start up."))
    #
    # def processSpecificCfg(self):
    #     super().processSpecificCfg()        
    #     #self.config.access_level = DApiAccessLevel[self.config.access_level.upper()]
    #     self._autorefresh = self.config.autorefresh_on       
    #

        
    def initialize(self):
        BaseQtApp.initialize(self)
        if self.board and self.board.dmode == dapi2.DBoardPreferredDapiMode.COMMAND:
            if self.board.getAccessLevel() == dapi2.DApiAccessLevel.NO: 
                self.board.connect(DApiAccessLevel.FACTORY, DApiAccessLevel.FACTORY.passwd ) #@UndefinedVariable
        
    def getAvailableActions(self, context={}):
        ret = super().getAvailableActions(context)
        if self._board is not None: 
            if self.isConnected():
                #ret.add('actionAboutBoard')  
                ret.add('actionMotorMode')
                ret.add('actionRefreshDebug')
                ret.add('actionRefreshAnalogInputs')
                if self._board.isOnStandby():
                    ret.add('actionAPISendFirmware')
                    ret.add('actionFirmReset')
                    
        return ret             
    
        