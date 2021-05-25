'''Definition of base class for GUI application and base class for main window.

:author: F. Voillat
:date: 2021-0-24 Creation
:copyright: Dassym 2021
'''

from PyQt5.Qt import QApplication, QMessageBox, QAction, QSettings, QObject, QMainWindow,\
    Qt, QTimer, QTime, QEventLoop, QGuiApplication, QIcon, QSize
import sys
from functools import partial
from os.path import os

from app.base import BaseApp
import app
from app.gui.dlg import AboutDialog
from dapi2.dcom.base import DComException
from dboard.workspace import BaseWorkspace
from app.ressource import getRessourcePath
from app.gui.dlg.selectconnectiondialog import SelectConnectionDialog

from .res import res_img #@UnusedImport
from app.gui.splashscreen import AppSplashScreen
from dapi2.derror import DApiComError

 
TIMEOUT_MS = 250
'''GUI timer delay [ms]'''

REFRESH_COUNT = 2
'''Count between 2 refresh'''


STANDARD_LAYOUTS = {
    'vantage': os.path.join(app.IMG_DIR, 'layout-vantage.svg'),
    'vantage-dark': os.path.join(app.IMG_DIR, 'layout-vantage-dark.svg'),
    'lipo': os.path.join(app.IMG_DIR, 'layout-lipo.svg'),
    }


#===============================================================================
# class BaseGuiObject(QObject):
#     '''Base class for GUI objects.'''
#         
#     def __init__(self, owner=None, parent=None, widget=None):
#         '''Initialization
#         
#         :param owner: The owner of this GUI object (BaseGuiObject).
#         :param parent: The parent widget for displaying this GUI object (QWidget).    
#         :param widget: The widget if already created (QWidget).
#         '''
#         assert isinstance(owner, BaseGuiObject) or owner == None
#         assert isinstance(parent, QWidget) or parent == None
#         assert isinstance(widget, QWidget) or widget == None
#         self._owner = owner
#         self._parent = parent
#         self._widget = widget
#         self._disable_events_cnt = 0
#         super().__init__()
#         
#     def getWidget(self, name, qclass = QObject): 
#         ret = self.findChild(qclass, name, options=Qt.FindChildrenRecursively)
#         if ret == None: 
#             raise Exception('Widget `{0!s}` ({1!s}) not found!'.format(name, qclass.__name__))
#         return ret
#             
#     def disableEvents(self):
#         self._disable_events_cnt += 1
#         return self._disable_events_cnt
#     
#     def enableEvents(self):
#         if self._disable_events_cnt > 0:
#             self._disable_events_cnt -= 1
#         return self._disable_events_cnt
# 
#     def setSensitive(self, value):
#         self._widget.set_sensitive(value)
#         
#         
#     def _saveGeometries(self, settings):
#         pass
# 
#     def _restoreGeometries(self, settings):
#         pass
#     
#     
#     def saveUserConfig(self, settings):
#         '''Enregistre la configuration utilisateur.'''
#         settings.beginGroup(self.__class__.__name__)
#         try:
#             settings.setValue("Geometry", self.saveGeometry())
#             try:
#                 settings.setValue("State", self.saveState())
#             except AttributeError: pass
#             self._saveGeometries(settings)
#         except Exception as e:
#             self.log.error('save_user_config:'+str(e))
#         settings.endGroup()
#         
#     def restoreUserConfig(self, settings):
#         '''Restaure la configuration utilisateur.'''
#         settings.beginGroup(self.__class__.__name__)
#         try: 
#             self.restoreGeometry(settings.value("Geometry"))
#             try:
#                 self.restoreState(settings.value("State"))
#             except AttributeError: pass
#             self._restoreGeometries(settings)
#         except Exception as e:
#             self.log.error('restore_user_config:'+str(e))
#         settings.endGroup()
#         
#     @property
#     def owner(self):
#         return self._owner
#     @property
#     def parent(self):
#         return self._parent
#     
#     @property
#     def widget(self):
#         return self._widget 
#     @property
#     def events_enabled(self):
#         return self._disable_events_cnt == 0  
#     @property
#     def window(self):
#         return self._owner.window        
#     @property
#     def app(self):
#         return self._owner.app      
#===============================================================================
    

    
def UserActionHandler(function):
    
    def wrapper(self, *args, **kwargs):
        if not self.eventsEnabled: return
        self.log.debug(function.__name__+str(args))
        self.disableEvents()            
        try:
            return function(self, *args, **kwargs)
        except DApiComError as e:
            self.handleDApiComError(e)
        except Exception as e:
            self.handleError(e)
        finally:
            self.enableEvents()    
            return None
    return wrapper

