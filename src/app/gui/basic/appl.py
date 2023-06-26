'''Definition of main window for *basic* GUI application.

:author: F. Voillat
:date: 2021-11-03 Creation
:copyright: Dassym 2021
'''

from PyQt5.Qt import QDialog, QPixmap, QIcon, QMessageBox
import dapi2

from ..base import BaseMainWindow, BaseQtApp, UserActionHandler, UserBoardActionHandler
from ..common import DisableEvent
from ..dlg import AboutBoardDialog, FlashProgressDialog, MotorModeDialog, \
        SendFirmwareDialog
from ..widget import QRegBitAction, QRegBitNegAction
from .ui_basicwindow import Ui_BasicWindow


class BasicWindow(BaseMainWindow, Ui_BasicWindow):
    '''Class of main window for *basic* GUI application.
    
    :param BaseQtApp app: The application that owns the window
    ''' 
    def __init__(self, app, *args, **kwargs):
        '''Constructor'''
        BaseMainWindow.__init__(self, app, *args, **kwargs)
        Ui_BasicWindow.__init__(self, *args, **kwargs)
        
        self.setupUi(self)
        
    
    def _initWin(self):
        BaseMainWindow._initWin(self)

        self.actionAboutBoard.triggered.connect(self.doAboutBoard)
        self.actionRebootBoard.triggered.connect(self.doRebootBoard)
        self.actionAPISendFirmware.triggered.connect(self.doSendFirmware)
        
        #self.pushButtonStart.setAction(self.actionMotorStart)
        
        QRegBitNegAction.cast(self.actionMotorStart)
        
        self.actionMotorStart.triggered.connect(self.doMotorStart)
        #self.pushButtonStop.setAction(self.actionMotorStop)
        
        QRegBitAction.cast(self.actionMotorStop) 
        
        self.actionMotorStop.triggered.connect(self.doMotorStop)
        self.actionMotorReverse.triggered.connect(self.doMotorReverse)
        self.actionMotorMode.triggered.connect(self.doShowMotorMode)
        self.actionLightEnabled.triggered.connect(self.doLightEnable)
        self.actionLightBlue.triggered.connect(self.doLightAlternate)
        self.actionFirmReset.triggered.connect(self.doResetFirmware)
        
        
        self._addDialog('aboutboard', AboutBoardDialog(self))
        self._addDialog('motormode', MotorModeDialog(self))
        
        
        self.frameError.setLang(self.app.lang)
        self.groupBoxMemories.setLang(self.app.lang)
        iconSet = QIcon(QPixmap(':img/24/memory-set.png'))
        iconGet = QIcon(QPixmap(':img/24/memory-get.png'))
        
        self.widgetSpeed.changed.connect(self.doSetSpeed)
        self.widgetTorque.changed.connect(self.doSetTorque)
        
        for m in self.groupBoxMemories:
            nSet = 'actionMemoryStore{0:d}'.format(m.number)
            nGet = 'actionMemoryRecall{0:d}'.format(m.number)
            aSet = self._addAction(self, name=nSet, label="Store "+m.caption, data=m.number, icon=iconSet, handler=self.doMemoryStore, tooltips=None, menu=self.menuMemory)
            aGet = self._addAction(self, name=nGet, label="Recall "+m.caption, data=m.number, icon=iconGet, handler=self.doMemoryRecall, tooltips=None, menu=self.menuMemory)
            m.setStoreAction(aSet)
            m.setRecallAction(aGet)
            self.app.memoryActions.update([nGet, nSet])
             
        
        # self.groupBoxMomories.memoryStore.connect(self.doMemoryStore)
        # self.groupBoxMomories.memoryRecall.connect(self.doMemoryRecall)
        
                
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
            
    def boardInit(self):
        super().boardInit()
        self.frameError.setReg(self.board.regs.wer, self.board)
        self.widgetSpeed.setBoard(self.board)
        self.widgetTorque.setBoard(self.board)
        self.groupBoxMemories.setBoard(self.board)
        
        self.actionMotorStart.setBit(self.board.regs.smr.bits.start, self.board)
        self.actionMotorStop.setBit(self.board.regs.smr.bits.start, self.board)
        
        
    def onWorkspaceChanged(self, workspace):
        super().onWorkspaceChanged(workspace)
        
        
    @DisableEvent
    def refresh(self):
        '''Refresh the windows according board setpoints'''
        super().refresh()
        if self.board is None: return
        
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
            pass
                #self.label.setText('Standby')
                ##self.graphicsViewPanel.setDisplayText('---')
            self.groupBoxMemories.setEnabled(False)
        else:
            # if self.board.isMotorRunning():
            #     speed = self.board.motorRealSpeed()
            #     ##self.graphicsViewPanel.setDisplayText(formatSpeed(speed/1000))
            #     #self.label.setText('Running:{0:d}'.format(speed))
            # else:
            #     speed = self.board.motorSpeed()
            #     ##self.graphicsViewPanel.setDisplayText(formatSpeed(speed/1000))
            #     #self.label.setText('Stopped:{0:d}'.format(speed))
            if self.board.getAccessLevel() >= dapi2.DApiAccessLevel.USER:
                self.groupBoxMemories.setEnabled(True)
                self.log.debug('self.groupBoxMemories.refresh()')
                self.groupBoxMemories.refresh()
        
        
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

    @UserBoardActionHandler
    def doRebootBoard(self, checked=None):
        '''Handler for *board reset* action'''
        temp = (self.app._autorefresh, self.board.getAccessLevel())
        self.board.reboot()
        delay = self.board.wait_after_reboot
        self.app.stopComm()
        self.log.info('Wait before reconnection ({}s)'.format(delay))
        self.app.sleep(delay)
        self.app.startComm(temp[1])
        self.update()
        

            
    @UserActionHandler
    def doAboutBoard(self, checked=None):
        '''Handler for  *about board* action'''
        self._dialogs['aboutboard'].initialize()
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
            temp = (self.app._autorefresh, self.app.board.getAccessLevel())
            self.app._autorefresh = False
            self.app.board.connect(dapi2.DApiAccessLevel.SERVICE, dapi2.DApiAccessLevel.SERVICE.passwd ) #@UndefinedVariable
            firmware = dlg.getFirmware()
            self.log.info('Firmware programming `{0!s}` '.format(firmware))
            self._flasProgressDialog = FlashProgressDialog(self,firmware)
            self._flasProgressDialog.show()
            self.app.processEvents()
            with open(str(dlg.getFirmware().fpath), 'rb') as fbin:
                self.board.flashBinaryFirm(fbin, self._flasProgressDialog.progress)
            self._flasProgressDialog.hide()
            del self._flasProgressDialog
            self.log.info('wait before reconnection ({}s)'.format(self.app.board.wait_after_reprogramming))
            self.app.sleep(self.app.board.wait_after_reprogramming)
            
            self.app.board.connect(temp[1], temp[1].passwd )
            self.app._autorefresh = temp[0]
        self.update()
        
    @UserBoardActionHandler
    def doResetFirmware(self, checked=None):
        '''Handler for  *reset firmware* action'''
        if QMessageBox.question(self, 'Reset firmware', """Are you sure you want to reset the firmware?\n
All memories will be reset to factory settings.""") ==  QMessageBox.Yes:
            temp = (self.app._autorefresh, self.app.board.getAccessLevel())
            
            self.app._autorefresh = temp[0]
            self.update()
        
        
    @UserBoardActionHandler
    def doMemoryStore(self, number, checked):
        self.board.memoryStore(number)
        self.board.getWorkspace().memories[number].read() 
    
    @UserBoardActionHandler
    def doMemoryRecall(self, number, checked):
        self.board.memoryRecall(number)
        self.board.getRegisters('setpoints', refresh=True)

