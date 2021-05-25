'''
Created on 2 oct. 2020

@author: fv
'''

from PyQt5.QtCore import QCoreApplication



from ..base import BaseApp
import app

       
class BaseCliApp(BaseApp, QCoreApplication):
    '''Base class for CLI applications
    
    :param Namespace config: Application configuration
    '''

    NAME = 'dcp-base-cli'
    
    @classmethod
    def cast(cls, app):
        assert isinstance(app, BaseApp)
        app.__class__ = cls
        return app
    
    def __init__(self, app_dir):
        QCoreApplication.__init__(self, [] )
        self.setApplicationVersion(app.__version__)
        self.setApplicationName(self.NAME)
        self.setOrganizationName(app.DASSYM)
        self.setOrganizationDomain(app.DASSYM_DOMAIN)
        BaseApp.__init__(self, app_dir)

    def connectionCallback(self, options):
        optionDefault = options[0][0]
        for option in options:
            print("[{}] {}".format(option[0], option[1]))
        txt = input("Select option from options [{}]: ".format(optionDefault))
        
        if txt == "":
            return int(optionDefault)
        else:
            return int(txt)
        
    # def initialize(self):
        # BaseApp.initialize(self)
        
                
        
        
     
            
        
        
