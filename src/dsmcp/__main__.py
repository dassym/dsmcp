'''Generic launcher for *dsmcp* applications 


This script is used to launch dsmcp with command

.. code-block:: bash
    python3 -m dsmcp <application> <options>
    
:author: F. Voillat
:date: Created on 12 mai 2021
'''

import sys
from os.path import os


if __name__ == '__main__':
    if sys.version_info < (3,8):
        raise Exception("DSMCP requires at least Python version 3.8")
    
    from dsmcp.app.launcher import Launcher
    
    launcher = Launcher(os.path.dirname(__file__), add_help=True)
    launcher.parser0.add_argument('application',  choices=('basic', 'dev', 'prod', 'service')) 
    launcher.preConfig() 
    
    if launcher.config.no_gui:
        if launcher.config.application == 'dev':
            from dsmcp.app.cli import DevCliApp
            application = launcher.launch(DevCliApp) 
        else:
            from dsmcp.app.cli import BasicCliApp
            application = launcher.launch(BasicCliApp) 
    else:
        if launcher.config.application == 'dev':
            from dsmcp.app.gui import DevGuiApp
            application = launcher.launch(DevGuiApp)
        else:
            from dsmcp.app.gui import BasicGuiApp
            application = launcher.launch(BasicGuiApp)  
    try: 
        application.initialize()
        application.run()
    except Exception as e:
        application.handleError(e)
        sys.exit(1)
    
    
