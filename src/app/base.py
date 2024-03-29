'''Implementation of Application Base Class.

:author: F. Voillat
:date: 2021-03-19 Created
'''

import getpass
import logging
import os.path
import platform
from serial import Serial, SerialException
import socket
import sys
import traceback


import re as RE

import dapi2

from .version import __version__,  DATE as APP_DATE # @UnresolvedImport
from .common import FIRM_PATHS, IMG_DIR, FIRM_DIR, TEMP_DIR, USR_DATA_DIR, APP_NAME, VERBOSITY
from .db import Database
from .stopwatch import Stopwatch
from .teller import TellerInterface
from .tracer import Tracer
from .utils import configStr
import serial


class BaseApp(TellerInterface, object):
    '''Base class for *dsmcp* applications

    Args:
        app_dir (str): The application root directory.

    '''

    NAME = APP_NAME
    DEFAULT_ACCESS_LEVEL = dapi2.DApiAccessLevel.USER
    '''Application default board access level. :py:class:`dapi2.dapi2.DApiAccessLevel` '''

    @classmethod
    def tr(cls, text, disambiguation=None, n=-1):
        return text
        #return QCoreApplication.translate('BaseApp',text, disambiguation, n)

    @classmethod
    def testSerial(cls, port):
        try:
            s = Serial(port)
            s.close()
            return True
        except (OSError, SerialException):
            pass
        return False


    def __init__(self, app_dir, lang):
        '''Constructor'''
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.info('Construct')
        self.locale = None
        self._config = None
        self.app_dir = app_dir
        self.log_to_file = False
        self._dcom = None
        self._dapi = None
        self._board = None
        self._tracer = Tracer(self)
        self._db = Database(self)
        TellerInterface.__init__(self)

        self._initL10n(lang)


    def _initL10n(self, lang):
        '''Initialize the application localization

        Args:
            lang (str): If defined the language to use, otherwise the local session language.
        '''
        pass


    def _initDCom(self):
        if self.config.host is not None:
            return self._initDSocket()
        else:
            port = self.config.serial
            if not (os.path.exists(port) and BaseApp.testSerial(port)):
                self.sayError(BaseApp.tr('The configured serial port `{0!s}` is not available!'.format(port)))
                m0 = RE.match('(.*)(\d+)', self.config.serial)
                bport = m0.group(1)
                nport = int(m0.group(2))
                for i in range(nport+1, nport+10):
                    port = '{0:s}{1:d}'.format(bport, i)
                    if os.path.exists(port) and BaseApp.testSerial(port):
                        break
                    port = None

                if port is None:
                    raise Exception(BaseApp.tr('No available serial port found between {0:s}{1:d} and {0:s}{2:d} !').format(bport, nport, i) )
            return self._initDSerial(port)

    def _initDSerial(self, port):
        self.log.info('initDSerial')
        serial_port = Serial(port)
        serial_port.baudrate = self.config.baudrate
        serial_port.timeout = 5
        serial_port.stopbits = 1
        if self.config.trace:
            return dapi2.DSerial(serial_port, dapi2.DApi2Side.MASTER, trace_callback=self._tracer.traceDapi)
        else:
            return dapi2.DSerial(serial_port, dapi2.DApi2Side.MASTER, trace_callback=None)



    def _initDSocket(self):
        self.log.info('initDSocket')
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = self.config.host.split(":")

        if len(host) == 0:
            raise Exception(BaseApp.tr("No host specified"))
        elif len(host) == 1:
            host.append(30443)
        else:
            host[1] = int(host[1])

        skt.connect((host[0], host[1]))
        com = dapi2.DSocket(skt, dapi2.DApi2Side.MASTER, trace_callback=None)
        options = com.get_ext_conn()
        com.select_ext_conn(self.connectionCallback(options))
        return com



    def prepareCfg(self, parser, preconf):
        '''Prepare the argument structure of the application to be parsed by the :meth:`processCfg` method.

        Args:
            parser (.ArgumentParser): The parser to initialize.
            preconf (.Namespace): Global configuration parsed by launcher
        '''


        parser.add_argument("-l", "--log-level", dest="loglevel", choices=[ 'error', 'warning', 'debug', 'info', 'noset'], metavar='LOGLEVEL', default="info",
                             help=BaseApp.tr("Log level {%(choices)s}. (default = info)"))
        parser.add_argument("--log-file", dest="logfile", default='stderr',
                            help=BaseApp.tr("LOG file (default = stderr)") )
        parser.add_argument("--log-max-size", dest="log_maxbytes",
                            help=BaseApp.tr("Maximum LOG file size in bytes (default=100000)."), default=100000)
        parser.add_argument("--log-backup-count", dest="log_backupcount",
                            help=BaseApp.tr("Number of LOG files retained (default=10)."), default=10)
        parser.add_argument("-t", "--trace", dest="trace", action='store_true', default=False,
                            help=BaseApp.tr("If present, trace API message exchanges (default = not)"))

        dcom_grp = parser.add_mutually_exclusive_group(required=False)
        dcom_grp.add_argument("-S", "--serial", dest="serial", nargs='?', metavar="SERIAL", const='default', default="default",
                              help=BaseApp.tr("Serial port for direct control."))
        dcom_grp.add_argument("-H", "--host", dest="host", nargs='?', metavar="HOST", const='default',
                              help=BaseApp.tr("Host name and port for remote control. (host:port)"))

        parser.add_argument("--command-mode", dest="command_mode", action='store_true',default=True ,
                            help=BaseApp.tr("Sets the preferred DAPI2 mode to 'command'. (Default=command mode)"))
        parser.add_argument("-R", "--register-mode", dest="command_mode", action='store_false',
                            help=BaseApp.tr("Sets the preferred DAPI2 mode to 'register'. (Default=command mode)"))
        parser.add_argument("-D", "--dev-mode", dest="dev_mode", action='store_true', default=False,
                            help=BaseApp.tr("Sets DSMCP execution mode 'development'. (Default=normal mode)"))
        parser.add_argument("-A", "--access-level", dest="access_level", choices=dapi2.DApiAccessLevel.list(), metavar="ACCESS", default=None,
                            help=BaseApp.tr("Sets the access level for the connection to the board {{%(choices)s}}. (Default={})".format(self.DEFAULT_ACCESS_LEVEL.name if self.DEFAULT_ACCESS_LEVEL is not None else BaseApp.tr("not specified/unchanged"))))
        parser.add_argument("-b", "--baudrate", dest="baudrate", type=int, choices=dapi2.COM_SPEEDS, metavar="BAUDRATE", default=dapi2.COM_SPEEDS[0],
                            help=BaseApp.tr("Sets the serial port baud rate {{%(choices)s}}. (default: {0:d})".format(dapi2.COM_SPEEDS[0]) ))
        parser.add_argument("--version", action='version', version='%(prog)s version {0:s}'.format(self.version),
                            help=BaseApp.tr("Show software version"))
        parser.add_argument("--firm-paths", dest="firm_paths",
                            help=BaseApp.tr("Search paths for firmware binaries. The different paths are separated by a semicolon (;)"))

        self.prepareSpecificCfg(parser)


    def prepareSpecificCfg(self, parser):
        '''Prepare specific argument structure of the application to be parsed by the :meth:`processSpecificCfg` method.

        Args:
            parser (.ArgumentParser): The parser to initialize.

        Note:
            Call this method at the end of the derived method.
        '''
        pass

    def processCfg(self, parser, args):
        '''Parse the command line arguments and interpret the values

        Args:
            parser (ArgumentParser): The parser.
            args (Namespace): The arguments default values given by the configuration file (.ini)
        '''
        parser.set_defaults(**args)
        self._config = parser.parse_args()

        if self.config.loglevel:
            self.config.loglevel = getattr(logging, self.config.loglevel.upper())

        if self.config.verbosity is not None:
                try:
                    if isinstance(self.config.verbosity_cnt, int):
                        self.config.verbosity = VERBOSITY(self.config.verbosity)
                    elif self.config.verbosity.isdigit():
                        self.config.verbosity = VERBOSITY(str(self.config.verbosity))
                    else:
                        self.config.verbosity = VERBOSITY[self.config.verbosity.upper()]
                except:
                    self.config.verbosity = VERBOSITY.NONE

        if self.config.verbosity_cnt is not None:
            try:
                self.config.verbosity = VERBOSITY(self.config.verbosity_cnt)
            except:
                pass

        if 'firm_paths' in self.config and self.config.firm_paths is not None:
            self.config.firm_paths = self.config.firm_paths.split(';')  + FIRM_PATHS
        else:
            self.config.firm_paths = FIRM_PATHS


        if 'serial' in self.config and self.config.serial == 'default':
            self.config.serial = self.config.default_serial

        if 'host' in self.config and self.config.host == 'default':
            self.config.host = self.config.default_host


        if self.config.access_level is not None:
            self.config.access_level = dapi2.DApiAccessLevel[self.config.access_level.upper()]
        if not self.config.dev_mode and self.config.access_level is None:
            self.config.access_level = self.DEFAULT_ACCESS_LEVEL


        self.processSpecificCfg()

    def processSpecificCfg(self):
        '''Interpret the specific arguments value

        Note:
            Call this method at the end of the derived method.
        '''
        pass

    def prepareL10n(self, lang):
        '''Prepare the application localization

        Args:
            lang (str): If defined the language to use, otherwise the local session language.
        '''

        assert False, "Abstract method!"


    def connectionCallback(self, options):
        '''Callback function for the connection process

        Args:
            options (dist) : Some options
        '''
        assert False, "No overwritted func"

    def setBoard(self, board):
        '''Sets the board of application.

        Args:
            board (BaseDBoard): The board of application
        '''
        self._board = board

    def logEnvironment(self):
        pass

    def environmentCheck(self):
        self.log.debug('Environment control...')

    def startUp(self):
        '''Startup application

        Actions performed:

            - Application environment checking
            - Discovery and loading of the Dassym product database
            - Instantiation of the DAPI2 API (:class:`~dapi2.dapi2.DApi2`)
        '''
        self.log.debug('Start up application (BaseApp) v {} ...'.format(__version__))
        self.log.debug('Python version: {} ({})'.format( ".".join([str(x) for x in sys.version_info[:3]]) , platform.architecture()[0]))
        self.log.debug('OS: {}'.format(platform.platform()))
        self.logEnvironment()
        self.log.debug('PyDapi2:{0:s}'.format(dapi2.__version__))
        self.log.debug('Configuration:\n\t'+configStr(self.config))
        self._db.discover([USR_DATA_DIR] + self.config.firm_paths)
        self.sayMedium(BaseApp.tr('{:d} firmwares and {:d} customers have been identified.'.format(len(self._db.firmwares),len(self._db.customers))))
        self.environmentCheck()
        self.sayHigh('All checks on the application environment pass')
        self._dapi = dapi2.DApi2(self._dcom, dev_mode=self.isInDevMode() )
        self._tracer.dapi = self._dapi




    def initialize(self):
        '''Initialize the application

        Actions performed:

            - Instantiation of the communication object: a descendant of :class:`~dapi2.dcom.base.BaseDCom`.
            - Instantiation of the DAPI2 API (:class:`~dapi2.dapi2.DApi2`)
            - Instantiation of the object representing the electronic card: a descendant of :class:`dboard.base.BaseDBoard`.
        '''
        #self.sayMedium(BaseApp.tr("Start {0:s} v{1:s}").format("self.NAME", '000'))#__version__))
        self.log.debug('Initialize (BaseApp)...')



        #self.startUp()


    def connectBoard(self, level=None):
        '''Establishes the connection with the board.

        Args:
            level (DApiAccessLevel): If not None, sets the DAPI access level.

        Returns:
            float: The time to update all registers.
        '''

        self.log.debug('*** connectBoard ***')
        assert self._board is None

        if not self.config.command_mode:
            dmode = dapi2.DBoardPreferredDapiMode.REGISTER
        else:
            dmode = dapi2.DBoardPreferredDapiMode.COMMAND

        self._board = dapi2.DBoardFactory(self.dapi, dmode, self.sayLow)

        if self._board is not None:
            self.sayMedium(BaseApp.tr('Connection to the board...'))
            t = Stopwatch(autostart=True)
            self._board.initialize()
            t.stop()

            self.log.debug(f"Time to connect and update all registers: {t.time:0.4f}s")

            self.readWorkspaceMemmories()

            #TODO: m = BaseApp.tr("{a:s}@{b.name}:{b.sn:05d} through {s.name!s}@{s.baudrate:d}").format(
                    # a=self._board.access.name, b=self._board, s=self._board.com.serial)

            self._board.workspaceChanged.connect(self.onWorkspaceChanged)
            self._board.connectionChanged.connect(self.onConnectionChanged)

            if level is not None and self._board.getAccessLevel() != level:
                self._board.connect(level, level.passwd)
            self.sayMedium(BaseApp.tr("Link established with the access level {0!s}.").format(self._board.getAccessLevel().name))

            if not self.db.firmwares or (
                        self.db.board_class is not None and
                        not isinstance(self.board,self.db.board_class)
                        ):
                self.sayHigh(BaseApp.tr('Discovers firmwares...'))


        else:
            self.sayWarning(BaseApp.tr("No connection available. No card is connected!"))


        return t.time

    def disconnectBoard(self):
        self.log.debug('*** disconnectBoard ***')
        assert self._board is not None
        self._board.workspaceChanged.disconnect(self.onWorkspaceChanged)
        self._board.connectionChanged.disconnect(self.onConnectionChanged)

        del self._board
        self._board = None


    def readWorkspaceMemmories(self):
        if (not self.board.workspace.standby) and self.board.workspace.active:
            if self._board.getAccessLevel() >= dapi2.DApiAccessLevel.USER:
                self.sayHigh('Read memories ...')
                self.board.workspace.memories.readAll()


    def initComm(self):
        self.log.debug('initComm')
        assert self._dcom is None
        try:
            self._dcom = self._initDCom()
        except Exception as e:
            self._dcom = None
            if self.isInDevMode():
                self.displayError(e)
            else:
                raise e
        self._dapi.dcom = self._dcom
        # self._dapi = dapi2.DApi2(self._dcom, dev_mode=self.isInDevMode() )
        # self._tracer.dapi = self._dapi



    def stopComm(self):
        self.log.debug('stopComm')
        self.board.dapi.dcom.close()

        self.disconnectBoard()


    def startComm(self, access_level=None):
        assert self._dcom is not None
        self.log.debug('startComm')
        if not self.dcom.isOpen():
            self.sayLow(BaseApp.tr('Connecting...'))
            self.dcom.open()
            self.log.debug('Reset all local registers.')
            self.dapi.regs.disableEvents()
            self.dapi.regs.reset()
            self.dapi.regs.enableEvents()
        #if self.board is None or (self.board.getFactoryData() != self.board.getFactoryData(read=True)):
        return self.connectBoard(access_level)


    def changeWorkspace(self, workspace):
        self.log.debug(f"changeWorkspace({workspace!s}) ...")
        try:
            self.board.setWorkspace(workspace)
            self.sayLow(BaseApp.tr("Current workspace : {0!s}".format(workspace) ))
        except dapi2.DApiComAbortedError:
            err = self.board.getError(refresh=True)
            self.sayError(BaseApp.tr("Workspace change aborted! Error : 0x{0:02X}".format(err) ))

    def onWorkspaceChanged(self, workspace):
        self.log.debug(f"onWorkspaceChanged({workspace!s})")
        self.board.refreshHeader()
        self.board.refreshState()
        if self.board.workspace.isFunctional():
            self.board.refreshSetpoints()
            self.readWorkspaceMemmories()

    def onConnectionChanged(self, state, level):
        self.log.debug(f"onConnectionChanged({state!s}, {level!s})")
        pass

    def isGui(self):
        assert False, 'Abstract method!'

    def isCli(self):
        return not self.isGui()

    def run(self):
        '''Run this application'''
        assert False, 'Abstract method!'
        return 0

    def terminate(self, exit_code=0):
        '''Terminates application

        Args:
            exit_code (int): If >0 : exit the application immediately with code `exit_code`.
        '''
        try:
            self.sayMedium(BaseApp.tr('Finished')+"("+str(exit_code)+")")
        except:
            pass
        if exit_code > 0:
            exit(exit_code)

    def displayError(self, error):
        '''Display the given error

        Args:
            error (str): The error message
        '''
        self.sayError(error)

    def errorInfo(self):
        return (
            ('Trace'      , str(traceback.format_exc())),
            ('Application',' {0!s} {1!s} ({2!s})'.format(self.name, self.version, APP_DATE.isoformat())),
            ('Python'     , (".".join([str(x) for x in sys.version_info[:3]]))+" - " +platform.architecture()[0] ),
            ('Station'    , "{0!s} / {1!s}".format(platform.node(), platform.platform())),
            ('User'       , getpass.getuser()),
            ('Serial lib' , serial.__version__),
            ('DAPI2'      , f"{dapi2.__version__} ({dapi2.__date__})"),
            )


    def handleError(self, exception):
        '''Handling an error or exception

        Args:
            e (Exception): the exception to be processed
        '''
        txt = str(exception)
        self.displayError(txt)
        txt += '\n-------\n'+'\n'.join( "{}: {}".format(*x) for x in self.errorInfo())
        txt += '\n-------\n'
        self.log.error(txt)
        self.terminate(1)

    def isConnected(self):
        '''Check if the communication channel is open

        Returns:
            bool : True, the communication channel is open ; False, otherwise.
        '''
        return self._dcom.isOpen()

    def isInDevMode(self):
        '''Check if the application is executed in development mode

        Returns:
            bool : True, if the application is executed in development mode ; False, otherwise.
        '''
        return self.config.dev_mode

    def getImageDir(self):
        '''Returns the path to the images directory

        Returns:
            str: The images directory path
        '''
        return IMG_DIR

    def getFirmwareDir(self):
        '''Returns the path to the firmwares directory

        Returns:
            str: The firmwares directory path
        '''
        return FIRM_DIR

    def getTempDir(self):
        '''Returns directory for temporary files

        Returns:
            str: The temporary directory path
        '''
        return TEMP_DIR

    def getUserDataDir(self):
        '''Returns the path to the user data directory

        Returns:
            str: The user data directory path
        '''
        return USR_DATA_DIR

    @property
    def name(self):
        '''The application's name'''
        return self.NAME

    @property
    def version(self):
        '''The application's version'''
        return __version__

    @property
    def config(self):
        '''The application's configuration'''
        return self._config


    @property
    def dapi(self):
        '''The :class:`.dapi2.DApi2` linked to application'''
        return self._dapi
    @property
    def board(self):
        '''The :class:`~.dboard.base.BaseDBoard` linked to application'''
        return self._board
    @property
    def dcom(self):
        '''The :class:`~.dapi2.dcom.base.BaseDCom` linked to application'''
        return self._dcom

    @property
    def db(self):
        '''The :class:`.Database` linked to application'''
        return self._db

    @property
    def tracer(self):
        '''The :class:`~dsmcp.app.tracer.Tracer` linked to application'''
        return self._tracer

    @property
    def lang(self):
        return self.locale.name().split('_')[0]
