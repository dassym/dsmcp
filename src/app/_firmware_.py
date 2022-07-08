'''
The "firmware" module implements the functionalities and classes allowing the discovery and use of firmware files.

:author:  F. Voillat
:date: 2021-04-28 Creation
:copyright: Dassym SA 2021
'''
from dapi2.common import dateToWord, versionToStr
import functools
import logging
from os.path import os
import struct

import datetime as DT
import re as RE


MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
'''List of months used to convert firmware build date.''' 

def wordxorbytes(buf, l):
    '''Convert (hash) the firmware name to a tag number.
    
    :param Bytes buf: The buffer containing the firmware name 
    :param int l: The length expressed in byte
    :return: The computed tag number
    :rtype: int
    '''
    return functools.reduce(lambda x,y : x^y, struct.unpack('<'+'H'*l, buf[:2*l] + b'\x00'*(2*l-len(buf))))

def buf2date(buf):
    '''Convert the firmware build date into Python datetime
    
    :param Bytes buf: The buffer containing the firmware build date in format MMM DD YYYY
    :return: The firmware build date
    :rtype: Datetime
    ''' 
    s = buf.decode('ASCII')
    return DT.date(int(s[7:]), MONTHS.index(s[:3])+1, int(s[4:6]))

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


class Firmware(object):
    '''The class representing a firmware for a Dassym board.
    
    :param string filename: The name of the file containing the firmware
    '''
    
    @classmethod
    def newFromConfig(cls, config):
        '''Create a new firmware from data contained in the configuration Namespace.
        
        :param Namespace config: The configuration containing the data
        :return: The new Firmware object.
        :rtype: Firmware 
        '''
        obj = Firmware(config.filename)
        obj.name = config.name
        obj.version = config.version
        try:
            obj.date =  DT.datetime.strptime(config.date, '%b %d %Y')
        except:
            obj.date =  DT.datetime.strptime(config.date, '%Y-%m-%d')
        obj.descr = config.descr
        obj.customer = config.customer
        obj.tag = wordxorbytes(bytes(obj.name,encoding="ASCII") , 16)
        obj.board_id = config.board[:2].lower()+config.board[3:5] 
        obj.type = config.type 
        return obj
    
    @classmethod
    def newFromFile(cls, filename, descr=None, customer=None):
        '''Create a new firmware from a file.
        
        :param string filename: The name of the file containing the firmware.
        :param string descr: A firmware description (optional).
        :param string customer: the client for which the firmware is intended (optional).
        :return: The new Firmware object.
        :rtype: Firmware 
        '''
        obj = Firmware(filename)
        offset = 0x000
        
        with open(filename, 'rb') as f:
            f.seek(0x00)
            magic_number = f.read(6)
            obj.type = 'firm'
            if magic_number != b"DASSYM":
                f.seek(0x10)
                magic_number = f.read(6)
                if magic_number != b"DASSYM":
                    raise Exception( 'The file `{0!s}` is not a Dassym firmware!'.format(os.path.basename(filename)))
                offset = 0x2000
                obj.type = 'full' 
            
            f.seek(0x08+offset)
            board_name = readString(f,8)
            obj.target = board_name[:2].lower()+"-"+board_name[3:5] 
            f.seek(0x10+offset)
            obj.version = ( ord(f.read(1)), ord(f.read(1)) )
            f.seek(0x14+offset)
            obj.name = readString(f,32)
            obj.tag = wordxorbytes(bytes(obj.name,encoding="ASCII") , 16)
            f.seek(0x34+offset)
            obj.date = buf2date(f.read(11))
            m = RE.match('^(\w+)-',obj.name)
            if m is not None:
                obj.customer = m.group(1) 
        return obj
        
    def __init__(self, filename):
        self.filename = filename
        self.name = None
        self.tag = None
        self.version = None
        self.date = None
        self.descr = None
        self.customer = None
        self.type = None
        self.target = None
        
    def __eq__(self, other):
        assert other is None or isinstance(other, Firmware)
        return other is not None and self.tag == other.tag and self.version == other.version    
    
    def __lt__(self, other):
        assert isinstance(other, Firmware)
        return self.tag < other.tag or (self.tag == other.tag and self.version < other.version)     
    
    def __str__(self):
        try:  
            return self.target +":"+self.name+" V"+versionToStr(self.version)+" ("+self.date.isoformat()+" 0x{0:04x})".format(self.tag)
        except:
            super().__str__()
        
    def softId(self):
        '''Returns the firmware tag number aka software ID
        
        :return: The firmware tag number
        :rtype: int
        '''
        if self.tag is not None:
            return '{0:04x}'.format(self.tag)
        else:
            return None
        
    def key(self):
        '''returns a key constructed with the name, version number and date of the firmware
        
        :return: The firmware key.
        :rtype: string
        ''' 
        return self.name + str(100-self.version[0]) + str(100-self.version[1]) + str(0xffff-dateToWord(self.date))         
        

