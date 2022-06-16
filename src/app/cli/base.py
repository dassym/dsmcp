'''
Implementation of CLI application base class.

:author: F. Voillat
:date: 2020-10-02 Creation 
'''

#from PyQt5.QtCore import QCoreApplication



from ..base import BaseApp


class BaseCliApp(BaseApp): #, QCoreApplication):
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
        #QCoreApplication.__init__(self, [] )
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
        
        
    def prepareL10n(self, lang):
        '''Prepare the application localization
        
        :param str lang: If defined the language to use, otherwise the local session language.
        '''
        pass        
        
    def isGui(self):
        return False  
     
        
        
