import sys, os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'src'))

from _version import __version__, VERSION, __ver__, DATE, REQUIRED_PYTHON
import datetime as DT
import regex as RE





SHORTNAME = 'dsm-cp'
NAME = 'dsm-cp'
COMPACTNAME = 'dsmcp'
DESCRIPTION = 'Dassym control panel of Dassym API verion 2'
COPYRIGHT = 'Dassym SA - 2021'
AUTHORS = ('F.Voillat', 'T. Marti', 'H. Dupoux')

#DEB_DEPENDS = ', '.join(["{0:s} (>= {1:s})".format(k, '.'.join([str(x) for x in v])  ) for k,v in DEPENDENCIES.items() ])  


def setReleaseDate(isodate):
    d = DT.datetime.strptime(isodate, '%Y-%m-%d')
    ds = '{0:d}, {1:d}, {2:d}'.format(*d.timetuple())
    fname = os.path.join('src', '_version.py')
    with open(fname, 'r+') as f:
        tmp = f.read() 
    tmp = RE.sub( r'^DATE\s*=\s*DT\.date\([^)]+\)\s*$',
            "DATE = DT.date({0:s})".format(ds),
            tmp, flags=RE.MULTILINE
            )
    with open(fname, 'w+') as f:
        f.write(tmp) 
        
        
        