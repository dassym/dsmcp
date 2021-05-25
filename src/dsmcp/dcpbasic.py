'''Launcher for *dsmcp basic*.

:author: F. Voilat
:date: Created on 19 mars 2021
'''

import sys
from os.path import os

if __name__ == '__main__':
    if sys.version_info < (3,8):
        raise Exception("DSMCP requires at least Python version 3.8")
    
    from app.launcher import Launcher
    
    launcher = Launcher(os.path.dirname(__file__))
    launcher.preConfig()
    if launcher.config.no_gui:
        from app.cli import BasicCliApp
        application = launcher.launch(BasicCliApp) 
    else:
        from app.gui import BasicGuiApp
        application = launcher.launch(BasicGuiApp)  
    try: 
        application.initialize()
        application.run()
    except Exception as e:
        application.handleError(e)
        sys.exit(1)