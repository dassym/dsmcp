'''

:author: fv
:date: Created on 19 mars 2021
'''


import argparse
import configparser
import os

from .common import APP_NAME
from ._version import __version__
from .base import BaseApp



class Launcher(object):
    '''class used to launch the application
    
    :param str app_dir: The application root directory.
    '''
    def __init__(self, app_dir, add_help=False):
        
        self.app_dir = app_dir
        self.add_help=add_help
        self.args_config = {}
        self.parser = None
        self._parser0 = None
        self._initCfg()
        
    
    def _initCfg(self):
        self._parser0 = argparse.ArgumentParser(description='{0:s} (v{1:s})'.format(APP_NAME, __version__), add_help=self.add_help)
        self._parser0.add_argument("-c", "--config", dest="config", help = BaseApp.tr("Configuration file (.ini)") )
        self._parser0.add_argument("--no-gui", dest="no_gui", action='store_true', default=False, help = BaseApp.tr("If present start no GUI application") )  
        self._parser0.add_argument("--qt5-options", dest="qt5_options", help = BaseApp.tr("Qt5 options") )
        self._parser0.add_argument("--lang", dest="lang", help=BaseApp.tr("ISO name of language to use."))
        verbosity_grp = self._parser0.add_mutually_exclusive_group()
        verbosity_grp.add_argument("-v", dest="verbosity_cnt", action="count", help=BaseApp.tr("Verbosity level (default=none)."))
        verbosity_grp.add_argument("--verbosity", dest="verbosity", help=BaseApp.tr("Verbosity level (default=0:none)."), default=0)

        
    def preConfig(self):
        '''Pre-configuration of application with the already defined arguments''' 
        self.config, remaining_argv0 = self._parser0.parse_known_args() #@UnusedVariable
        
        if self.config.config is not None:
            
            if os.path.dirname(self.config.config) == '':
                self.config.config = os.path.join(self.app_dir, self.config.config )
            
            if not os.path.exists(self.config.config):
                raise Exception(BaseApp.tr("Configuration file not found!"))
            cfg = configparser.ConfigParser()
            cfg.read(self.config.config,encoding='utf_8_sig')  
    
            for section in cfg.sections() :
                if section == 'GLOBAL':
                    prefix = ''
                else:
                    prefix = section.lower()+'_'
                for k in cfg[section]:
                    v = cfg[section][k]
                    if v.lower() in ('yes', 'true'):
                        v = True
                    elif v.lower() in ('no', 'false'):
                        v = False
                    
                    self.args_config[prefix+k] = v
                    
        self.parser = argparse.ArgumentParser( parents=[self._parser0], add_help=not self.add_help)
        
        
    def launch(self, app_class):
        '''Create and launch the application
        
        :param BaseApp app_class: The applications's class to create an launch.
        :return: The application
        '''
        app = app_class(self.app_dir)
        app.prepareL10n(self.config.lang)
        app.prepareCfg(self.parser)
        app.processCfg(self.parser, self.args_config)
        app.initLog()
        return app
    
    @property
    def parser0(self):
        return self._parser0
    
