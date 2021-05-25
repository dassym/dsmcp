'''

:author: fv
:date: Created on 24 mars 2021
'''
from .base import BaseCliApp
from .dcpshell import DcpShell
from ..base import BaseApp
from dapi2.dapi2 import DApiAccessLevel


class DevCliApp(BaseCliApp):
    '''Class for *development* CLI application
    
    :param Namespace config: Application configuration
    '''
    NAME = 'dcp-dev'

    def __init__(self, config):
        '''Constructor'''
        super().__init__(config)
        
    def prepareCfg(self, parser):
        super().prepareCfg(parser)
        parser.add_argument("--normal-mode", dest="dev_mode", action='store_false', help=BaseApp.tr("Sets DSMCP execution mode 'development'. (Default=normal mode)"))
        parser.set_defaults(dev_mode=True)
        
        
    def initialize(self):
        super().initialize()
        self.shell = DcpShell(self)
    
    def run(self):
        '''Executes application'''
        self.log.info(BaseApp.tr('Run single shot'))
        level = self.board.getAccessLevel() 
        if level != DApiAccessLevel.NO:
            self.shell.prompt = level.name[0]+">"
        else: 
            self.shell.prompt = ">"
        self.shell.cmdloop(BaseApp.tr('Welcome to \033[1m{0:s}\033[0m version {1:s} shell! Type `help` or `?` to list commands.').format(
                    self.applicationName(),
                    self.applicationVersion()
                    ))
        return self.terminate()
        