class BasicQtApp(BaseQtApp):
    '''Class for *basic* GUI application
    
    Args:
        app_dir (str): Application root directory
        lang (str): If defined the language to use, otherwise the local session language.
    '''
    NAME = 'dcp-basic-gui'
    '''Application name'''
    
    
    def __init__(self, app_dir, lang):
        '''Constructor'''
        self._memoryActions = set([])
        super().__init__(app_dir, lang)
        
        
    def _initWin(self):
        self._window = BasicWindow(self) 
        self._window._initWin()
        
        
    def prepareSpecificCfg(self, parser):
        #parser.add_argument("-A", "--access-level", dest="access_level", choices=dapi2.DApiAccessLevel.list(),  help=BaseApp.tr("Sets the access level for the connection to the board. (Default=USER)"), default=None)
        super().prepareSpecificCfg(parser)
    
    def processSpecificCfg(self):
        # if self.config.access_level is not None:
        #     self.config.access_level = dapi2.DApiAccessLevel[self.config.access_level.upper()]
        # if not self.config.dev_mod and self.config.access_level is None:
        #     self.config.access_level = dapi2.DApiAccessLevel.USER
        super().processSpecificCfg()       
        
        
    def getAvailableActions(self, context={}):
        ret = super().getAvailableActions(context)
        if self.board is not None: 
            if self.isConnected():
                #ret.add('actionAboutBoard')  
                ret |= set(('actionMotorMode', 'actionRebootBoard','actionFirmReset'))
                if self.board.isOnStandby():
                    if self.board.getAccessLevel() >= dapi2.DApiAccessLevel.SERVICE:
                        ret.add('actionAPISendFirmware')
                    if self.board.getAccessLevel() > dapi2.DApiAccessLevel.NO:
                        ret.add('actionFirmReset')
                if self.board.getAccessLevel() > dapi2.DApiAccessLevel.NO:
                    ret |= self._memoryActions
        return ret        
        
    def initialize(self):
        BaseQtApp.initialize(self)
        if self.board and self.board.dmode == dapi2.DBoardPreferredDapiMode.COMMAND and not self.dapi.dev_mode:
            self.board.connect()
            

#        if self.board.isOnStandby():
#            self.board.setWorkspace(1)
        
         
    
        
    @property
    def memoryActions(self):
        return self._memoryActions
        
        
