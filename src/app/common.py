'''Definition of the common elements of the *app* module

.. |date| date::

:author: F. Voillat
:date: 2021-03-19 Created
:date: |date| Last Updated 
'''

from enum import IntEnum
from os.path import os
import sys


APP_NAME = 'dsmcp'
'''Application name'''

APP_DESCRIPTION = "The DsmCP application offers a control panel to control Dassym boards."
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

USR_DATA_DIR = os.path.join(USR_HOME_DIR, "dassym") if sys.platform == 'linux' \
        else os.path.join(os.getenv('USERPROFILE'), "Dassym") if sys.platform[:3] == 'win' \
        else os.path.join(USR_HOME_DIR, 'Library', 'Application Support', 'dassym') if sys.platform[:6] == 'darwin' \
        else None
'''User Dassym directory.'''

OS_SHORT_NAME = 'lnx' if sys.platform == 'linux' \
        else 'win' if sys.platform[:3] == 'win' \
        else 'mac' if sys.platform[:6] == 'darwin' \
        else '?'
'''OS short name.'''        

OS_CONFIG_DIRS = [os.path.join('etc', "dassym")] if sys.platform == 'linux' \
        else [] if sys.platform[:3] == 'win' \
        else [] if sys.platform[:6] == 'darwin' \
        else []
'''OS configurations directory.'''

OS_DEFAULT_CCONFIG_NAME = "{}-{}.ini".format(APP_NAME, OS_SHORT_NAME)
'''OS Default name of configuration file.'''

DEFAULT_CCONFIG_NAME = "{}.ini".format(APP_NAME)
'''Default name of configuration file.'''


#DEFAUT_CONFIG = os.path.join( DEFAULT_CCONFIG_NAME)

DEFAULT_USR_CONFIG =  os.path.join(USR_DATA_DIR, DEFAULT_CCONFIG_NAME)       
'''Default path of user's configuration file.'''
        
USR_DATA_APP_DIR = os.path.join(USR_DATA_DIR, APP_NAME)
'''Application User Dassym directory.'''

USR_FIRM_DIR = os.path.join(USR_DATA_DIR, 'firm')  
'''Path of user's firmware directory.'''   


FIRM_PATHS = [USR_FIRM_DIR, FIRM_DIR]
'''List of paths to locate the firmware.'''

CONFIG_PATHS = [USR_DATA_DIR] + OS_CONFIG_DIRS
'''List of paths to locate the configuation file.'''


DEFAULT_SERIAL = '/dev/ttyS0' if sys.platform == 'linux' \
    else 'COM1' if sys.platform[:3] == 'win' \
    else '/dev/ttyUSB0' if sys.platform[:6] == 'darwin' \
    else '/dev/ttyS0' 
'''Default serial port to use to connect to the card.'''
    
DEFAULT_HOST = 'sav.dassym.com:30443' 
'''Default URL of Dassym's SAV server.'''


class VERBOSITY(IntEnum):
    '''Enumeration for application verbosity level'''
    
    NONE = 0
    MINIMAL = 1
    LOW = 2
    MEDIUM = 3 
    HIGH = 4