#===============================================================================
# 
# 
# def prepareCfg():
#     #global log, args_config, config, initial_dir
#     
#     parser0 = argparse.ArgumentParser(description='{0:s} (v{1:s})'.format(app.APP_NAME, app.__version__), add_help=False)
#     parser0.add_argument("-c", "--config", dest="config", help = tr("Configuration file (.ini)") )
#     parser0.add_argument("--no-gui", dest="no_gui", action='store_true', default=False, help = tr("If present start no GUI application") )  
#     parser0.add_argument("--qt5-options", dest="qt5_options", help = tr("Qt5 options") )
#     parser0.add_argument("--lang", dest="lang", help=tr("ISO name of language to use."))
#     parser0.add_argument("-v", "--verbosity", action="count", help=tr("Verbosity level (default=0)."), default=0)
#     
#     app.config, remaining_argv0 = parser0.parse_known_args() #@UnusedVariable
#     
#     if app.config.config is not None:
#         
#         if os.path.dirname(app.config.config) == '':
#             app.config.config = os.path.join(app.initial_dir, app.config.config )
#         
#         if not os.path.exists(app.config.config):
#             raise Exception(tr("Configuration file not found!"))
#         cfg = configparser.ConfigParser()
#         cfg.read(app.config.config,encoding='utf_8_sig')  
# 
#         for section in cfg.sections() :
#             if section == 'GLOBAL':
#                 prefix = ''
#             else:
#                 prefix = section.lower()+'_'
#             for k in cfg[section]:
#                 v = cfg[section][k]
#                 if v.lower() in ('yes', 'true'):
#                     v = True
#                 elif v.lower() in ('no', 'false'):
#                     v = False
#                 
#                 app.args_config[prefix+k] = v
# 
#     app.parser = argparse.ArgumentParser( parents=[parser0] )
#     
#     app.parser.add_argument("-l", "--log-level", dest="loglevel", choices=[ 'error', 'warning', 'debug', 'info', 'noset'], help=tr("Log level. (default = info)"), default="info"   )
#     app.parser.add_argument("--log-file", dest="logfile", default='stderr', help=tr("LOG file (default = stderr)") )
#     app.parser.add_argument("--log-max-size", dest="log_maxbytes", help=tr("Maximum LOG file size in bytes (default=100000)."), default=100000)
#     app.parser.add_argument("--log-backup-count", dest="log_backupcount", help=tr("Number of LOG files retained (default=10)."), default=10)
#     app.parser.add_argument("-t", "--trace", dest="trace", action='store_true', help=tr("If present, trace API message exchanges (default = not)"), default=False )
#     
#     
#     dcom_grp = app.parser.add_mutually_exclusive_group(required=True)
#     dcom_grp.add_argument("-S", "--serial", dest="serial", help=tr("Serial port for direct control."), metavar="SERIAL")
#     dcom_grp.add_argument("-H", "--host", dest="host", help=tr("Host name and port for remote control. (host:port)"), metavar="HOST")
#     
#     app.parser.add_argument("-C", "--command-mode", dest="command_mode", action='store_true', help=tr("Sets the preferred DAPI2 mode to 'command'. (Default=command mode)"),default=True )
#     app.parser.add_argument("-R", "--register-mode", dest="command_mode", action='store_false', help=tr("Sets the preferred DAPI2 mode to 'register'. (Default=command mode)"))
#     app.parser.add_argument("-D", "--dev-mode", dest="dev_mode", action='store_true', help=tr("Sets DSMCP execution mode 'development'. (Default=normal mode)"))
# 
#     app.parser.add_argument("-b", "--baudrate", dest="baudrate", type=int, help=tr("Baud rate. (default: {0})".format(dapi2.COM_SPEEDS[0]) ), metavar="BAUDRATE", default=dapi2.COM_SPEEDS[0])
#     app.parser.add_argument("-v", "--version", action='version',  help=tr("Show software version"), version='%(prog)s version {0:s}'.format(app.__version__)   )
#     app.parser.add_argument("--firm-paths", dest="firm_paths", help=tr("Search paths for firmware binaries. The different paths are separated by a semicolon (;)"))
#     app.parser.add_argument("--registers",  help=tr("The XML registers definition file"), dest="regfile",  default="data:dapi-registers.xml" )
#     app.parser.add_argument("--layout",  help=tr("The GUI layout name or SVG file. (default: vantage)"), dest="layout", default="vantage")
#     
#     
# def processCfg():   
#     
#     app.parser.set_defaults(**app.args_config)
#     app.config = app.parser.parse_args()
#     
#     
#     if app.config.loglevel:
#         app.config.loglevel = getattr(logging, app.config.loglevel.upper())
#     
#     app.log = logging.getLogger()
#     
#     if app.config.logfile is None or app.config.logfile == 'stderr':
#         log_handler = logging.StreamHandler(sys.stderr)
#     elif app.config.logfile == 'stdout':
#         log_handler = logging.StreamHandler(sys.stdout)
#     else:
#         if os.path.dirname(app.config.logfile) != '':
#             logfile = os.path.normpath(app.config.logfile)
#         else:
#             logfile = os.path.normpath(os.path.join(app.DEFAULT_LOG_DIR, app.config.logfile))
#             
#         log_handler = logging.handlers.RotatingFileHandler( filename=logfile, maxBytes=app.config.log_maxbytes, backupCount=app.config.log_backupcount)
# 
#     if app.config.verbosity:
#             try:
#                 if isinstance(app.config.verbosity, int):
#                     app.config.verbosity = VERBOSITY(app.config.verbosity)
#                 elif app.config.verbosity.isdigit():
#                     app.config.verbosity = VERBOSITY(str(app.config.verbosity))
#                 else:
#                     app.config.verbosity = VERBOSITY[app.config.verbosity]
#             except:
#                 app.config.verbosity = VERBOSITY.NONE
#     
#     
#     if 'firm_paths' in app.config and app.config.firm_paths is not None:
#         app.config.firm_paths = app.config.firm_paths.split(';') 
#     else:
#         app.config.firm_paths = []
#         
# 
# 
# 
#     app.log.setLevel(app.config.loglevel)
#     logfmt = logging.Formatter(app.LOG_FORMAT)
#     log_handler.setFormatter(logfmt)   
#     app.log.addHandler(log_handler)
#===============================================================================
    

# def initialize():
    # assert app.application is None
    # try:
        # app.log.info(tr('Start {}  v{}').format(app.NAME, app.VERSION))
        # app.log.debug(tr('Python version: {} ({})').format( ".".join([str(x) for x in sys.version_info[:3]]) , platform.architecture()[0]))
        # app.log.debug(tr('OS: {}').format(platform.platform()))
        # app.log.debug(tr('Configuration:\n\t') + app.utils.configStr(app.config)  )
        #
        # if app.config.no_gui:
            # app.application = BaseCliApp(app.config)
        # else:
            # raise Exception("GUI not yet implemanted!")
            # #TODO:app.application = GuiApp(config) 
            #
        # app.application.initialize()
        #
    # except Exception as e:
        # handleException(e)
        #
# def run():
    # assert app.application is not None
    # try:
        # app.log.info( tr('Run {}').format(app.NAME) )
        # return app.application.run()
    # except Exception as e:
        # handleException(e)
        #
# def terminate():
    #
    # assert app.application is not None
    #
    # app.application.terminate()
    #
    # try:
        # app.log.info( tr('End {0!s} ({1:d}).').format(app.NAME, app.exit_code) )
    # except Exception as e:
        # handleException(e)
    
# def handleException(e):
    # if app.log:
        # app.log.error(tr('Error*:')+str(e))
    # else:
        # print(tr('Error*:')+str(e), file=sys.stderr)
    # if app.config.loglevel == logging.DEBUG:
        # s = traceback.format_exc()
        # if s and app.log:
            # app.log.error(tr('Trace\n')+ str(s))
        # else:
            # print(tr('Trace\n')+ str(s), file=sys.stderr)
    # ## Boîte de dialogue pour l'affichage de'erreur
    # if isinstance(app.application, QApplication):
        # dialog = QMessageBox(QMessageBox.Critical, app.NAME+tr('Error:'), tr("An error has occurred!\nDetail:\n")+str(e), QMessageBox.Ok )
        # dialog.exec()
    # if app.exit_code == 0:
        # app.exit_code=9
        #
    # sys.exit(app.exit_code)

