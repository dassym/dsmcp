'''Launcher for *dsmcp panel*.

:author: F. Voilat
:date: Created on 19 mars 2021
'''

from os.path import os
import sys

from app.version import REQUIRED_PYTHON  # @UnresolvedImport
from app import APP_NAME


if __name__ == '__main__':
    if sys.version_info < REQUIRED_PYTHON:
        raise Exception(
            "DSMCP requires at least Python version {}".format('.'.join([str(x) for x in REQUIRED_PYTHON]) )
            )
    
    from app.launcher import Launcher
    
    launcher = Launcher(os.path.dirname(__file__))
    launcher.preConfig()
    if not launcher.config.gui:
        launcher.log.warning(f"{APP_NAME!s} panel as no CLI mode. The GUI mode is launched.")
    from app.gui.panel import PanelQtApp
    application = launcher.launch(PanelQtApp)
    try: 
        application.startUp()
        application.initialize()
        application.run()
    except Exception as e:
        application.handleError(e)
        sys.exit(1)