'''Definition of *basic* CLI application.

:author: F. Voillat
:date: 2021-0-24 Creation
:copyright: Dassym 2021
'''
from dapi2.dapi2 import DApiAccessLevel

from app.cli.base import BaseCliApp
from app.cli.dcpshell import DcpShell


class BasicCliApp(BaseCliApp):
    '''Class for *basic* CLI application
    
    Args:
        app_dir (str): Application root directory
        lang (str): If defined the language to use, otherwise the local session language.
    '''
    NAME = 'dcp-basic'
    '''Application name'''
    


    def __init__(self, app_dir, lang):
        '''Constructor'''
        super().__init__(app_dir,lang)
        

        
    def initialize(self):
        '''Initialize application'''
        super().initialize()
        self.shell = DcpShell(self)
    
    def run(self):
        '''Executes application'''
        
        super().run()
        
        if self.board is not None:
            level = self.board.getAccessLevel()
        else:
            level = DApiAccessLevel.NO
        if level != DApiAccessLevel.NO:
            self.shell.prompt = level.name[0]+">"
        else: 
            self.shell.prompt = ">"
        self.shell.cmdloop('Welcome to \033[1m{0:s}\033[0m version {1:s} shell! Type `help` or `?` to list commands.'.format(
                    self.name,
                    self.version
                    ))
        return self.terminate()
        