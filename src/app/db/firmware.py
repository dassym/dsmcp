'''

:author:  F. Voillat
:date: 2022-06-24 Creation
:copyright: Dassym SA 2021
'''


from pathlib import Path
import functools
import struct
import re as RE
import datetime as DT

import dapi2
from .base import DbObject
from app.db.board import DbBoard

def wordxorbytes(buf, l):
    '''Convert (hash) the firmware name to a tag number.

    :param Bytes buf: The buffer containing the firmware name
    :param int l: The length expressed in byte
    :return: The computed tag number
    :rtype: int
    '''
    return functools.reduce(lambda x,y : x^y, struct.unpack('<'+'H'*l, buf[:2*l] + b'\x00'*(2*l-len(buf))))


def readString(f, length):
    '''Read a characters string from file

    :param file f: The file from which the characters will be read.
    :param int length: The length of the string to be read.
    :return: The string read
    :rtype: string
    '''
    s = ''
    c = b'*'
    i=0
    while i < length:
        c = f.read(1)
        i+=1
        if ord(c) != 0:
            s += chr(c[0])
        else:
            break
    return s

MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
'''List of months used to convert firmware build date.'''


def buf2date(buf):
    '''Convert the firmware build date into Python datetime

    :param Bytes buf: The buffer containing the firmware build date in format MMM DD YYYY
    :return: The firmware build date
    :rtype: Datetime
    '''
    s = buf.decode('ASCII')
    return DT.date(int(s[7:]), MONTHS.index(s[:3])+1, int(s[4:6]))


class DbFirmwares(DbObject):
    '''A class to contain the listed firmwares
    '''


    def __init__(self, owner, firmwares=[]):
        self._items = firmwares
        super().__init__(owner, oid=None)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __iter__(self):
        for item in self._items:
            yield item

    def clear(self):
        '''Clears the firmware list'''

        self._items.clear()

    def add(self, firmware):
        if firmware in self._items:
            self.log.warning(f"Attempt to add already registered firmware `{firmware.getKey()}` !")
        else:
            self._items.append(firmware)
            if firmware.owner is self.owner:
                firmware.setOwner(self)


    def findLastFirmwareVersion(self, tag):
        '''Find the last known version of a firmware.

        :param int tag: The firmware tag number.
        :return: the firmware found, or None
        '''

        l = sorted([x for x in self._items if x.tag==tag])
        return l[-1]

    def get(self, board_class, name=None, tag=None, version=None, date=None, ftype=None):
        '''Returns a firmware according to certain criteria.

        Args:
            board (DbBoard, dapi2.DBoard): The class of board for which the firmware is intended
            tag (int): If specified, filter firmwares according the tag number.
            verson (tuple): The firmware version (x,y).
            date (datetime): The firmware build date.
            ftype (str): If specified, filter firmwares according the type.

        Returns:
            The first firmware found, or `None`
        '''
        trg = board_class.getName().lower()
        for firm in self:
            if firm.target == trg \
                    and (name is None or name == firm.name)\
                    and (tag is None or tag == firm.tag)\
                    and ((version is None) or version == firm.version) \
                    and((date is None) or firm.date == date) :
                return firm
        return None

    def find(self, board, customer=None, tag=None, ftype=None):
        '''Returns a generator for the list of all firmwares matching certain criteria.

        Args:
            board (DbBoard, dapi2.DBoard): The class of board for which the firmware is intended
            customer (DbCustomer): If specified, filter firmwares according the customer.
            tag (int): If specified, filter firmwares according the tag number.
            ftype (str): If specified, filter firmwares according the type.

        Returns:
            The generator for the firmwares list.
        '''

        if not isinstance(board, DbBoard):
            board = self.db.getBoard(board)

        for firm in self:
            if firm.target == board.firmTarget \
                    and (customer is None or customer == firm.customer) \
                    and (ftype is None or ftype == firm.type) \
                    and (tag is None or tag == firm.tag) :
                yield firm

    def isLast(self, firmware):
        '''Checks if a firmware is the latest known version.

        :param Firmware firmware: The firmware to check
        :return: True, if the firmware is the latest version, otherwise false.
        '''

        return firmware is self.findLastFirmwareVersion(firmware.tag)


class DbFirmware(DbObject):
    '''The class representing a firmware for a Dassym board.

    '''

    @classmethod
    def fromBinary(cls, owner, fpath):
        obj = cls(owner)
        obj._initFromFirm(fpath)
        obj.log.debug(str(obj))
        return obj

    def __init__(self, owner, oid=None, tag=None, version=None, date=None, customer=None, target=None, fpath=None):
        super().__init__(owner, oid=oid)
        self.tag = None
        self.version = None
        self.date = None
        self.customer = None
        self.type = None
        self.target = None
        self.obsolete = False
        self.fpath = fpath

    def __eq__(self, other):
        assert other is None or isinstance(other, DbFirmware)
        return other is not None and self.tag == other.tag and self.version == other.version

    def __lt__(self, other):
        assert isinstance(other, DbFirmware)
        return self.tag < other.tag or (self.tag == other.tag and self.version < other.version)

    def __str__(self):
        try:
            return self.target +":"+self.name+" V"+dapi2.versionToStr(self.version)+" ("+self.date.isoformat()+" 0x{0:04x})".format(self.tag)
        except:
            super().__str__()

    def _initFromFirm(self, fpath):
        offset = 0x000
        fpath = Path(fpath)

        with fpath.open('rb') as f:
            f.seek(0x00)
            magic_number = f.read(6)
            self.type = 'firm'
            if magic_number != b"DASSYM":
                f.seek(0x10)
                magic_number = f.read(6)
                if magic_number != b"DASSYM":
                    raise Exception( 'The file `{0!s}` is not a Dassym firmware!'.format(fpath.name))
                offset = 0x2000
                self.type = 'full'

            f.seek(0x08+offset)
            board_name = readString(f,8)
            #self.target = board_name[:2].lower()+"-"+board_name[3:5]
            self.target = board_name
            f.seek(0x10+offset)
            self.version = ( ord(f.read(1)), ord(f.read(1)) )
            f.seek(0x14+offset)
            n = readString(f,32)
            if not n.endswith(self.type):
                raise Exception(f"The type {self.type} isn't coherent with the name {n}!")
            self.setName(n[:-len(self.type)-1])
            self.tag = wordxorbytes(bytes(n,encoding="ASCII") , 16)
            self._id = '{0:04x}'.format(self.tag)
            f.seek(0x34+offset)
            self.date = buf2date(f.read(11))
            m = RE.match('^(\w+)-',self.name)
            if m is not None:
                self.customer = self.db.getCustomer(m.group(1), insensitive=True)
        self.fpath = fpath


    def getKey(self):
        '''returns a key constructed with the name, version number and date of the firmware

        :return: The firmware key.
        :rtype: string
        '''
        return self.name + str(100-self.version[0]) + str(100-self.version[1]) + str(0xffff-dapi2.dateToWord(self.date))

    def getDescr(self, fmt='txt'):
        v = dapi2.versionToStr(self.version)
        d = self.date.isoformat()

        if fmt=='txt':
            return str(self)
        elif fmt=='html':
            return f"""<i>file: </i>{self.fpath.name}<br/>
                    <i>version: </i>{v}  <i>date: </i>{d}  <i>tag: </i>0x{self.tag:04X}<br/>
                    <i>customer: </i>{self.customer.name}<br/>
                    """
        else:
            raise ValueError("Invalid firmware description format!")


    def isLast(self):
        return self.owner.isLast(self)
