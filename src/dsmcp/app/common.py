from os.path import os
import sys
from enum import IntEnum
  

APP_NAME = 'dsmcp'
'''Application name'''

APP_DESCRIPTION = "The DSM-CP application offers a control panel to control Dassym boards."
'''Application description'''

DASSYM = 'Dassym'
'''Application editor'''

DASSYM_DOMAIN = 'dassym.com'
'''Application domain'''

TEMP_DIR = os.getenv('TMP') if os.name == 'nt' else '/tmp'
'''Path to temporary directory'''
#TODO: TEMP_DIR pour darwin 

DEFAULT_LOG_DIR = TEMP_DIR 
'''Path to deefault directory to store log file.'''

LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
'''Format pattern for logging message'''


DIR = os.path.dirname(os.path.realpath(__file__))
'''Directory of application package'''

IMG_DIR = os.path.join( DIR, "..", "img")
'''Directory of application iamges'''

DATA_DIR = os.path.join( DIR, "..", "data")
'''Directory of application data'''

FIRM_DIR = os.path.join( DIR, "..", "firm")
'''Directory of Dassym's board firmware'''

USR_HOME_DIR = os.path.expanduser("~")
'''User home directory.'''


USR_DATA_DIR = os.path.join(USR_HOME_DIR, ".config","dassym") if sys.platform == 'linux' \
        else os.path.join(os.getenv('LOCALAPPDATA'), "Dassym") if sys.platform[:3] == 'win' \
        else os.path.join(USR_HOME_DIR, 'Library', 'Application Support', 'Dassym') if sys.platform[:6] == 'darwin' \
        else None
'''User Dassym directory.'''
        
USR_DATA_APP_DIR = os.path.join(USR_DATA_DIR, APP_NAME)
'''Application User Dassym directory.'''    

APP_PYTHON_REQUIRES = (3, 8)


class VERBOSITY(IntEnum):
    '''Enumeration for application verbosity level'''
    
    NONE = 0
    MINIMAL = 1
    LOW = 2
    MEDIUM = 3 
    HIGH = 4


