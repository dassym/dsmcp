'''

:author: fv
:date: Created on 24 mars 2021
'''
from dapi2.dapi2 import DApiAccessLevel

from ..base import BaseApp, BaseCliApp
from ..dcpshell import DcpShell


class DevCliApp(BaseCliApp):
    '''Class for *development* CLI application
    
    Args:
        app_dir (str): Application root directory
        lang (str): If defined the language to use, otherwise the local session language.
    '''
    NAME = 'dcp-dev'

    def __init__(self, app_dir, lang):
        '''Constructor'''
        super().__init__(app_dir, lang)
        
#    def prepareCfg(self, parser, preconf):
#        super().prepareCfg(parser, preconf)
#        parser.add_argument("--normal-mode", dest="dev_mode", action='store_false', help=BaseApp.tr("Sets DSMCP execution mode 'development'. (Default=normal mode)"))
#        parser.set_defaults(dev_mode=True)
        
        
    def initialize(self):
        super().initialize()
        self.shell = DcpShell(self)
    
    def run(self):
        '''Executes application'''
        self.log.info(BaseApp.tr('Run single shot'))
        
        if self.board is None:
            self.sayError('No board defined. No action is possible!')
            return self.terminate()
        
        level = self.board.getAccessLevel() 
        if level != DApiAccessLevel.NO:
            self.shell.prompt = level.name[0]+">"
        else: 
            self.shell.prompt = ">"
        self.shell.cmdloop(BaseApp.tr('Welcome to {0:s} version {1:s} shell! Type `help` or `?` to list commands.').format(
                    self.name,
                    self.version
                    ))
        return self.terminate()
        