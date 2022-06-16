import datetime as DT


MAJOR_VERSION = 0
'''Major version number'''

MINOR_VERSION = 5
'''Minor version number'''

REVISION_VERSION = 0
'''Revision version number'''

VERSION = (MAJOR_VERSION, MINOR_VERSION, REVISION_VERSION)
'''Version number as 3-tuples containing *major*, *minor* and *revision* numbers.''' 

__version__ = '{0:d}.{1:d}.{2:d}'.format(*VERSION)
'''Appication version number'''

__ver__ = '{0:d}.{1:d}'.format(*VERSION)
'''Appication short version number'''

DATE = DT.date(2022, 6, 16)
'''Release date'''

REQUIRED_PYTHON = (3,7)
'''The required Python verison'''

REQUIRED_DAPI2 = (0,3,10)
'''The required PyDapi2 verison'''
