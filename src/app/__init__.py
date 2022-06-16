# -*- coding: utf-8 -*-

from _version import VERSION, __ver__, __version__, MAJOR_VERSION, MINOR_VERSION, REVISION_VERSION

from . import utils
from .base import BaseApp
from .common import *


#
# exit_code = 0
# '''Application exit code''' 
#
# application = None
# '''The application itself'''
# from .i18n import i18n_rc  #@UnusedImport 
#from .launcher import prepareCfg, processCfg
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