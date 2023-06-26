import sys, os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'src','app'))

from version import __version__, VERSION, __ver__, DATE, REQUIRED_PYTHON, REQUIRED_DAPI2
from common import APP_NAME as NAME, APP_DESCRIPTION as DESCRIPTION, APP_PUBLISHER as PUBLISHER
import datetime as DT
import regex as RE


SHORTNAME = NAME.lower()
COMPACTNAME = SHORTNAME

COPYRIGHT = PUBLISHER + ' - ' + DATE.strftime('%Y')
AUTHORS = ('F.Voillat', 'T. Marti', 'H. Dupoux')
DOCURL = "https://www.dassym.com/doc/dsmcp/"



#DEB_DEPENDS = ', '.join(["{0:s} (>= {1:s})".format(k, '.'.join([str(x) for x in v])  ) for k,v in DEPENDENCIES.items() ])


def setReleaseDate(isodate):
    d = DT.datetime.strptime(isodate, '%Y-%m-%d')
    ds = '{0:d}, {1:d}, {2:d}'.format(*d.timetuple())
    fname = os.path.join('src', 'app', 'version.py')
    with open(fname, 'r+') as f:
        tmp = f.read()
    tmp = RE.sub( r'^DATE\s*=\s*DT\.date\([^)]+\)\s*$',
            "DATE = DT.date({0:s})".format(ds),
            tmp, flags=RE.MULTILINE
            )
    with open(fname, 'w+') as f:
        f.write(tmp)


