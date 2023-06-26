'''Launcher for *dsmcp developer*. 


:author: F. Voillat
:date: Created on 24 mars 2021
'''

from os.path import os
import sys

from app.version import REQUIRED_PYTHON  # @UnresolvedImport
from app import APP_NAME


if __name__ == '__main__':
    if sys.version_info < REQUIRED_PYTHON:
        raise Exception(
            "{} requires at least Python version {}".format(APP_NAME, '.'.join([str(x) for x in REQUIRED_PYTHON]) )
            )

    from app.launcher import Launcher
    launcher = Launcher(os.path.dirname(__file__))
    launcher.preConfig()
    if launcher.config.gui:
        from app.gui.dev import DevQtApp
        application = launcher.launch(DevQtApp)
    else:  
        from app.cli import DevCliApp
        application = launcher.launch(DevCliApp)
    try: 
        application.startUp()
        application.initialize()
        application.run()
    except Exception as e:
        application.handleError(e)
        sys.exit(1)