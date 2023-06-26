'''Definition of base class for GUI application and base class for main window.

:author: F. Voillat
:date: 2021-0-24 Creation
:copyright: Dassym 2021
'''


from PyQt5.Qt import QApplication, QMessageBox, QAction, QSettings, QObject, QMainWindow, \
    Qt, QTime, QEventLoop, QIcon, QLabel, QDialog, QPixmap, \
    QRegularExpression, QSize
from PyQt5.QtCore import QLocale, QTranslator, QLibraryInfo, QT_VERSION_STR, PYQT_VERSION_STR
from dapi2 import BaseWorkspace
from dapi2.dapi2 import DApiAdditionalBoard
from dapi2.dboard.common import DBoardPreferredDapiMode
from dapi2.dcom.base import DComException
from functools import partial
import logging
import sys

import app
from app.base import BaseApp
from app.i18n import i18n_rc  # @UnusedImport
from app.ressource import getRessourcePath
from app.stopwatch import Stopwatch

from .common import UserActionHandler, UserBoardActionHandler, DisableEvent, REFRESH_COUNT_INIT, TIMEOUT_MS, STANDARD_LAYOUTS, \
        REFRESH_ALL_REF_TIME
from .dlg.aboutdialog import AboutDialog
from .dlg.connectdialog import ConnectDialog
from .dlg.registersviewdialog import RegistersViewDialog
from .dlg.selectconnectiondialog import SelectConnectionDialog
from .splashscreen import AppSplashScreen


#from .res import img_rc #@UnusedImport
IconSizes = (16,32,48,64)

