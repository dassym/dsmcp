# -*- coding: utf-8 -*-

from ._version import VERSION, __ver__, __version__, MAJOR_VERSION, MINOR_VERSION, REVISION_VERSION 

from .common import *


#
# exit_code = 0
# '''Application exit code''' 
#
# application = None
# '''The application itself'''


from .i18n import res_i18n  #@UnusedImport 

#from .launcher import prepareCfg, processCfg
from .base import BaseApp
from . import utils

#from .cli import *
#from .gui import *

#
# log = None
# '''The application logger'''
#
# args_config = {}
# '''The arguments given by INI file'''
# config = None
# '''The application configuration'''
#
# initial_dir = None
# '''The application initial directory. The folder of the main script.'''
#
# parser = None
# '''The argument line parser'''