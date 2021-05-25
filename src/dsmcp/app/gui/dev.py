'''

:author: fv
:date: Created on 24 mars 2021
'''
from app.gui.base import BaseGuiApp

class DevGuiApp(BaseGuiApp):
    '''Class for *development* GUI application
    
    :param Namespace config: Application configuration
    '''
    NAME = 'dcp-dev'

    def __init__(self, config):
        '''Constructor'''
        super().__init__(config)