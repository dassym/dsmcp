'''

:author: fv
:date: Created on 19 mars 2021
'''


import argparse
import configparser
import logging
import os
from shutil import copyfile
import sys

from .version import __version__, DATE  # @UnresolvedImport
from .common import APP_NAME, CONFIG_PATHS, DEFAULT_SERIAL, DEFAULT_HOST, \
    DEFAULT_LOG_DIR, LOG_FORMAT, USR_FIRM_DIR, DEFAULT_APP_CONFIG, \
    USR_DATA_APP_DIR, USR_DATA_DIR, DEFAULT_USR_CONFIG, OS_DEFAULT_CCONFIG_NAME
from .teller import TellerInterface
from .base import BaseApp
import shutil


class Launcher(TellerInterface):
    '''class used to launch the application
    
    :param str app_dir: The application root directory.
    '''
    
    @classmethod
    def tr(cls, text, disambiguation=None, n=-1):
        return text
    
        
    def __init__(self, app_dir, add_help=False):
        '''Constructor'''
        
        TellerInterface.__init__(self)
        self.app_dir = app_dir
        self.add_help=add_help
        self.args_config = {}
        self.log = logging.getLogger()
        self.parser = None
        self._parser0 = None
        self._parser1 = None
        self._initCfg()
        
        for p in [USR_DATA_DIR, USR_DATA_APP_DIR, USR_FIRM_DIR]:
            if not os.path.exists(p):
                try:
                    os.mkdir(p)
                except OSError:
                    self.sayError("Creation of the directory `{0!s}` failed".format(p))
                else:
                    self.sayMedium("Successfully created the directory `{0!s}`".format(p))

    
    def _initCfg(self):
        self._parser0 = argparse.ArgumentParser(
                    description="""The dsmcp package which provides a family of human-machine interface applications for Dassym electronic boards.
Version: {1:s}
""".format(APP_NAME, __version__),
                    add_help=self.add_help,
                    formatter_class=argparse.RawTextHelpFormatter,
                    epilog="""Licence: ©Dassym SA {dy:s}
         This program is free software under the terms of the GNU General Public License verion 3. 
""".format(dy=DATE.strftime('%Y'))
                )
        self._parser0.add_argument("-c", "--config", dest="config", help = BaseApp.tr("Configuration file (.ini)"), default=DEFAULT_USR_CONFIG )
        #self._parser0.add_argument("--no-gui", dest="no_gui", action='store_true', default=False, help = BaseApp.tr("If present start no GUI application") )  
        self._parser0.add_argument("--qt5-options", dest="qt5_options", help = BaseApp.tr("Qt5 options") )
        # Ajout d'une ligne ici pour les paramètres du fichier python 
        
        gui_grp = self._parser0.add_mutually_exclusive_group()
        gui_grp.add_argument("--cli", dest="gui", action='store_false', default=True, help=BaseApp.tr("If present, launches the application without the graphical user interface (default)"))
        gui_grp.add_argument("--gui", dest="gui", action='store_true', default=True, help=BaseApp.tr("If present, launches the application with the graphical user interface (default:witout GUI)"))
        
        self._parser0.add_argument("--lang", dest="lang", help=BaseApp.tr("ISO name of language to use."))
        verbosity_grp = self._parser0.add_mutually_exclusive_group()
        verbosity_grp.add_argument("-v", dest="verbosity_cnt", action="count", help=BaseApp.tr("Verbosity level (default=none)."))
        verbosity_grp.add_argument("--verbosity", dest="verbosity", help=BaseApp.tr("Verbosity level (default=0:none)."), default=0)
        
        self._parser0.add_argument("--default-serial", dest="default_serial", help=BaseApp.tr("Default serial port."), default=DEFAULT_SERIAL)
        self._parser0.add_argument("--default-host", dest="default_host", help=BaseApp.tr("Default host address and port (host:port)."), default=DEFAULT_HOST)
        
    def preConfig(self):
        '''Pre-configuration of application with the already defined arguments''' 
        self.config, remaining_argv0 = self._parser0.parse_known_args() #@UnusedVariable
        fconfig = None  
        if self.config.config is not None:
            if os.path.dirname(self.config.config) == '':
                for path in CONFIG_PATHS+[self.app_dir]:
                    fconfig = os.path.join(path, self.config.config )
                    if os.path.exists(fconfig): 
                        self.config.config = fconfig
                        break
                if fconfig is None:
                    raise Exception(BaseApp.tr("The configuration file {0!s} was not found in paths {1:s}!".format(self.config.config, '; '.join(CONFIG_PATHS+[self.app_dir]) )))
                        
            
            if not os.path.exists(self.config.config):
                self.sayWarning(BaseApp.tr("Create default configuration file `{0!s}`").format(DEFAULT_USR_CONFIG))
                try:
                    copyfile(DEFAULT_APP_CONFIG, DEFAULT_USR_CONFIG)
                except OSError:
                    raise Exception(BaseApp.tr("Configuration file not found and copying of the default `{0!s}` failed!".format(DEFAULT_USR_CONFIG)))
                else:
                    self.sayMedium("Successfully copied the default ini file to `{0!s}`".format(DEFAULT_USR_CONFIG))
                
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
                    
        self._parser1 = argparse.ArgumentParser( parents=[self._parser0],
                        add_help=self.add_help,
                        formatter_class=argparse.RawTextHelpFormatter,
                        epilog="""Licence: ©Dassym SA {dy:s}
         This program is free software under the terms of the GNU General Public License verion 3. 
""".format(dy=DATE.strftime('%Y'))
                        )
        self._parser1.set_defaults(**self.args_config)
        self.config, remaining_argv0 = self._parser1.parse_known_args() #@UnusedVariable
        
    def initLog(self,app):
        '''Initialize the application logger'''
        if app.config.logfile is None or app.config.logfile == 'stderr':
            log_handler = logging.StreamHandler(sys.stderr)
        elif app.config.logfile == 'stdout':
            log_handler = logging.StreamHandler(sys.stdout)
        else:
            if os.path.dirname(app.config.logfile) != '':
                logfile = os.path.normpath(app.config.logfile)
            else:
                logfile = os.path.normpath(os.path.join(DEFAULT_LOG_DIR, app.config.logfile))
            log_handler = logging.handlers.RotatingFileHandler( filename=logfile, maxBytes=app.config.log_maxbytes, backupCount=app.config.log_backupcount)
            self.log_to_file = True
        
        self.log.setLevel(app.config.loglevel)
        logfmt = logging.Formatter(LOG_FORMAT)
        log_handler.setFormatter(logfmt)   
        self.log.addHandler(log_handler)        
        
    def launch(self, app_class):
        '''Create and launch the application
        
        :param BaseApp app_class: The applications's class to create an launch.
        :return: The application
        '''
        app = app_class(self.app_dir, self.config.lang)
        #app.prepareL10n(self.config.lang)
        
        self.parser = argparse.ArgumentParser( parents=[self._parser0],
                        add_help=not self.add_help,
                        formatter_class=argparse.RawTextHelpFormatter,
                        description="""Application {0:s} (v{1:s})
This application is part of the dsmcp package which provides a family of human-machine interface applications for Dassym electronic boards.
""".format(app.name, app.version),
                        epilog="""Licence: ©Dassym SA {dy:s}
         This program is free software under the terms of the GNU General Public License verion 3. 
""".format(dy=DATE.strftime('%Y'))
                        )
        
        app.prepareCfg(self.parser, self.config)
        app.processCfg(self.parser, self.args_config)
        self.initLog(app)
        return app
    
    
    def isCli(self):
        return True
    
    @property
    def parser0(self):
        return self._parser0