def UserBoardActionHandler(function):
    
    def wrapper(self, *args, **kwargs):
        ret = None
        if not self.eventsEnabled: return
        self.log.debug(function.__name__+str(args))
        self.disableEvents()            
        try:
            ret = function(self, *args, **kwargs)
        except DApiComError as e:
            self.handleDApiComError(e)
        except Exception as e:
            self.handleError(e)
        finally:
            self.enableEvents()    

        self.update()
        return ret 

    return wrapper



class BaseMainWindow(QMainWindow):
    '''Base class for application's main window.
    
    :param BaseGuiApp app: The application that owns the window
    '''
    
    def __init__(self, app, *args, **kwargs):
        '''Constructor'''
        self._app = app
        self._disable_events_cnt = 0
        self._dialogs = {}
        self._actions = {}
        QMainWindow.__init__(self, *args, **kwargs)
        
    def _initWin(self):
        self._addDialog('about', AboutDialog(self))
        self.actionAbout.triggered.connect(self.onAbout)
        self.actionAutoRefresh.setChecked(self._app.autorefresh)
        self.actionAutoRefresh.toggled.connect(self.onAutorefreshToggled)
        self.actionRefresh.triggered.connect(self.onRefreshTriggered)
        
        
    def _cleanupWin(self):
        
        for dlg in list(self._dialogs.keys()):
            try:
                self.log.debug('cleanup dialog '+dlg)
                self._dialogs[dlg].close()
                del self._dialogs[dlg]
            except Exception as e:
                self.log.error('An error occurred while cleaning up the {} dialog!\n{}'.format(dlg, str(e)))
                
        
    def _addAction(self, parent, name, label, data, icon, handler, tooltips=None, menu=None, bar=None):
        '''Adds an action on menu and toolbar.
        
        :param QWidget parent: The parent of new action.
        :param str name: The action name
        :param str label. The action label
        :param data: Data to pass to action
        :param QIcon icon: The action icon
        :param function handler: The action handler  
        :param str tooltips: The action tooltips text
        :param QMenu menu: the menu to which the action must be added
        :param QToolBar bar: the toolbar to which the action must be added
        '''
        
        #self.log.debug('AddAction({0:s})'.format(name))
        
        if icon is not None:
            action = QAction(icon, label, parent, triggered=partial(handler, data) )
        else:
            action = QAction(label, parent, triggered=partial(handler, data) )
        action.setObjectName(name)
        action.setToolTip(tooltips)
        action.setEnabled(True)
        if menu is not None:
            menu.addAction(action)
        if bar is not None:
            bar.addAction(action)        
        #self.log.debug('Add action '+name)
        self._actions[name] = action
        return action  
    
    def _addDialog(self, name, dialog):
        assert not name in self._dialogs, 'The `{}` dialog already exists!'.format(name)
        self.log.debug('_addDialog('+name+','+str(dialog)+')') 
        self._dialogs[name] = dialog      
    
    def initialize(self):
        for qaction in self.findChildren(QAction):
            if qaction.objectName():  
                self._actions[qaction.objectName()] = qaction
        
        for ws in self.app.board.workspaces:
            self._addAction(self, name='actionWorkspace{0:d}'.format(ws.par), label=ws.name, data=ws, icon=None, handler=self.onWorkspaceTriggered, tooltips=None, menu=self.menuWorkspace)
            
        self.update()
        
    def finalize(self):
        self._cleanupWin()
        
    def closeEvent(self, event):
        self.log.debug('closeEvent '+str(event))
        for dlg in list(self._dialogs.keys()):
            self._dialogs[dlg].close()
        event.accept()
        return QMainWindow.closeEvent(self, event)
        
    def saveGeometries(self, settings):
        settings.beginGroup("MainWindow")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.endGroup()
    
        
    def restoreGeometries(self, settings):
        settings.beginGroup("MainWindow")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("state"))
        settings.endGroup()        
    
    def disableEvents(self):
        '''Disable event processing'''
        self._disable_events_cnt += 1
        return self._disable_events_cnt
    
    def enableEvents(self):
        '''Enable event processing.
        
        For the processing of events to be active, the number of nested calls for deactivation and activation must be equal.
        '''
        if self._disable_events_cnt > 0:
            self._disable_events_cnt -= 1
        return self._disable_events_cnt
    
    
    def getWidget(self, name, qclass = QObject): 
        '''Find a widget based on its name
        
        :param str name: The widget name to find.
        :param class qclass: The widget call to find. (default QObject => any)    
        ''' 
        ret = self.findChild(qclass, name, options=Qt.FindChildrenRecursively)
        if ret == None: 
            raise Exception('Widget `{0!s}` ({1!s}) not found!'.format(name, qclass.__name__))
        return ret
    
    def handleError(self, exception):
        '''Error handler'''
        return self._app.handleError(exception)
    
    def handleDApiComError(self, exception):
        '''DAPI communication Error handler'''
        self.log.error(str(exception))
        self.app.displayError(exception)
        
    
    def refreshActionsSensitivity(self, context={}):
        '''Updates the sensitivity of actions
        
        :param dict context: A dictionary that can contain contextual information.
        '''
        available_actions =  self.app.getAvailableActions(context)
        for aname in available_actions:
            o = self.getWidget(aname)
            o.setEnabled(True)
        for aname in self.actions - available_actions:
            try:
                self.getWidget(aname).setEnabled(False)
            except Exception as e:
                self.log.error('refreshActionsSensitivity -> '+str(self.actions - available_actions))
                raise e   
            
            
    
    def refresh(self):
        '''Refresh the windows according board setpoints'''
        self.disableEvents()
        try:
            if not self.board.isOnStandby():
                self.board.refreshSetpoints()
            for action in self._actions.values():
                if isinstance(action.data, BaseWorkspace):
                    action.setChecked( action.data.active )
                    
            self.refreshActionsSensitivity()
        finally:
            self.enableEvents()
        
    
    @UserActionHandler
    def onAbout(self, checked=None):
        '''Handler for "about" action.'''
        self.dialogs['about'].exec()
    
    @UserActionHandler
    def onRefreshTriggered(self, checked=None):
        self.app.refresh()
        
    
    @UserActionHandler
    def onAutorefreshToggled(self, checked=None):
        self.app.autorefresh = checked
    
    @UserBoardActionHandler
    def onWorkspaceTriggered(self, workspace=None, checked=None):
        self.app.board.setWorkspace(workspace)
    
        
    @property
    def app(self):
        '''The application that owns the window.'''
        return self._app
    @property
    def log(self):
        '''shortcuts to the logger of the application'''
        return self._app.log
    @property
    def board(self):
        '''shortcuts to the board (:class:`dboard.BaseDBoard`) of the application'''
        return self._app.board
    @property
    def dapi(self):
        '''shortcuts to the *dapi* (:class:`dapi2.dapi2.DApi2`) of the application'''
        return self._app.dapi
    @property
    def eventsEnabled(self):
        '''The events processing activation status'''
        return self._disable_events_cnt == 0          
    @property
    def actions(self):
        '''The list of names of actions'''
        return self._actions.keys()
    
    @property
    def dialogs(self):
        '''The dialog windows dictionary {name:widget}'''
        return self._dialogs
    

