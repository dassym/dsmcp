'''

:author:  F. Voillat
:date: 2022-06-03 Creation
:copyright: Dassym SA 2021
'''

import dapi2

from pathlib import Path
import datetime as DT

from app.utils import str2version, str2bool
from .base import DbObject



class DbBoardBios(DbObject):

    def __init__(self, owner, oid=None, file=None):
        super().__init__(owner, oid=oid)
        self.file = file

    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.file = xelement.get('file')

class DbBoardVersion(DbObject):


    def __init__(self, owner, oid=None, date=None, obsolete=None):
        self.obsolete = obsolete
        self.date = date
        self._ver = None
        super().__init__(owner, oid=oid )

    def __eq__(self, other):
        assert other is None or isinstance(other, DbBoardVersion)
        return other is not None and self.id == other.id

    def __lt__(self, other):
        assert isinstance(other, DbBoardVersion)
        return self.id < other.id

    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.obsolete = str2bool(xelement.get('obsolete'))
        if 'date' in xelement.keys():
            self.date = DT.datetime.strptime(xelement.get('date'), '%Y-%m-%d').date()

    def setId(self, oid):
        super().setId(oid)
        self._ver = str2version(self.id)


    def isLast(self):
        return self == self.owner.vers[0]

    @property
    def major(self):
        return self._ver[0]

    @property
    def minor(self):
        return self._ver[1]


class DbBoardVariant(DbObject):
    def __init__(self, owner, oid=None, ref=None, img=None):
        self.ref = ref
        self.img = img
        self._firm_target = None
        super().__init__(owner, oid=oid)

    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        if 'ref' in xelement.keys():
            self.ref = xelement.get('ref')

        self._firm_target = xelement.get('firmtarget')

        ximg = xelement.find('img')
        if ximg is not None:
            s = ximg.text
            s.strip()
            path = Path(s)
            if path.name == s:
                path = self.db.getCurrentLoadingPath().parent.joinpath(path)


            self.img = str(path)

    def findSofts(self, customer=None, tag=None):
        return self.db.firmwares.find(self.board, customer=customer, tag=tag)

    @property
    def vers(self):
        return self.owner.vers

    @property
    def board(self):
        return self.owner

    @property
    def firmTarget(self):
        if self._firm_target is not None:
            return self._firm_target
        else:
            return self.owner.firmTarget


class DbBoard(DbBoardVariant):


    CLASSES = dict( [ (c.__name__, c) for c in dapi2.DBoard.getSubclasses()  ] )

    def __init__(self, owner, oid=None, bios=None):
        self._vers = []
        self._variants = []
        self.bios = bios
        self.board_class = None
        super().__init__(owner, oid=oid)

    def _initFromXml(self, xelement):
        super()._initFromXml(xelement)
        self.board_class = self.CLASSES[xelement.get('class')]

        self._vers = []
        for xel in xelement.findall('version'):
            self._vers.append(DbBoardVersion.fromXml(self, xel, oid=xel.get('id')))
        self._vers.sort(reverse=True)

        self.bios = DbBoardBios.fromXml(self, xelement.find('bios'))

        self._variants = [DbBoardVariant.fromXml(self, xelement)]
        for xel in xelement.findall('variant'):
            self._variants.append(DbBoardVariant.fromXml(self, xel))
        self._variants.sort()

    def addVersion(self, v):
        self._vers.append(v)
        self._vers.sort(reverse=True)

    def getLastVersion(self):
        return self._vers[0]

    def getVersion(self, vid):
        for v in self._vers:
            if v.id == vid:
                return v
        raise KeyError(f'Hardware `{vid!s}` not found!')

    def getVariant(self, vid, insensitive=False):
        if insensitive:
            VID = vid.upper()
            for v in self._variants:
                if v.id.upper() == VID:
                    return v
        else:
            for v in self._variants:
                if v.id == vid:
                    return v
        raise KeyError(f'Variant `{vid!s}` not found!')

    def findSofts(self, customer=None, tag=None):
        return self.db.firmwares.find(self, customer=customer, tag=tag)

    def findVariants(self, customer=None):
        if customer is None or (not customer.boards and not customer.boardvariants):
            return (self._variants, [])
        else:
            custvariants = list(x.variant for x in customer.boardvariants)
            bok = self in (x.board for x in customer.boards)
            r = ([],[])
            for v in self._variants:
                ok = bok and (not customer.boardvariants or v in custvariants)
                r[int(not ok)].append(v)
        return r


    @property
    def vers(self):
        return self._vers
    @property
    def variants(self):
        return self._variants

    @property
    def board(self):
        return self

    @property
    def firmTarget(self):
        return  self._firm_target



