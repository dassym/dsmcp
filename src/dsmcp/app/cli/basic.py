'''Definition of *basic* CLI application.

:author: F. Voillat
:date: 2021-0-24 Creation
:copyright: Dassym 2021
'''
from app.cli.base import BaseCliApp
from app.cli.dcpshell import DcpShell
from app.base import BaseApp
from dapi2.dapi2 import DApiAccessLevel


class BasicCliApp(BaseCliApp):
    '''Class for *basic* CLI application
    
    :param Namespace config: Application configuration
    '''
    NAME = 'dcp-basic'
    '''Application name'''
    


    def __init__(self, app_dir):
        '''Constructor'''
        super().__init__(app_dir)
        

        
    def initialize(self):
        '''Initialize application'''
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
        