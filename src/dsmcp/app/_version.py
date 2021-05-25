import datetime as DT

MAJOR_VERSION = 0
'''Major version number'''

MINOR_VERSION = 1
'''Minor version number'''

REVISION_VERSION = 1
'''Revision version number'''

VERSION = (MAJOR_VERSION, MINOR_VERSION, REVISION_VERSION)
'''Version number as 3-tuples containing *major*, *minor* and *revision* numbers.''' 

__version__ = '{0:d}.{1:d}.{2:d}'.format(*VERSION)
'''Appication version number'''

__ver__ = '{0:d}.{1:d}'.format(*VERSION)
'''Appication short version number'''

DATE = DT.date(2021, 5, 25)