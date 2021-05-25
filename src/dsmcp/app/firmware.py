'''

:author:  F. Voillat
:date: 2021-04-28 Creation
:copyright: Dassym SA 2021
'''
from os.path import os
import re as RE
import datetime as DT
import functools

import struct
from dapi2.common import dateToWord, versionToStr
import logging


MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec') 

def wordxorbytes(buf, l):
    return functools.reduce(lambda x,y : x^y, struct.unpack('<'+'H'*l, buf[:2*l] + b'\x00'*(2*l-len(buf))))

def buf2date(buf):
    s = buf.decode('ASCII')
    return DT.date(int(s[7:]), MONTHS.index(s[:3])+1, int(s[4:6]))

def readString(f, length):
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
    
    @classmethod
    def newFromConfig(cls, config):
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
        return other is not None and self.id == other.id and self.version == other.version    
    
    def __lt__(self, other):
        assert isinstance(other, Firmware)
        return self.tag < other.tag or (self.tag == other.tag and self.version < other.version)     
    
    def __str__(self):
        try:  
            return self.target +":"+self.name+" V"+versionToStr(self.version)+" ("+self.date.isoformat()+" 0x{0:04x})".format(self.tag)
        except:
            super().__str__()
        
    def softId(self):
        if self.tag is not None:
            return '{0:04x}'.format(self.tag)
        else:
            return None
        
    def key(self):
        return self.name + str(100-self.version[0]) + str(100-self.version[1]) + str(0xffff-dateToWord(self.date))         
        

class Firmwares(object):
    
    def __init__(self, app):
        self.log = logging.getLogger(self.__class__.__name__)
        self._app = app
        self._items = []
        
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        return self._items[index]
     
    def __iter__(self):
        for item in self._items:
            yield item     
        
        
    def discover(self, firm_paths, board=None):
        
        def scanDir(path):
            r = RE.compile(r".*_firm\.bin",)
            for folder, subs, files in os.walk(path):
                for fname in files:
                    if fname[0] == '.' or r.match(fname) is None:
                        continue  
                    #self.log.debug(fname)
                    firmware = Firmware.newFromFile(os.path.join(folder,fname))
                    
                    if firmware.type == 'full':
                        #self.log.warning('Full firmware :'+fname)
                        continue
                    if firmware.customer is None and not self._app.config.dev_mode:
                        self.log.warning('Invalid firmware :'+fname)
                        continue
                    
                    if board is not None and firmware.target != board.name:
                        continue
                    self._items.append(firmware)
                    self.log.debug(str(firmware))
                
                for pname in subs:
                    if pname[0]== '.':
                        continue
                    scanDir(os.path.join(folder,pname)) 
        
        for path in firm_paths:
            scanDir(path)
            
    def findLastFirmwareVersion(self, tag): 
        l = sorted([x for x in self._items if x.tag==tag])
        return l[-1] 
            
    def get(self, board_class, tag, version=None, date=None):
        trg = board_class.getName().lower()
        for firm in self:
            if firm.target == trg \
                    and tag == firm.tag \
                    and ((version is None) or version == firm.version) \
                    and((date is None) or firm.date == date) :
                return firm
        return None
    
    def find(self, board_class, tag=None):
        for firm in self:
            if firm.target == board_class.getName().lower() and (tag is None or tag == firm.tag):
                yield firm
            
    def isLast(self, firmware):
        return firmware is self.findLastFirmwareVersion(firmware.tag)        

        