'''Launcher for *dsmcp basic*.

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
    if launcher.config.gui:
        from app.gui.basic import BasicQtApp
        application = launcher.launch(BasicQtApp)
    else:
        from app.cli import BasicCliApp
        application = launcher.launch(BasicCliApp) 
    try: 
        application.initialize()
        application.run()
    except Exception as e:
        application.handleError(e)
        sys.exit(1)