class BaseMainWindow(QMainWindow):
    '''Base class for application's main window.

    :param BaseQtApp app: The application that owns the window
    '''

    def __init__(self, app, *args, **kwargs):
        '''Constructor'''
        self.log = logging.getLogger(self.__class__.__name__)
        self._app = app
        self._disable_events_cnt = 0
        self.old_level = None
        self._dialogs = {}
        self._actions = {}
        QMainWindow.__init__(self, *args, **kwargs)

    def _initWin(self):
        self.setWindowIcon(QIcon('./img/dcp.ico'))
        self._addDialog('about', AboutDialog(self))
        self._addDialog('registersview', RegistersViewDialog(self))
        self._addDialog('connect', ConnectDialog(self))
        self.actionAbout.triggered.connect(self.onAbout)
        self.actionRegistersView.triggered.connect(self.onRegistersView)
        self.actionAutoRefresh.setChecked(self._app._autorefresh)
        self.actionAutoRefresh.toggled.connect(self.onAutorefreshToggled)
        self.actionRefresh.triggered.connect(self.onRefreshTriggered)
        self.actionConnect.triggered.connect(self.onConnect)
        self.actionLink.triggered.connect(self.onLink)
        self._labelStatusBoard = QLabel(self)
        self._labelStatusBoard.setToolTip(BaseApp.tr('Board'))
        self._labelStatusAccessLevel = QLabel(self)
        self._labelStatusAccessLevel.setToolTip(BaseApp.tr('Access level'))
        self._labelStatusConnection = QLabel(self)
        self._labelStatusConnection.setToolTip(BaseApp.tr('Connection'))
        self._labelStatusWorkspace = QLabel(self)
        self._labelStatusWorkspace.setToolTip(BaseApp.tr('Workspace'))
        self._labelStatusWorkspaceFunctional = QLabel(self)
        self._labelStatusWorkspaceFunctional.setPixmap(QPixmap(':/img/16/unknow.png'))

        self.statusBar.addPermanentWidget( self._labelStatusBoard )
        self.statusBar.addPermanentWidget( self._labelStatusWorkspace )
        self.statusBar.addPermanentWidget( self._labelStatusWorkspaceFunctional )
        self.statusBar.addPermanentWidget( self._labelStatusAccessLevel )
        self.statusBar.addPermanentWidget( self._labelStatusConnection )



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

        :return: The action created.
        '''

        self.log.debug('_addAction({0:s})'.format(name))

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

    def _removeAction(self, action):
        self.log.debug('_removeAction({0:s})'.format(action.objectName()))
        del self._actions[action.objectName()]
        action.deleteLater()
        del action

    def _addDialog(self, name, dialog):
        assert not name in self._dialogs, 'The `{}` dialog already exists!'.format(name)
        #self.log.debug('_addDialog('+name+','+str(dialog)+')')
        self._dialogs[name] = dialog
        return dialog

    def initialize(self):
        self.log.debug('Initialize BaseMainWindow ...')
        for qaction in self.findChildren(QAction):
            if qaction.objectName():
                self._actions[qaction.objectName()] = qaction

        for dlg in self.dialogs.values():
            dlg.initialize(self.app)

        if self.app.board and self.dapi.dcom:
            self.boardInit()
        # self.dialogs['registersview'].initialize()

    def finalize(self):
        self._cleanupWin()


    def boardInit(self):
        self.log.debug('boardInit')
        assert self.app.board is not None, "No board instantiated!"
        for ws in self.app.board.workspaces:
            self._addAction(self, name='actionWorkspace{0:d}'.format(ws.par), label=ws.name, data=ws, icon=None, handler=self.onWorkspaceTriggered, tooltips=None, menu=self.menuWorkspace)
        for dlg in self.dialogs.values():
            dlg.boardInit()

        self.onWorkspaceChanged(self.app.board.getWorkspace())
        self.onConnectionChanged(self.app.isConnected(), self.app.board.getAccessLevel())

    def onWorkspaceChanged(self, workspace):
        self._labelStatusWorkspace.setText("{0!s}:{1!s}/{2!s}".format(
                workspace.name,
                workspace.controllerType.name,
                workspace.peripheralName,
            ))
        self._labelStatusWorkspace.setToolTip("{0!s}\nController type:{1!s}\nPeripheral type:{2!s}".format(
                workspace.name,
                workspace.controllerType.help,
                workspace.peripheralType.help,
            ))
        for dlg in self.dialogs.values():
            dlg.onWorkspaceChanged(workspace)
        self.refresh()

    def onConnectionChanged(self, state, level):
        self._labelStatusAccessLevel.setPixmap(QPixmap(':img/24/access-{0:d}.png'.format(level.value)))
        self._labelStatusAccessLevel.setToolTip(BaseApp.tr("Access level: {0:s}".format(level.name)))


    def boardReset(self):
        self.log.debug('boardReset ...')
        for qaction in self.findChildren(QAction,
                QRegularExpression('actionWorkspace.+')
                , Qt.FindChildrenRecursively ):
            self._removeAction(qaction)
        self.menuWorkspace.clear()
        self.log.debug('... boardReset')

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
        settings.beginGroup("Dialogs")
        for n, d in self.dialogs.items():
            settings.setValue(n+".geometry", d.saveGeometry())
        settings.endGroup()



    def restoreGeometries(self, settings):
        settings.beginGroup("MainWindow")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("state"))
        settings.endGroup()
        settings.beginGroup("Dialogs")
        for n, d in self.dialogs.items():
            d.restoreGeometry(settings.value(n+".geometry"))
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
            #o = self.getWidget(aname)
            try:
                o = self._actions[aname]
                o.setEnabled(True)
            except KeyError:
                pass
        for aname in self.actions - available_actions:
            try:
                #self.getWidget(aname).setEnabled(False)
                o = self._actions[aname]
                o.setEnabled(False)
            except Exception as e:
                self.log.error('refreshActionsSensitivity -> '+str(self.actions - available_actions))
                raise e


    @DisableEvent
    def refresh(self):
        '''Refresh the window according board set points'''
        if self.app.dcom:
            self._labelStatusConnection.setText(str(self.app.dcom))
            self.actionLink.setChecked(  self.app.dcom.isOpen() )
            self.actionAutoRefresh.setChecked(self.app.autorefresh)
            if self.board is not None:
                ab = self.board.getAdditionalBoard()
                if ab == DApiAdditionalBoard.NO:
                    self._labelStatusBoard.setText("{0:s} #{1:05d}".format(self.board.name, self.board.sn))
                else:
                    self._labelStatusBoard.setText("{0:s}+{2:s} #{1:05d}".format(self.board.name, self.board.sn, ab.descr))

                if self.board.dmode != DBoardPreferredDapiMode.COMMAND:
                    self._labelStatusBoard.setText(self._labelStatusBoard.text() + "[{}]".format(self.board.dmode.name[:3]))

                if self.board.workspace.isFunctional():
                    self._labelStatusWorkspaceFunctional.setPixmap(QPixmap(':/img/16/status-on.png'))
                else:
                    self._labelStatusWorkspaceFunctional.setPixmap(QPixmap(':/img/16/status-off.png'))
                #self._labelStatusWorkspace.setText(str(self.app.board.getWorkspace().name))
                #self.log.debug('Board = '+repr(self.app.board))
                #self.log.debug('Access level = '+self.app.board.getAccessLevel().name)
                # self._labelStatusAccessLevel.setPixmap(QPixmap(':img/24/access-{0:d}.png'.format(self.app.board.getAccessLevel().value)))
                # self._labelStatusAccessLevel.setToolTip(BaseApp.tr("Access level: {0:s}".format(self.app.board.getAccessLevel().name)))
                #self._labelStatusAccessLevel.setText(self.app.board.getAccessLevel().name)
                # update Workspace actions
                for action in self._actions.values():
                    if isinstance(action.data, BaseWorkspace):
                        action.setChecked( action.data.active )
            else:
                self._labelStatusBoard.setText(BaseApp.tr('No board'))
                self._labelStatusWorkspaceFunctional.setPixmap(QPixmap(':/img/16/unknow.png'))
                self._labelStatusWorkspace.clear()
                self._labelStatusAccessLevel.clear()
        else:
            self._labelStatusConnection.setText(BaseApp.tr('Unlink'))
            self._labelStatusWorkspaceFunctional.setPixmap(QPixmap(':/img/16/unknow.png'))
            self._labelStatusBoard.clear()
            self._labelStatusWorkspace.clear()
            self._labelStatusAccessLevel.clear()
        self.refreshActionsSensitivity()
        self.update()


    @UserActionHandler
    def onAbout(self, checked=None):
        '''Handler for "about" action.'''
        self.dialogs['about'].exec()

    @UserActionHandler
    def onRegistersView(self, checked=None):
        '''Handler for "Registers view" action.'''
        self.dialogs['registersview'].show()


    @UserActionHandler
    def onRefreshTriggered(self, checked=None):
        self.app.refresh()


    @UserActionHandler
    def onAutorefreshToggled(self, checked=None):
        self.app._autorefresh = checked

    @UserBoardActionHandler
    def onWorkspaceTriggered(self, workspace=None, checked=None):
        self.app.changeWorkspace(workspace)
        #self.app.onWorkspaceChanged()


    @UserBoardActionHandler
    def onConnect(self, checked=None):
        '''Handler for  *connect* action'''

        if not self.app.isConnected():
            self.app.startComm()
        dlg = self._dialogs['connect']
        if dlg.exec(level=self.old_level) == QDialog.Accepted:
            level = dlg.getAccessLevel()
            self.log.info("Change access level to "+level.name)
            self.board.connect(level, level.passwd )
            self.log.debug("New access level "+self.board.getAccessLevel().name)
            self.old_level = level

    @UserBoardActionHandler
    def onLink(self, checked=None):
        '''Handler for *link* action'''
        if checked:
            self.app.startComm()
        else:
            self.app.stopComm()

    @property
    def app(self):
        '''The application that owns the window.'''
        return self._app
    # @property
    # def log(self):
    #     '''shortcuts to the logger of the application'''
    #     return self._app.log
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


class BaseQtApp(BaseApp, QApplication):
    '''Base class for GUI applications

    Args:
        app_dir (str): Application root directory
        lang (str): If defined the language to use, otherwise the local session language.
    '''

    NAME = 'dcp-base-gui'
    '''Application name'''

    # @classmethod
    # def tr(cls, text, disambiguation=None, n=-1):
    #     return QCoreApplication.translate('BaseQtApp',text, disambiguation, n)

    @classmethod
    def cast(cls, app):
        assert isinstance(app, BaseApp)
        app.__class__ = cls
        return app

    def __init__(self, app_dir, lang):
        '''Constructor'''
        QApplication.__init__(self, [])
        self.splash = None
        BaseApp.__init__(self, app_dir, lang)
        self._autorefresh = False
        self._refresh_count_init = REFRESH_COUNT_INIT
        self._refresh_count = self._refresh_count_init
        self._refresh_pass = 0
        self.setApplicationVersion(app.__version__)
        self.setApplicationName(self.NAME)
        self.setOrganizationName(app.APP_PUBLISHER)
        self.setOrganizationDomain(app.DASSYM_DOMAIN)
        self.setQuitOnLastWindowClosed(True)
        self.setWindowIcon(QIcon(':img/dcp.ico'))
        self._window = None
        self.openSplashScreen()
        self._timer0 = None
        self._icons = {}
        self._loadIcons()
        self._initL10n(lang)
        self._initWin()


    def _loadIcons(self):
        for n in ('ok', 'warning', 'error', 'info'):
            N = n[0].upper()
            self._icons[N] = QIcon()
            for x in IconSizes:
                s = QSize(x,x)
                self._icons[N].addFile(f':/img/{x}/{n}.png', size=s)

        self._icons['OWE'] = (self._icons['O'],self._icons['W'],self._icons['E'])


    def _initL10n(self, lang):
        '''Initialize the application localization

        Args:
            lang (str): If defined the language to use, otherwise the local session language.
        '''

        if lang is not None:
            self.locale = QLocale(lang)
        else:
            self.locale = QLocale.system()
        self._qtTranslator = QTranslator()
        self._qtBaseTranslator = QTranslator()
        self._qtAppTranslator = QTranslator()

        self.log.debug(f"_initL10n({self.locale.name()})")

        s = QLibraryInfo.location(QLibraryInfo.TranslationsPath)  # @UndefinedVariable

        if not self._qtAppTranslator.load(self.locale, 'dsm-cp', "_", ":/i18n/", ".qm"):
            self.log.error('DSMCP translation resource load failed for {0!s}!'.format(self.locale.name()))
        else:
            self.installTranslator(self._qtAppTranslator)
            self.log.info(BaseApp.tr('DSMCP Translation resource successfully loaded for {0!s}.').format(self.locale.name()))

        if not self._qtTranslator.load( 'qt_help_fr', s):
            self.log.error('Translation load `qt_help_fr.qm` failed for {0!s} in `{1!s}`!'.format(self.locale.name(), s))
        else:
            self.installTranslator(self._qtBaseTranslator)
            self.log.info(BaseApp.tr('Qt translation file successfully loaded for {0!s}.').format(self.locale.name()))

        if not self._qtBaseTranslator.load(self.locale, 'qtbase', '_', s):
            self.log.error('Translation load `qtbase_*.qm` failed for {0!s} in `{1!s}`!'.format(self.locale.name(), s))
        else:
            self.installTranslator(self._qtBaseTranslator)
            self.log.info(BaseApp.tr('Qt base translation file successfully loaded for {0!s}.').format(self.locale.name()))



    def _initWin(self):
        assert False, "Abstract method!"


    def connectionCallback(self, options):
        dialog = SelectConnectionDialog(self, options)
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
            if self._refresh_pass == 0:
                self._board.refreshHeader()
                self._board.refreshState()
                self._board.refreshSetpoints()
                self._refresh_pass = 1
            else:
                self._board.refreshState()
                self._refresh_pass += 1
                if self._refresh_pass == 4:
                    self._refresh_pass = 0
            #TODO: self.update_status_misc()
        # else:
            # self._label_status_miscellaneous.setText('~')
            # self._label_status_connection.setText('~')

    def prepareSpecificCfg(self, parser):
        super().prepareSpecificCfg(parser)
        #parser.add_argument("-A", "--access-level", dest="access_level", choices=[x.name.lower() for x in DApiAccessLevel],  help=BaseApp.tr("Sets access level'. (Default=factory)"), default=DApiAccessLevel.FACTORY.name)
        autorefresh_grp = parser.add_mutually_exclusive_group()
        autorefresh_grp.add_argument("--autorefresh-off", dest="autorefresh_on", action="store_false", default=False, help=BaseApp.tr("Disables auto refresh on start up."))
        autorefresh_grp.add_argument("--autorefresh-on", dest="autorefresh_on", action="store_true", default=False, help=BaseApp.tr("Enables auto refresh on start up."))

    def processSpecificCfg(self):
        #self.config.access_level = DApiAccessLevel[self.config.access_level.upper()]
        self._autorefresh = self.config.autorefresh_on
        super().processSpecificCfg()


    def logEnvironment(self):
        self.log.debug('Qt version:{0!s}'.format(QT_VERSION_STR))
        self.log.debug('PyQt version:{0!s}'.format(PYQT_VERSION_STR))
        self.log.debug('Qt locale:`{0!s}` ; decimal: `{1!s}` : language: {2!s}'.format(self.locale.name(), self.locale.decimalPoint(), self.locale.bcp47Name()))


    def getAvailableActions(self, context={}):
        '''Returns a set with available actions according actual situation.

        :return: available actions
        :rtype: Set of str
        '''
        ret = set(['actionQuit', 'actionLink', 'actionConnect', 'actionHelp','actionAbout', 'actionRegistersView',
                   'actionAutoRefresh', 'actionWorkspace0'])
        if self._board is not None:
            if self.isConnected():
                ret |= set(('actionRefresh','actionAboutBoard',))
                aws = self._board.getWorkspace()
                for ws in self._board.workspaces:
                    if ws != aws:
                        ret.add('actionWorkspace{0:d}'.format(ws.par))
                if aws.isFunctional():
                    ret |= set(['actionMotorReverse', 'actionLightEnabled',])

                    if self._board.hasBlueLight():
                        ret.add('actionLightBlue')
                    if self._board.isMotorStarted():
                        ret.add('actionMotorStop')
                    else:
                        ret.add('actionMotorStart')
            else:
                pass
        return ret

    def onWorkspaceChanged(self, workspace):
        super().onWorkspaceChanged(workspace)
        self._window.onWorkspaceChanged(workspace)

    def onConnectionChanged(self, state, level):
        super().onConnectionChanged(state, level)
        self._window.onConnectionChanged(state, level)



    def openSplashScreen(self):
        '''Ouvre le splash screen'''
        self.log.debug('openSplashScreen')
        splash_img = QPixmap(':img/splashscreen.png')
        #rect = QGuiApplication.primaryScreen().geometry()
        #splash_img = QIcon(':img/splashscreen.png').pixmap(QSize(400,200))
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

    def isGui(self):
        return True




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
        self.log.debug('refresh')
        self._refresh_pass = 0
        self.partialRefresh()

    def partialRefresh(self):
        if self.board:
            w = Stopwatch(autostart=True)
            self._refresh()
            w.stop()
            self._window.refresh()

            self.log.debug(f"Time to refresh: {w.time:0.4f}s")
            if self._refresh_pass == 1 and w.time > 0.250:
                self._refresh_count_init += 1

    def startUp(self):
        super().startUp()
        self.log.debug('Startup BaseQtApp ...')
        self.restoreUserConfig()

    def initialize(self):
        '''Initialization of application'''
        BaseApp.initialize(self)
        self.log.debug('Initialize BaseQtApp ...')
        self.sayHigh('Window initialization...')
        self._window.initialize()



    def run(self):
        '''Executes application'''
        self.log.info(BaseApp.tr('Run')+" "+self.NAME+"...")
        self.initComm()
        self.startComm(self.config.access_level)
        #self.refresh()
        self._window.old_level = self.board.getAccessLevel()
        self.log.debug('Show main window...')
        self._window.show()

        self.closeSplashScreen()
        self.startTimer()
        self.log.debug('Start Qt main loop...')
        exit_code = self.exec()
        self.log.debug('Exit from Qt main loop...')
        self.saveUserConfig()
        self._window.finalize()
        self.stopTimer()
        del self._window
        return self.terminate(exit_code)

    def startTimer(self):
        if not self._timer0:
            self._timer0 = QApplication.startTimer(self, TIMEOUT_MS)
            self._refresh_count = REFRESH_COUNT_INIT

    def stopTimer(self):
        if self._timer0:
            self.killTimer(self._timer0)
            self._timer0 = None

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
                    self.name+BaseApp.tr('Error:'),
                    BaseApp.tr("An error has occurred!\nDetail:\n")+str(error),
                    QMessageBox.Ok, self.window,
                    Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowStaysOnTopHint)
        dialog.exec()

    def errorInfo(self):
        ret = super().errorInfo()
        ret = ret + (('Qt',f"{QT_VERSION_STR} / PyQt: {PYQT_VERSION_STR}"),)
        return ret

    def initComm(self):
        BaseApp.initComm(self)

    def stopComm(self):
        super().stopComm()
        self.stopTimer()
        self._window.boardReset()

    def startComm(self, access_level=None):
        t = super().startComm(access_level)
        if t > REFRESH_ALL_REF_TIME:
            self._refresh_count_init = round(REFRESH_COUNT_INIT * t / REFRESH_ALL_REF_TIME)
            self.sayWarning(BaseApp.tr('The refresh period has been increased {0:.0f} ms'.format(REFRESH_COUNT_INIT*TIMEOUT_MS)))
        self._window.boardInit()
        self.startTimer()


    def timerEvent(self, event=None):
        '''Periodic processing caused by the GUI "timeout"

        @param QTimerEvent event : The timer event.
        '''
        try:
            #self.log.debug('timer0')
            if self._autorefresh and self._refresh_count > 0:
                self._refresh_count -= 1
                if self._refresh_count == 0 :
                    self.partialRefresh()
                    self._refresh_count = self._refresh_count_init
        except DComException as e:
            self.sayError(BaseApp.tr('Communication is broken!'))
            self.stopComm()
            #self.board.disconnect()
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


    def icon(self, name):
        return self._icons[name]
    def pixmap(self, name, size):
        return self._icons[name].pixmap(QSize(size,size))

    @property
    def window(self):
        '''The main window of application'''
        return self._window

    @property
    def autorefresh(self):
        return self._autorefresh

    @property
    def icons(self):
        return self._icons

# ==== Initialize ====
log = logging.getLogger(__name__)
log.debug('Initialize module')



