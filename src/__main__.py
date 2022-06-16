'''Generic launcher for *dsmcp* applications 


This script is used to launch dsmcp with command

.. code-block:: bash
    python3 -m dsmcp <application> <options>
    
:author: F. Voillat
:date: Created on 12 mai 2021
'''

from os.path import os
import sys


if __name__ == '__main__':
    if sys.version_info < (3,8):
        raise Exception("DSMCP requires at least Python version 3.8")
    
    from app.launcher import Launcher
    
    launcher = Launcher(os.path.dirname(__file__), add_help=True)
    launcher.parser0.add_argument('application',  choices=('basic', 'dev', 'prod', 'srv', 'ctrl'), help="""Application to launch:
- basic : Interface to handle the essential functionalities of
          the Dassym command boards.
- dev : Interface allowing advanced and development features.
- prod : Specialized interface for production operations.
- srv : Interface allowing advanced and after sale services features.
- ctrl : Special application for the final control of Dassym motors.
""") 
    launcher.preConfig() 
    
    if launcher.config.gui:
        if launcher.config.application == 'dev':
            from app.gui.dev import DevQtApp
            application = launcher.launch(DevQtApp)
        if launcher.config.application == 'panel':
            from app.gui.panel import PanelQtApp
            application = launcher.launch(PanelQtApp)
        else:
            from app.gui.basic import BasicQtApp
            application = launcher.launch(BasicQtApp)
    else:  
        if launcher.config.application == 'dev':
            from app.cli import DevCliApp
            application = launcher.launch(DevCliApp) 
        else:
            from app.cli import BasicCliApp
            application = launcher.launch(BasicCliApp) 
    try: 
        application.initialize()
        application.run()
    except Exception as e:
        application.handleError(e)
        sys.exit(1)
    
    
