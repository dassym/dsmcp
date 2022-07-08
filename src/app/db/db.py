'''

:author:  F. Voillat
:date: 2022-03-07 Creation
:copyright: Dassym SA 2021
'''

import logging
from pathlib import Path

from app.db.partner import DbStandardCustomer
import lxml.etree as ET
import re as RE

from ..common import USR_DATA_DIR
from .board import DbBoard
from .firmware import DbFirmwares, DbFirmware
from .partner import DbCustomer


DB_DATA_FILE = 'data.xml'


class PrefixResolver(ET.Resolver):
    def __init__(self, prefix):
        if prefix[-1] != ':':
            prefix += ':'
        self.log = logging.getLogger('PrefixResolver[{0!s}]'.format(prefix)) 
        self.prefix = prefix
        
    def resolve(self, url, pubid, context):
        if url.startswith(self.prefix):
            path = Path(USR_DATA_DIR).joinpath(url[len(self.prefix):])
            self.log.debug(url + "->" + str(path))
            return self.resolve_filename(str(path),context)    
    

class Database(object):
    
    R_FIRM = RE.compile(r".*_firm\.bin",)

    def __init__(self, app, lang='en'):
        self._scanned_paths = []
        self._current_loading_path = None
        self.app = app
        self.board_class = None
        self.log = logging.getLogger('Database')
        self.log.debug('Construct')
        self.lang = lang
        self.boards = {}
        self.customers = {}
        self.firmwares = DbFirmwares(self)
        self.firm_paths = []
        self.standard_cust = None
        
    def clear(self):
        self.boards = {}
        self.customers = {}
        self.firmwares.clear()
        
    
    def _scanDir(self, path):
        if not path.exists():
            self.app.sayWarning(f'The path `{path}` does not exist!')
            return 
        if self._alreadySacanned(path):
            self.app.sayWarning(f'The path `{path}` has already been scanned!')
            return 
            
        fdata = Path(path).joinpath(DB_DATA_FILE) 
        if fdata.exists():
            self.loadFile(fdata)

        for item in path.iterdir():
            if item.is_file() and self.R_FIRM.match(str(item)) is not None:
                #self.log.debug(' > fpath = '+fpath)
                firmware = DbFirmware.fromBinary(self.firmwares, str(item))
                
                if firmware.type == 'full':
                    continue
                if firmware.customer is None and not self.app.config.dev_mode:
                    self.log.warning('Invalid firmware :'+item.name)
                    continue
                
                if self.board_class is not None and firmware.target != self.board_class.getName():
                    continue
                self.firmwares.add(firmware)
                #self.log.debug(str(firmware))
            elif item.is_dir():
                self._scanDir(item)
            
        self._scanned_paths.append(path)
    
    
    def _alreadySacanned(self, path):
        for p in self._scanned_paths:
            if p in path.parents:
                return True 
        return False
    
    def discover(self, paths, board_class=None, clear=True):
        '''Discovers DSMCP data in the mentioned directories
        
        Args:
            paths (str, list, tuple): list of directories to scan 
            board_class (class): If defined : filter data according the board class
            clear (bool): If `True` : clear all data before scan.
        '''
        if clear:
            self.clear()
                
        if isinstance(paths, str):
            opaths = [Path(paths)]
        else:
            paths = list(set(paths))
            paths.sort()
            opaths = [ Path(p).resolve() for p in paths ]
        
        self.board_class = board_class
            
        self.log.info('Discovers data in {:s}'.format(str(opaths)))
        
        for opath in opaths:
            self._scanDir(opath)
             
            
        
        
    def loadFile(self, path):
        self.log.debug('loadFile({0!s}).'.format(path))

        self._current_loading_path = path 

        xparser = ET.XMLParser()
        xparser.resolvers.add( PrefixResolver('user') )
        
        with path.open() as f:
            self.app.sayMedium(f"Load data from XML file `{path!s}`")
            xtree = ET.parse(f, xparser)
            xtree.xinclude()
            xroot = xtree.getroot()

            for xboard in xroot.findall('board'):
                bid = xboard.get('id') 
                oboard = DbBoard.fromXml(self, xboard, oid=bid)
                self.boards[oboard.id] = oboard
             
            
            for xcustomer in xroot.findall("standardcustomer"):
                ocustomer = DbStandardCustomer.fromXml(self, xcustomer)
                self.customers[ocustomer.id] = ocustomer
                self.standard_cust = ocustomer 
            
            for xcustomer in xroot.findall("customer"):
                ocustomer = DbCustomer.fromXml(self, xcustomer)
                self.customers[ocustomer.id] = ocustomer
            
        
        self._current_loading_path = None
        
    def getCurrentLoadingPath(self):
        return self._current_loading_path
            
    def getCustomers(self, standard=False):
        return [ x for x in self.customers.values() if (standard or not x.standard)]
    
    def getCustomer(self, cid, insensitive=False):
        if cid is None:
            return None
        try:
            if insensitive:
                CID = cid.upper()
                for k,v in self.customers.items():
                    if k.upper() == CID:
                        return v
                raise KeyError() 
            else: 
                return self.customers[cid]
        except KeyError:
            self.log.warning(f"getCustomer:unknown customer `{cid}` creation !") 
            cust = DbCustomer(self, oid=cid, name=cid)
            self.customers[cust.id] = cust 
            return cust
            
              
    def getBoard(self, bid, insensitive=False):
        if bid is None:
            return None
        try:
            if insensitive:
                BID = bid.upper()
                for k,v in self.boards.items():
                    if k.upper() == BID:
                        return v
                raise KeyError() 
            else: 
                return self.boards[bid]
        except KeyError:
            raise KeyError(f"Board `{bid!s}` not found in database!")
        
    def findBoards(self, customer=None):
        if customer is None or not customer.boards:
            return (self.boards.values(), [])
        else:
            r = ([],[])
            for b in self.boards.values():
                r[int(not b in customer.boards)].append(b)
        return r  
            
    def getBoardVariant(self, vid, board=None, insensitive=False):
        if board is not None:
            return board.getVariant(vid,insensitive=insensitive)
        else:
            for b in self.boards.values():
                try:
                    return b.getVariant(vid,insensitive=insensitive)
                except KeyError:
                    pass
        raise KeyError(f'Variant `{vid!s}` not found in database!')

    def findBoardVariants(self, board, customer=None):
        return board.findVariants(customer)
            
   
            
    @property
    def db(self):
        return self    
        
    
