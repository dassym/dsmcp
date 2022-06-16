'''Launcher for *dsmcp prod*.

:author: F. Voilat
:date: Created on 19 mars 2021
'''

import dapi2
from os.path import os
import sys

from _version import REQUIRED_PYTHON, REQUIRED_DAPI2
from app import APP_NAME


if __name__ == '__main__':
    if sys.version_info < REQUIRED_PYTHON:
        raise Exception(
            "{} requires at least Python version {}".format(APP_NAME, '.'.join([str(x) for x in REQUIRED_PYTHON]) )
            )
    if dapi2.VERSION < REQUIRED_DAPI2:
        raise Exception(
            "{} requires at least PyDapi2 version {}".format(APP_NAME, '.'.join([str(x) for x in REQUIRED_DAPI2]) )
            )
         
    
    from app.launcher import Launcher
    
    launcher = Launcher(os.path.dirname(__file__))
    launcher.preConfig()
    if not launcher.config.gui:
        launcher.log.warning(f"{APP_NAME!s} panel as no CLI mode. The GUI mode is launched.")
    from app.gui.prod import ProdQtApp
    application = launcher.launch(ProdQtApp)
    try: 
        application.initialize()
        application.startUp()
        application.run()
    except Exception as e:
        application.handleError(e)
        sys.exit(1)
        
        