class BaseGuiApp(BaseApp, QApplication):
    '''Base class for GUI applications
    
    :param Namespace config: Application configuration
    '''
    
    NAME = 'dcp-base-gui'
    '''Application name'''
    
    @classmethod
    def cast(cls, app):
        assert isinstance(app, BaseApp)
        app.__class__ = cls
        return app

    def __init__(self, app_dir):
        '''Constructor'''
        QApplication.__init__(self, [])
        self.splash = None 
        BaseApp.__init__(self, app_dir)
        self.autorefresh = True
        self._refresh_count = REFRESH_COUNT
        self.setApplicationVersion(app.__version__)
        self.setApplicationName(self.NAME)
        self.setOrganizationName(app.DASSYM)
        self.setOrganizationDomain(app.DASSYM_DOMAIN)
        self.setQuitOnLastWindowClosed(True) 
        self._window = None
        self.openSplashScreen()
        self._timer = QTimer()
        
        
        
    def _initWin(self):
        assert False, "Abstract method!"
        
    def connectionCallback(self, options):  
        dialog = SelectConnectionDialog(options)
        r = dialog.exec()
        if r == True:
            ret = dialog.getSelectedOption()
            del dialog
            return int(ret)
        else:
            sys.exit(0)
    
        
    def _refresh(self):
        if self._board is not None and self.isConnected():
            if not self._dcom.isOk(): return 
            self._board.refreshState()
            #self._board.refreshSetpoints()
            #TODO: self.update_status_misc()
        # else:
            # self._label_status_miscellaneous.setText('~')
            # self._label_status_connection.setText('~')
            
    def prepareSpecificCfg(self, parser):
        parser.add_argument("--layout",  help=BaseApp.tr("The GUI layout name or SVG file. (default: vantage)"), dest="layout", default="vantage")
    
            
    def getAvailableActions(self, context={}):
        '''Returns a set with available actions according actual situation.
        
        :return: available actions
        :rtype: Set of str 
        '''
        ret = set(['actionQuit','actionHelp','actionAbout', 'actionAutoRefresh'])
        if self._board is not None: 
            if self.isConnected():
                ret |= set(('actionSysDisconnect', 'actionRefresh'))
                aws = self._board.getWorkspace()
                for ws in self._board.workspaces:
                    if ws != aws:
                        ret.add('actionWorkspace{0:d}'.format(ws.par)) 
                if aws.isFunctional(): 
                    ret |= set(['actionMotorCW','actionMotorCCW', 'actionLightEnabled',])
                    
                    if self._board.hasBlueLight():
                        ret.add('actionLightBlue')
                    if self._board.isMotorStarted():
                        ret.add('actionMotorStop')
                    else:                        
                        ret.add('actionMotorStart')
            else:
                ret.add('actionSysConnect')
        return ret     
    
    def openSplashScreen(self):
        '''Ouvre le splash screen''' 
        self.log.debug('openSplashScreen')
        #splash_img = QPixmap(':img/splashscreen.png')
        rect = QGuiApplication.primaryScreen().geometry()
        splash_img = QIcon(':img/splashscreen.svg').pixmap(QSize(400,200))
        self.splash = AppSplashScreen(self, splash_img, Qt.WindowStaysOnTopHint)
        self.splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.splash.setEnabled(True)
        self.splash.show()
        self.splash.showMessage(self.applicationName())
        self.splash.show()
        self.splash.update()
        self.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
        self.log.debug('splashscreen open')
        return self.splash 
        
        
    def closeSplashScreen(self):
        '''Ferme le splash screen'''
        self.log.debug('closeSplashScreen')
        self.processEvents()
        self.splash.finish(self._window)
        self.splash = None      
        
    def say(self, level, text):
        
        super().say(level,text)
        if self.splash:
            self.splash.showMessage(text)
            self.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
        
        
    def saveUserConfig(self):
        '''Saves the user configuration of windows of application.'''
        self.log.debug('saveUserConfig')
        settings = QSettings()
        self._window.saveGeometries(settings)

    def restoreUserConfig(self):
        '''Restores the user configuration of windows of application.'''
        self.sayHigh(BaseApp.tr('Restoration of visual configuration'))
        settings = QSettings()
        try:
            self._window.restoreGeometries(settings)
        except Exception as e:
            self.log.error(str(e))
            self.sayError(BaseApp.tr('Restoration of visual configuration is aborted!'))


    def refresh(self):
        '''Refresh the display'''
        self._refresh()
        self._window.refresh()
        

    def initialize(self):
        '''Initialization of application'''
        self._initWin()
        BaseApp.initialize(self)
        self.sayHigh('Load board registers...')
        self.board.refreshAll()
        self.sayHigh('Window initialization...')
        self._window.initialize()
        
        
        
    def run(self):
        '''Executes application'''
        self.log.info(BaseApp.tr('Run')+" "+self.NAME+"...")
        
        self.log.debug('Show main window...')
        self._window.show()
        self.restoreUserConfig()
        self.closeSplashScreen()
        self._timer0 = self.startTimer(TIMEOUT_MS)
        self.log.debug('Start Qt main loop...')
        exit_code = self.exec()
        self.log.debug('Exit from Qt main loop...')
        self.saveUserConfig()
        self._window.finalize()
        self.killTimer(self._timer0)
        del self._window
        return self.terminate(exit_code)
                

    def terminate(self, exit_code=0):
        '''Terminates application'''
        try:
            self.log.info(BaseApp.tr('Finished')+"("+str(exit_code)+")")
        except:
            pass
        if exit_code > 0:
            self.exit(exit_code)
            exit(exit_code)         
        
        
    def displayError(self, error):
        '''Display the given error
        
        :param str error: The error message''' 
        self.log.error(error)
        dialog = QMessageBox(
                    QMessageBox.Critical,
                    self.applicationName()+BaseApp.tr('Error:'),
                    BaseApp.tr("An error has occurred!\nDetail:\n")+str(error),
                    QMessageBox.Ok )
        dialog.exec()
        
    def timerEvent(self, event=None):
        '''Periodic processing caused by the GUI "timeout"
        
        @param QTimerEvent event : The timer event.
        '''
        try:
            #self.log.debug('timer0')
            if self.autorefresh and self._refresh_count > 0:
                self._refresh_count -= 1
                if self._refresh_count == 0 :
                    self.refresh()
                    self._refresh_count = REFRESH_COUNT
        except DComException as e:
            self.board.disconnect()
            self.refresh()
        except Exception as e:
            self.handleError(e)
            
            
    def getLayoutFile(self, layout):
        '''Returns the SVG file for a control panel layout
        
        :param str layout: The layout name or resource
        :return: the SVG file path
        :rtype: str
        '''  
        try:
            return STANDARD_LAYOUTS[layout]
        except KeyError:
            return getRessourcePath(layout)
        
        
            
    def sleep(self, seconds):
        '''Put the application to sleep
        
        :param float seconds: sleep duration of the application expressed in seconds
        '''
        wake_up_time = QTime.currentTime().addMSecs(int(seconds*1000))
        while (QTime.currentTime() < wake_up_time):
            self.processEvents(QEventLoop.AllEvents, 100)        
        
        
    @property
    def window(self):
        '''The main window of application'''
        return self._window


        
        