'''

:author: fv
:date: Created on 19 mars 2021
'''
import logging.handlers
import os.path
import re as RE
from serial import Serial
import traceback
import platform
import getpass
import sys
import socket
from PyQt5.QtCore import QCoreApplication, QLocale, QTranslator,\
    QLibraryInfo, QT_VERSION_STR, PYQT_VERSION_STR


import dapi2, dboard
from .tracer import Tracer
from dapi2.dcom.dsocket import DSocket
from .common import IMG_DIR, FIRM_DIR, TEMP_DIR, USR_DATA_DIR, APP_NAME, VERBOSITY, LOG_FORMAT, DEFAULT_LOG_DIR
from ._version import __version__
from .firmware import Firmwares
from .utils import configStr
 
class BaseApp(object):
    '''Base class for *dsmcp* applications
    
    :param str app_dir: The application root directory.
    
    '''
    
    NAME = APP_NAME

    @classmethod
    def tr(cls, text, disambiguation=None, n=-1):
        return QCoreApplication.translate('BaseApp',text, disambiguation, n)

    

    def __init__(self, app_dir):
        '''
        Constructor
        '''
        self.log = logging.getLogger(self.__class__.__name__)
        self.config = None
        self.app_dir = app_dir
        self.log_to_file = False
        self._dcom = None
        self._dapi = None
        self._board = None
        self._tracer = Tracer(self) 
        self._firmwares = Firmwares(self)
        
        #self._board = Board92(self, self.registers)


    def _initDCom(self):
        if self.config.host is not None:
            return self._initDSocket()
        else:
            port = self.config.serial
            if not os.path.exists(self.config.serial):
            
                m0 = RE.match('(.*)(\d+)', self.config.serial)
                bport = m0.group(1)
                nport = int(m0.group(2)) 
                for i in range(nport, nport+10):
                    port = '{0:s}{1:d}'.format(bport, i)
                    if os.path.exists(port):
                        break
                    port = None
            
                if port is None:
                    raise Exception(BaseApp.tr('No serial port found between {0:s}{1:d} and {0:s}{2:d} !').format(bport, nport, i) )
            
            
            
            return self._initDSerial(port)
    
    def _initDSerial(self, port):
        serial_port = Serial(port)
        serial_port.baudrate = self.config.baudrate
        serial_port.timeout = 5
        serial_port.stopbits = 1
        if self.config.trace:  
            return dapi2.DSerial(serial_port, dapi2.DApi2Side.MASTER, trace_callback=self._tracer.traceDapi)
        else:
            return dapi2.DSerial(serial_port, dapi2.DApi2Side.MASTER, trace_callback=None)

        
          
    def _initDSocket(self):
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = self.config.host.split(":")
        
        if len(host) == 0:
            raise Exception("No host specified")
        elif len(host) == 1:
            host.append(30443)
        else:
            host[1] = int(host[1])
        
        skt.connect((host[0], host[1]))
        com = DSocket(skt, dapi2.DApi2Side.MASTER, trace_callback=None)
        options = com.get_ext_conn()
        com.select_ext_conn(self.connectionCallback(options))
        return com
    
    
    
    def prepareCfg(self, parser):
        '''Prepare the argument structure of the application to be parsed by the :meth:`processCfg` method.
        
        :param ArgumentParser parser: The parser to initialize.
        '''
    
        parser.add_argument("-l", "--log-level", dest="loglevel", choices=[ 'error', 'warning', 'debug', 'info', 'noset'], help=BaseApp.tr("Log level. (default = info)"), default="info"   )
        parser.add_argument("--log-file", dest="logfile", default='stderr', help=BaseApp.tr("LOG file (default = stderr)") )
        parser.add_argument("--log-max-size", dest="log_maxbytes", help=BaseApp.tr("Maximum LOG file size in bytes (default=100000)."), default=100000)
        parser.add_argument("--log-backup-count", dest="log_backupcount", help=BaseApp.tr("Number of LOG files retained (default=10)."), default=10)
        parser.add_argument("-t", "--trace", dest="trace", action='store_true', help=BaseApp.tr("If present, trace API message exchanges (default = not)"), default=False )
        
        dcom_grp = parser.add_mutually_exclusive_group(required=True)
        dcom_grp.add_argument("-S", "--serial", dest="serial", help=BaseApp.tr("Serial port for direct control."), metavar="SERIAL")
        dcom_grp.add_argument("-H", "--host", dest="host", help=BaseApp.tr("Host name and port for remote control. (host:port)"), metavar="HOST")
        
        parser.add_argument("-C", "--command-mode", dest="command_mode", action='store_true', help=BaseApp.tr("Sets the preferred DAPI2 mode to 'command'. (Default=command mode)"),default=True )
        parser.add_argument("-R", "--register-mode", dest="command_mode", action='store_false', help=BaseApp.tr("Sets the preferred DAPI2 mode to 'register'. (Default=command mode)"))
        parser.add_argument("-D", "--dev-mode", dest="dev_mode", action='store_true', help=BaseApp.tr("Sets DSMCP execution mode 'development'. (Default=normal mode)"), default=False)
            
        parser.add_argument("-b", "--baudrate", dest="baudrate", type=int, help=BaseApp.tr("Baud rate. (default: {0})".format(dapi2.COM_SPEEDS[0]) ), metavar="BAUDRATE", default=dapi2.COM_SPEEDS[0])
        parser.add_argument("--version", action='version',  help=BaseApp.tr("Show software version"), version='%(prog)s version {0:s}'.format(__version__)   )
        parser.add_argument("--firm-paths", dest="firm_paths", help=BaseApp.tr("Search paths for firmware binaries. The different paths are separated by a semicolon (;)"))
        parser.add_argument("--registers",  help=BaseApp.tr("The XML registers definition file"), dest="regfile",  default="data:dapi-registers.xml" )
        
        self.prepareSpecificCfg(parser)
        
    def prepareSpecificCfg(self, parser):
        pass
        
    def processCfg(self, parser, args):   
        '''Parse the command line arguments and 
        
        :param ArgumentParser parser: The parser.
        :param Namespace args: The arguments default values given by the configuration file (.ini)
        '''
        parser.set_defaults(**args)
        self.config = parser.parse_args()
        
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
            self.config.firm_paths = self.config.firm_paths.split(';') 
        else:
            self.config.firm_paths = []
            
        self.processSpecificCfg()
            
    def processSpecificCfg(self):
        pass   
     
    def initLog(self):
        '''Initialize the application logger'''
        
        if self.config.logfile is None or self.config.logfile == 'stderr':
            log_handler = logging.StreamHandler(sys.stderr)
        elif self.config.logfile == 'stdout':
            log_handler = logging.StreamHandler(sys.stdout)
        else:
            if os.path.dirname(self.config.logfile) != '':
                logfile = os.path.normpath(self.config.logfile)
            else:
                logfile = os.path.normpath(os.path.join(DEFAULT_LOG_DIR, self.config.logfile))
            log_handler = logging.handlers.RotatingFileHandler( filename=logfile, maxBytes=self.config.log_maxbytes, backupCount=self.config.log_backupcount)
            self.log_to_file = True
    
        self.log.setLevel(self.config.loglevel)
        logfmt = logging.Formatter(LOG_FORMAT)
        log_handler.setFormatter(logfmt)   
        self.log.addHandler(log_handler)
            
    def prepareL10n(self, lang):
        '''Prepare the application localization
        
        :param str lang: If defined the language to use, otherwise the local session language.
        ''' 
        
        if lang:
            self.locale = QLocale(lang)
        else:
            self.locale = QLocale.system()
        self._qtTranslator = QTranslator()
        self._qtBaseTranslator = QTranslator()
        self._qtAppTranslator = QTranslator()        
        
        s = QLibraryInfo.location(QLibraryInfo.TranslationsPath)

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

            
            
    def connectionCallback(self, options):
        assert False, "No overwritted func"
        
    def setBoard(self, board):
        '''Sets the board of application.
        
        :param BaseDBoard board: The board of application
        ''' 
        self._board = board
        
    def initialize(self):
        '''Initialize the application
        
        Actions performed:
        
            - Instantiation of the communication object: a descendant of :class:`~dapi2.dcom.base.BaseDCom`.
            - Instantiation of the DAPI2 API (:class:`~dapi2.dapi2.DApi2`)
            - Instantiation of the object representing the electronic card: a descendant of :class:`dboard.base.BaseDBoard`.
        '''
        self.sayMedium(BaseApp.tr("Start {0:s} v{1:s}").format(self.NAME, __version__))
        self.log.debug('Initialize...')
        self.log.debug('Python version: {} ({})'.format( ".".join([str(x) for x in sys.version_info[:3]]) , platform.architecture()[0]))
        self.log.debug('OS: {}'.format(platform.platform()))
        self.log.debug('Qt version:{0!s}'.format(QT_VERSION_STR))
        self.log.debug('PyQt version:{0!s}'.format(PYQT_VERSION_STR))
        self.log.debug('Qt locale:`{0!s}` ; decimal: `{1!s}` : language: {2!s}'.format(self.locale.name(), self.locale.decimalPoint(), self.locale.bcp47Name()))
        self.log.debug('PyDapi2:{0:s}'.format(dapi2.__version__))
        
        self.log.debug('Configuration:\n\t'+configStr(self.config))
        
        self.sayHigh(BaseApp.tr('Connecting...'))
        self._dcom = self._initDCom()
        self._dapi = dapi2.DApi2(self._dcom, dev_mode=self.isInDevMode() )
        self._tracer.dapi = self._dapi
        if not self.config.command_mode:
            dmode = dboard.DBoardPreferedDapiMode.REGISTER
        else:
            dmode = dboard.DBoardPreferedDapiMode.COMMAND
        self._board = dboard.DBoardFactory(self.dapi, dmode, self.sayLow)
        
        #TODO: m = BaseApp.tr("{a:s}@{b.name}:{b.sn:05d} through {s.name!s}@{s.baudrate:d}").format(
                # a=self._board.access.name, b=self._board, s=self._board.com.serial)
        self.sayMedium(BaseApp.tr("Connected."))
        self.board.initialize()
        self._firmwares.discover(self.config.firm_paths, self.board)
        
        
         
        
        
    def run(self):
        '''Run this application''' 
        return 0
        
    def terminate(self, exit_code=0):
        '''Terminates application'''
        try:
            self.sayMedium(BaseApp.tr('Finished')+"("+str(exit_code)+")")
        except:
            pass
        if exit_code > 0:
            exit(exit_code)
            
    def say(self, level, text):
        '''Display text on stdout
        
        :param VERBOSITY level: The level needed to display this text.
        :param str text: Text to display.
        '''
        if self.config.verbosity >= level:
            print( text )
            if self.log_to_file:
                if level >= VERBOSITY.MEDIUM:
                    self.log.debug( text )
                else:
                    self.log.info( text )
        else:
            if level >= VERBOSITY.MEDIUM:
                self.log.debug( text )
            else:
                self.log.info( text )
        
    def sayMinimal(self, text):
        self.say(VERBOSITY.MINIMAL, text)
    def sayLow(self, text):
        self.say(VERBOSITY.LOW, text)
    def sayMedium(self, text):
        self.say(VERBOSITY.MEDIUM, text)
    def sayHigh(self, text):
        self.say(VERBOSITY.HIGH, text)
      
    def sayError(self, text):
        if self.config.verbosity >= VERBOSITY.MINIMAL:
            print( self.tr('ERROR:')+str(text) )
            if self.log_to_file:
                self.log.error(text)
        else:
            self.log.error(text)
            
    def sayWarning(self, text):
        if self.config.verbosity >= VERBOSITY.MINIMAL:
            print( self.tr('WARNING:')+str(text) )
            if self.log_to_file:
                self.log.warning(text)
        else:
            self.log.warning(text)        
            
         
            
    def displayError(self, error):
        '''Display the given error
        
        :param str error: The error message''' 
        self.sayError(error)
        
        
    def handleError(self, exception):
        '''Handling an error or exception
        :param Exception e: the exception to be processed
        '''
        txt = str(exception)
        self.displayError(txt)
        txt += '\n'+ str(traceback.format_exc())
        txt += '\n{0!s} : {1!s}'.format(self.applicationName(), self.applicationVersion())
        txt += '\nPython : {0!s}'.format( ".".join([str(x) for x in sys.version_info[:3]]) )
        txt += '\nStation : {0!s} / {1!s}'.format(platform.node(), platform.platform())
        txt += '\nUser : {0!s}'.format(getpass.getuser())
        self.log.error(txt)
        self.terminate(1)
        
    def isConnected(self):
        '''Check if the communication channel is open
        
        :return: True, the communication channel is open ; False, otherwise.
        :rtype: bool
        '''
        return self._dcom.isOpen()
    
    def isInDevMode(self):
        '''Check if the application is executed in development mode
        
        :return: True, if the application is executed in development mode ; False, otherwise.
        :rtype: bool
        '''
        return self.config.dev_mode
        
    def getImageDir(self):
        '''Return the directory where the images are stored'''
        return IMG_DIR
    
    def getFirmwareDir(self):
        '''returns the directory where the firmware is stored'''
        return FIRM_DIR
    
    def getTempDir(self):
        '''return directory for temporary files'''
        return TEMP_DIR
    
    def getUserDataDir(self):
        '''returns the user data directory'''
        return USR_DATA_DIR
        
    @property
    def name(self):
        '''The application's name'''
        return 
            
    @property
    def dapi(self):
        '''The :class:`~dapi2.dapi2.DApi2` linked to application'''
        return self._dapi
    @property
    def board(self):
        '''The :class:`~dboard.base.BaseDBoard` linked to application'''
        return self._board
    @property
    def dcom(self):
        '''The :class:`~dapi2.dcom.base.BaseDCom` linked to application'''
        return self._dcom
    
    @property
    def tracer(self):
        '''The :class:`~dsmcp.app.tracer.Tracer` linked to application'''
        return self._tracer
    @property
    def firmwares(self):
        return self._firmwares