class Firmwares(object):
    '''A class to contain the listed firmwares 
    
    :param BaseApp app: The application.
    '''
    
    R_FIRM = RE.compile(r".*_firm\.bin",)
    
    def __init__(self, app):
        self.log = logging.getLogger(self.__class__.__name__)
        self._app = app
        self._items = []
        self._board = None
        
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
        
    def discover(self, firm_paths, board=None):
        '''Discover firmwares stored in directories
        
        :param list firm_paths: List of directories in which to search for firmware
        :param BaseBoard board:
        
        ''' 
       
        def scanDir(path):
            if not os.path.exists(path):
                self._app.sayWarning(f'The path `{path}` does not exist!')
                return 

            for fname in os.listdir(path):
                fpath = os.path.join(path,fname)
                if os.path.isdir(fpath):
                    scanDir(fpath)
                elif os.path.isfile(fpath):
                    if self.R_FIRM.match(fname) is not None:
                        #self.log.debug(' > fpath = '+fpath)
                        firmware = Firmware.newFromFile(fpath)
                        
                        if firmware.type == 'full':
                            continue
                        if firmware.customer is None and not self._app.config.dev_mode:
                            self.log.warning('Invalid firmware :'+fname)
                            continue
                        
                        if board is not None and firmware.target != self._board.name:
                            continue
                        self._items.append(firmware)
                        #self.log.debug(str(firmware))
                    elif os.path.basename(fpath) == 'data.xml':
                        
        
        self._board = board
        
        for path in firm_paths:
            scanDir(path)
        
        self._items.sort()
        self._app.sayMedium(f'{len(self)} firmwares have been listed.')
        
            
    def findLastFirmwareVersion(self, tag):
        '''Find the last known version of a firmware.
        
        :param int tag: The firmware tag number.
        :return: the firmware found, or None
        '''
         
        l = sorted([x for x in self._items if x.tag==tag])
        return l[-1] 
            
    def get(self, board_class, tag, version=None, date=None):
        '''Returns a firmware according to certain criteria.
        
        :param class board_class: The class of board for which the firmware is intended
        :param int tag: The firmware tag number.
        :param tuple verson: The firmware version (x,y).
        :param datetime date: The firmware build date.
        :return:  the firmware found, or None 
        '''
        trg = board_class.getName().lower()
        for firm in self:
            if firm.target == trg \
                    and tag == firm.tag \
                    and ((version is None) or version == firm.version) \
                    and((date is None) or firm.date == date) :
                return firm
        return None
    
    def find(self, board_class, tag=None):
        '''Returns a generator for the list of all firmwares matching certain criteria.

        :param class board_class: The class of board for which the firmware is intended
        :param int tag: The firmware tag number.
        :return: The generator for the firmware list.
        '''
        for firm in self:
            if firm.target == board_class.getName().lower() and (tag is None or tag == firm.tag):
                yield firm
            
    def isLast(self, firmware):
        '''Checks if a firmware is the latest known version.
        
        :param Firmware firmware: The firmware to check
        :return: True, if the firmware is the latest version, otherwise false.
        '''
        
        return firmware is self.findLastFirmwareVersion(firmware.tag)        

        