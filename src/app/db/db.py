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
from .board import DbBoard, DbFirmwares, DbFirmware
from .partner import DbCustomer


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
            

        for item in path.iterdir():
            if item.is_dir():
                self._scanDir(item)
            elif item.is_file():
                if item.name == 'data.xml':
                    self.loadFile(item)
                elif self.R_FIRM.match(str(item)) is not None:
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
        self.log.info('Load data from XML file `{}`.'.format(path))

        self._current_loading_path = path 

        xparser = ET.XMLParser()
        xparser.resolvers.add( PrefixResolver('user') )
        
        with path.open() as f:
            xtree = ET.parse(f, xparser)
            xtree.xinclude()
            xroot = xtree.getroot()
             
            
            for xcustomer in xroot.findall("standardcustomer"):
                ocustomer = DbStandardCustomer.fromXml(self, xcustomer)
                self.customers[ocustomer.id] = ocustomer
                self.standard_cust = ocustomer 
            
            for xcustomer in xroot.findall("customer"):
                ocustomer = DbCustomer.fromXml(self, xcustomer)
                self.customers[ocustomer.id] = ocustomer
            
            for xboard in xroot.findall('board'):
                bid = xboard.get('id') 
                oboard = DbBoard.fromXml(self, xboard, oid=bid)
                self.boards[oboard.id] = oboard
        
        self._current_loading_path = None
        
    def getCurrentLoadingPath(self):
        return self._current_loading_path
            
    def getCustomers(self, standard=False):
        return [ x for x in self.customers.values() if (standard or not x.standard)]
    
    def getCustomer(self, cid):
        if cid is None:
            return None
        try:
            return self.customers[cid.upper()]
        except KeyError:
            self.log.warning(f"getCustomer:unknown customer `{cid}` creation !") 
            cust = DbCustomer(self, oid=cid, name=cid)
            self.customers[cust.id] = cust 
            return cust
            
              
    def getBoard(self, bid):
        if bid is None:
            return None
        return self.boards[bid]
    
    def getBoardVariant(self, vid, board=None):
        if board is not None:
            return board.getVariant(vid)
        else:
            for b in self.boards.values():
                try:
                    return b.getVariant(vid)
                except KeyError:
                    pass
        raise KeyError(f'Variant `{vid!s}` not found!')

            
   
            
    @property
    def db(self):
        return self    
        
    
