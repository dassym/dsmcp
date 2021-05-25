import sys, os.path
sys.path.insert(0, os.path.abspath('./src/dsmcp/app'))
import datetime as DT
import regex as RE
from _version import __version__ 
from common import APP_NAME as SHORTNAME, APP_DESCRIPTION as DESCRIPTION 



def setReleaseDate(isodate):
    d = DT.datetime.strptime(isodate, '%Y-%m-%d')
    ds = '{0:d}, {1:d}, {2:d}'.format(*d.timetuple())
    fname = os.path.join('src', 'app','_version.py')
    with open(fname, 'r+') as f:
        tmp = f.read() 
    tmp = RE.sub( r'^DATE\s*=\s*DT\.date\([^)]+\)\s*$',
            "DATE = DT.date({0:s})".format(ds),
            tmp, flags=RE.MULTILINE
            )
    with open(fname, 'w+') as f:
        f.write(tmp) 